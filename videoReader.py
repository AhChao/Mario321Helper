# python builtin lib
import threading
import queue
import sys
import math

# pip install lib
import cv2
import streamlink
import configparser
from pygrabber.dshow_graph import FilterGraph
from win11toast import toast

# local py file
from imageRecognize import isSimilarToTargetTemplate
from textRecognize import recognizeTheImage
import globalVar as gl


def initSettingValues():
    config = configparser.ConfigParser()
    config.read(r'config.ini', encoding="utf8")
    gl.set_value("currentStageCount", 0)
    gl.set_value("currentRefresh", 0)
    gl.set_value("targetStageCount", int(
        config.get('321Config', 'targetStageCount')))
    gl.set_value("maxRefresh", int(config.get('321Config', 'maxRefresh')))
    gl.set_value("globalMainWindowObj", "")
    gl.set_value("thresholdFor321", 0)
    gl.set_value("thresholdForCourseClear", 0)
    gl.set_value("coursesList", set())


def loggingStreaming(mainWindowObj):
    gl.set_value("globalMainWindowObj", mainWindowObj)
    config = configparser.ConfigParser()
    config.read(r'config.ini', encoding="utf8")
    isDebugWithCompareFrame = config.get(
        'DisplayConfig', 'debugWithCompareFrame') == "True"
    isStreamWithFullScreen = config.get(
        'StreamSettings', 'isStreamWithFullScreen') == "True"
    mainWindowObj.setTextToLabel(buildDisplayString())

    matchCourseClearTimes = 0
    cooldownTimeForCourseClear = 0
    isMatchForCourseClearCoolDownNow = False
    cooldownTimeFor321 = 0
    isMatchFor321CoolDownNow = False

    streamSource = config.get('StreamSettings', 'streamSource')
    fps = 0
    if streamSource == "LocalVideo":
        cap = cv2.VideoCapture("testImgs/321TestVideo.mkv")
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        cap.set(cv2.CAP_PROP_POS_FRAMES, 285*fps)
        # 260 for test course clear
        # 285 for refresh
    elif streamSource == "Twitch":
        session = streamlink.Streamlink()
        session.set_option("twitch-low-latency", True)
        session.set_option("hls-live-edge", 1)
        session.set_option("hls-segment-stream-data", True)
        session.set_option("hls-playlist-reload-time", "live-edge")
        session.set_option("stream-segment-threads", 2)
        session.set_option("player", "mpv")

        twitchStreamLink = 'https://www.twitch.tv/' + \
            config.get('StreamSettings', 'twtichStreamerName')
        streams = streamlink.streams(twitchStreamLink)
        url = streams['720p60'].url if "720p60" in streams else streams['480p']
        cap = cv2.VideoCapture(url)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
    elif streamSource == "LocalVirtualCamera":
        graph = FilterGraph()
        device = graph.get_input_devices().index("OBS Virtual Camera")
        cap = cv2.VideoCapture(device)
        print("Current Virtual Camera Size - width : " +
              str(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))) + " height : " + str(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        print("Reszie Virtual Camera to - width : " +
              str(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))) + " height : " + str(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        fps = 30
        cap.set(cv2.CAP_PROP_POS_FRAMES, 260*fps)
        ret, checkingSource = cap.read()
        obsSourceCheckingResult = cv2.matchTemplate(cv2.convertScaleAbs(cv2.imread(
            "./imgs/obsNoSource.png")), checkingSource, cv2.TM_SQDIFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(obsSourceCheckingResult)
        if minVal <= 0.01:
            print("Error : OBS Virtual Camera not opened or cloud not be found.")
            toast(
                "Obs Virtual Camera 未開啟",
                "影像來源設定為使用 Obs Virtual Camera，但未正確讀取到畫面。(Obs回傳為待機影像)")
            return

    print("fps : " + str(fps))

    save_interval = 1.5  # before 0.3 when use 321 icon
    frame_count = 0
    val321Queue = queue.Queue()
    while cap.isOpened():
        ret, frame = cap.read()
        frame_count += 1
        if isMatchForCourseClearCoolDownNow:
            cooldownTimeForCourseClear += 1
            if cooldownTimeForCourseClear >= fps*2:
                cooldownTimeForCourseClear = 0
                isMatchForCourseClearCoolDownNow = False

        if isMatchFor321CoolDownNow:
            cooldownTimeFor321 += 1
            if cooldownTimeFor321 >= fps*2:
                cooldownTimeFor321 = 0
                isMatchFor321CoolDownNow = False

        if config.get('DisplayConfig', 'debugWithShowFrame') == "True":
            cv2.imshow('frame', frame)  # may spend about 0.12s to display

        # Compare Per 0.5 seconds
        if math.floor(frame_count % (fps * save_interval)) == 0:
            # Compare with 321 template
            isInputMatchTo321Template = False
            isInputMatchToCourseClearTemplate = False
            thresholdFor321 = gl.get_value("thresholdFor321")
            thresholdForCourseClear = gl.get_value("thresholdForCourseClear")
            if not isMatchFor321CoolDownNow:
                threadFor321Detect = threading.Thread(target=lambda q, arg1, arg2, arg3: q.put(isSimilarToTargetTemplate(
                    arg1, arg2, arg3)), args=(val321Queue, "courseTitleMapping", cv2.convertScaleAbs(frame), thresholdFor321))  # 2 count then plus 1)
                threadFor321Detect.start()
            if not isMatchForCourseClearCoolDownNow:
                isInputMatchToCourseClearTemplate = isSimilarToTargetTemplate(
                    "courseClearMapping", cv2.convertScaleAbs(frame), thresholdForCourseClear)
            if not isMatchFor321CoolDownNow:
                threadFor321Detect.join()
            # compare with courseClear, cd for 5 seconds
            if isInputMatchToCourseClearTemplate:
                matchCourseClearTimes += 1
                if matchCourseClearTimes >= 1:
                    currentStageCount += 1
                    isMatchForCourseClearCoolDownNow = True
                    mainWindowObj.setTextToLabel(buildDisplayString())
            if not isMatchFor321CoolDownNow:
                isInputMatchTo321Template = val321Queue.get()
            if isInputMatchTo321Template:
                textRecognized = recognizeTheImage(
                    frame, isStreamWithFullScreen, isDebugWithCompareFrame)
                if textRecognized != "" and textRecognized != None:
                    coursesList = gl.get_value("coursesList")
                    coursesList.add(textRecognized)
                    print("Today Courses : " + str(coursesList))
                    gl.set_value("currentRefresh", max(
                        len(coursesList) - currentStageCount - 1, 0))
                    isMatchFor321CoolDownNow = True
                    mainWindowObj.setTextToLabel(buildDisplayString())
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("Error : Source is terminated, please check again then restart the program.")
    toast(
        "影像來源已中斷",
        "本來使用的影像來源已中斷，請重新確認後再運行程式")


def buildDisplayString():
    return str(gl.get_value("currentRefresh"))+" / " + \
        str(gl.get_value("maxRefresh")) + " 刷  " + \
        str(gl.get_value("currentStageCount")) + " / " + \
        str(gl.get_value("targetStageCount")) + " 關"


def addFakeStage():
    coursesList = gl.get_value("coursesList")
    currentRefresh = gl.get_value("currentRefresh")
    currentStageCount = gl.get_value("currentStageCount")
    targetCount = currentRefresh + currentStageCount + 1
    i = 0
    while len(coursesList) < targetCount:
        fakeName = "fake stage"+str(i)
        while fakeName in coursesList:
            i += 1
            fakeName = "fake stage"+str(i)
        coursesList.add(fakeName)


def operateOnCurrentRefreshCount(val):
    currentRefresh = gl.get_value("currentRefresh")
    currentRefresh += val
    coursesList = gl.get_value("coursesList")
    if currentRefresh < 0:
        return
    if val < 0:
        val *= -1
        while (val > 0 and len(coursesList) > 0):
            coursesList.pop()
            val -= 1
    else:
        addFakeStage()
    gl.set_value("currentRefresh", currentRefresh)
    gl.get_value("globalMainWindowObj").setTextToLabel(buildDisplayString())


def operateOnCurrentStageCount(val):
    currentStageCount = gl.get_value("currentStageCount")
    currentStageCount += val
    if currentStageCount < 0:
        return
    gl.set_value("currentStageCount", currentStageCount)
    gl.get_value("globalMainWindowObj").setTextToLabel(buildDisplayString())


def exitTheProgram():
    exitMsg = "Program shut down noramlly by clicked the exitbtn."
    print(exitMsg)
    sys.exit(exitMsg)


def resetCurrentValues():
    config = configparser.ConfigParser()
    config.read(r'config.ini', encoding="utf8")

    gl.set_value("currentRefresh", 0)
    gl.set_value("currentStageCount", 0)
    gl.set_value("coursesList", set())

    gl.set_value("targetStageCount", int(
        config.get('321Config', 'targetStageCount')))
    gl.set_value("maxRefresh", int(config.get('321Config', 'maxRefresh')))
    gl.get_value("globalMainWindowObj").setTextToLabel(buildDisplayString())

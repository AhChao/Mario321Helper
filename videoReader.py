import cv2
import streamlink
import configparser
from imageRecognize import isSimilarToTargetTemplate
import math
from pygrabber.dshow_graph import FilterGraph
import threading
import queue
import time

currentStageCount = 0
currentRefresh = 0
targetStageCount = 7
maxRefresh = 15
globalMainWindowObj = ""


def loggingStreaming(mainWindowObj):
    global globalMainWindowObj
    globalMainWindowObj = mainWindowObj
    config = configparser.ConfigParser()
    config.read(r'config.ini', encoding="utf8")

    global currentStageCount
    global currentRefresh
    global targetStageCount
    global maxRefresh
    currentStageCount = 0
    currentRefresh = 0
    targetStageCount = int(config.get('321Config', 'targetStageCount'))
    maxRefresh = int(config.get('321Config', 'maxRefresh'))
    timeMeasurementMessage = config.get(
        'TestSettings', 'timeMeasurementMessage')
    mainWindowObj.setTextToLabel(buildDisplayString())

    matchCourseClearTimes = 0
    match321Times = 0
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
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        fps = 30
        cap.set(cv2.CAP_PROP_POS_FRAMES, 260*fps)

    print("fps", fps)

    save_interval = 0.3
    frame_count = 0
    val321Queue = queue.Queue()
    while cap.isOpened:
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

        # print("here", frame_count % (fps * save_interval))
        # Compare Per 0.5 seconds
        if math.floor(frame_count % (fps * save_interval)) == 0:
            # Compare with 321 template
            isInputMatchTo321Template = False
            isInputMatchToCourseClearTemplate = False
            starttime = time.perf_counter()
            if not isMatchFor321CoolDownNow:
                # threadFor321Detect = threading.Thread(target=isSimilarToTargetTemplate(
                #    "321Mapping", cv2.convertScaleAbs(frame), 0.4), args=(val321Queue, ))  # 2 count then plus 1)
                threadFor321Detect = threading.Thread(target=lambda q, arg1, arg2, arg3: q.put(isSimilarToTargetTemplate(
                    arg1, arg2, arg3)), args=(val321Queue, "321Mapping", cv2.convertScaleAbs(frame), 0.3))  # 2 count then plus 1)
                threadFor321Detect.start()
            if not isMatchForCourseClearCoolDownNow:
                isInputMatchToCourseClearTemplate = target = isSimilarToTargetTemplate(
                    "courseClearMapping", cv2.convertScaleAbs(frame), 0.1)
            if not isMatchFor321CoolDownNow:
                threadFor321Detect.join()
            endtime = time.perf_counter()
            # print(endtime-starttime)
            if not isMatchFor321CoolDownNow:
                isInputMatchTo321Template = val321Queue.get()
            if isInputMatchTo321Template:
                match321Times += 1
                if match321Times >= 1:
                    currentRefresh += 1
                    isMatchFor321CoolDownNow = True
                    mainWindowObj.setTextToLabel(buildDisplayString())
            else:
                match321Times = 0
            # compare with courseClear, cd for 5 seconds
            if isInputMatchToCourseClearTemplate:
                matchCourseClearTimes += 1
                if matchCourseClearTimes >= 1:
                    currentStageCount += 1
                    isMatchForCourseClearCoolDownNow = True
                    mainWindowObj.setTextToLabel(buildDisplayString())
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # cap.release()
    # cv2.destroyAllWindows()


def buildDisplayString():
    global currentRefresh
    global maxRefresh
    global currentStageCount
    global targetStageCount
    return str(currentRefresh)+" / " + str(maxRefresh) + " 刷  " + \
        str(currentStageCount) + " / " + str(targetStageCount) + " 關"


def operateOnCurrentRefreshCount(val):
    global currentRefresh
    currentRefresh += val
    global globalMainWindowObj
    globalMainWindowObj.setTextToLabel(buildDisplayString())


def operateOnCurrentStageCount(val):
    global currentStageCount
    currentStageCount += val
    global globalMainWindowObj
    globalMainWindowObj.setTextToLabel(buildDisplayString())


def resetCurrentValues():
    global currentStageCount
    global currentRefresh
    currentRefresh = 0
    currentStageCount = 0

    global maxRefresh
    global targetStageCount
    config = configparser.ConfigParser()
    config.read(r'config.ini', encoding="utf8")
    targetStageCount = int(config.get('321Config', 'targetStageCount'))
    maxRefresh = int(config.get('321Config', 'maxRefresh'))

    global globalMainWindowObj
    globalMainWindowObj.setTextToLabel(buildDisplayString())

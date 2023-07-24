import cv2
import streamlink
import configparser
from imageRecognize import isSimilarToTargetTemplate
import math
import time
from pygrabber.dshow_graph import FilterGraph
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
        cap.set(cv2.CAP_PROP_POS_FRAMES, 260*fps)
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

    save_interval = 0.1
    frame_count = 0

    while cap.isOpened:
        ret, frame = cap.read()
        frame_count += 1
        if timeMeasurementMessage == "True":
            print("Per run in is Opened:", time.perf_counter())
        if isMatchForCourseClearCoolDownNow:
            cooldownTimeForCourseClear += 1
            if cooldownTimeForCourseClear >= fps*5:
                cooldownTimeForCourseClear = 0
                isMatchForCourseClearCoolDownNow = False
                print("Match for Course Clear CD finish")

        if isMatchFor321CoolDownNow:
            cooldownTimeFor321 += 1
            if cooldownTimeFor321 >= fps*2:
                cooldownTimeFor321 = 0
                isMatchFor321CoolDownNow = False
                print("Match for 321 CD finish")

        if config.get('DisplayConfig', 'debugWithShowFrame') == "True":
            cv2.imshow('frame', frame)

        # print("here", frame_count % (fps * save_interval))
        # Compare Per 0.5 seconds
        if math.floor(frame_count % (fps * save_interval)) == 0:
            if timeMeasurementMessage == "True":
                print("Per Interval:", time.perf_counter())
            # Compare with 321 template
            inputMatchTo321Template = isSimilarToTargetTemplate(
                "./sampleImgs/321Mapping.png", cv2.convertScaleAbs(frame), 0.55)  # 2 count then plus 1
            if inputMatchTo321Template:
                if not isMatchFor321CoolDownNow:
                    match321Times += 1
                    if match321Times >= 2:
                        currentRefresh += 1
                        isMatchFor321CoolDownNow = True
                        mainWindowObj.setTextToLabel(buildDisplayString())
            else:
                match321Times = 0
            # compare with courseClear, cd for 5 seconds
            if isSimilarToTargetTemplate("./sampleImgs/courseClearMapping.png", cv2.convertScaleAbs(frame), 0.1):
                if not isMatchForCourseClearCoolDownNow:
                    matchCourseClearTimes += 1
                    if matchCourseClearTimes >= 2:
                        currentStageCount += 1
                        isMatchForCourseClearCoolDownNow = True
                        mainWindowObj.setTextToLabel(buildDisplayString())
            if timeMeasurementMessage == "True":
                print("Finish Per Interval:", time.perf_counter())

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

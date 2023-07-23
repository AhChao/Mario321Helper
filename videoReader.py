import cv2
import streamlink
import configparser
from imageRecognize import isSimilarToTargetTemplate
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
    mainWindowObj.setTextToLabel(buildDisplayString())

    matchCourseClearTimes = 0
    match321Times = 0
    cooldownTimeForCourseClear = 0
    isMatchForCourseClearCoolDownNow = False

    useLocalVideo = True if config.get(
        'TestingSettings', 'useLocalVideoToTest') == "True" else False
    fps = 0
    if useLocalVideo:
        cap = cv2.VideoCapture("testImgs/321TestVideo.mkv")
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        cap.set(cv2.CAP_PROP_POS_FRAMES, 260*fps)
        # 260 for test course clear
        # 285 for refresh
    else:
        session = streamlink.Streamlink()
        session.set_option("twitch-low-latency", True)
        session.set_option("hls-live-edge", 1)
        session.set_option("hls-segment-stream-data", True)
        session.set_option("hls-playlist-reload-time", "live-edge")
        session.set_option("stream-segment-threads", 2)
        session.set_option("player", "mpv")

        streams = streamlink.streams('https://www.twitch.tv/slrabbit99')
        url = streams['720p60'].url if "720p60" in streams else streams['480p']
        cap = cv2.VideoCapture(url)
        fps = int(cap.get(cv2.CAP_PROP_FPS))

    save_interval = 0.4
    frame_count = 0

    while cap.isOpened:
        ret, frame = cap.read()
        frame_count += 1
        if isMatchForCourseClearCoolDownNow:
            cooldownTimeForCourseClear += 1
            if cooldownTimeForCourseClear >= fps*5:
                cooldownTimeForCourseClear = 0
                isMatchForCourseClearCoolDownNow = False

        if config.get('DisplayConfig', 'debugWithShowFrame') == "True":
            cv2.imshow('frame', frame)

        # Compare Per 0.5 seconds
        if frame_count % (fps * save_interval) == 0:
            # Compare with 321 template
            inputMatchTo321Template = isSimilarToTargetTemplate(
                "./sampleImgs/321Mapping.png", cv2.convertScaleAbs(frame), 0.55)  # 2 count then plus 1
            if inputMatchTo321Template:
                match321Times += 1
                if match321Times >= 2:
                    currentRefresh += 1
                    mainWindowObj.setTextToLabel(buildDisplayString())
                    match321Times = 0
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
    global globalMainWindowObj
    globalMainWindowObj.setTextToLabel(buildDisplayString())

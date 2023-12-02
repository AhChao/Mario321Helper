import cv2
import numpy as np
import configparser

config = configparser.ConfigParser()
config.read(r'config.ini', encoding="utf8")
isStreamWithFullScreen = config.get(
    'StreamSettings', 'isStreamWithFullScreen') == "True"

TemplateFor321 = cv2.convertScaleAbs(
    cv2.imread("./sampleImgs/321Mapping.png" if not isStreamWithFullScreen else "./sampleImgs/321Mapping_fullScreen.png"))
TemplateForCourseTitle = cv2.convertScaleAbs(
    cv2.imread("./sampleImgs/courseTitleMapping.png" if not isStreamWithFullScreen else "./sampleImgs/courseTitleMapping_fullScreen.png"))
TemplateForCourseClear = cv2.convertScaleAbs(
    cv2.imread("./sampleImgs/courseClearMapping.png" if not isStreamWithFullScreen else "./sampleImgs/courseClearMapping_fullScreen.png"))


def isSimilarToTargetTemplate(templateName, sourceObj, threshold):
    global TemplateFor321
    global TemplateForCourseClear
    global isStreamWithFullScreen
    template = TemplateForCourseTitle if templateName == "321Mapping" else TemplateForCourseClear
    if templateName == "321Mapping":
        if isStreamWithFullScreen:
            x = 0
            y = 0
            h = 500
            w = 1600
        else:
            x = 0
            y = 200
            h = 300
            w = 1000

        sourceObj = sourceObj[y:y+h, x:x+w]

    if templateName == "321Mapping":
        templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)
        targetGray = cv2.cvtColor(sourceObj, cv2.COLOR_BGR2RGB)
    else:
        templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        targetGray = cv2.cvtColor(sourceObj, cv2.COLOR_BGR2GRAY)

    method = cv2.TM_SQDIFF_NORMED
    result = cv2.matchTemplate(templateGray, targetGray, method)

    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    minLocX = minLoc[0]
    minLocY = minLoc[1]
    loc = np.where(result <= threshold)

    for pt in zip(*loc[::-1]):
        if pt != None:
            print("Matching Well with " + templateName +
                  " , " + str(minVal) + " , " + str(minLoc))
            return True
    else:
        return False

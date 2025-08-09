import cv2
import numpy as np
import globalVar as gl


def isSimilarToTargetTemplate(templateName, sourceObj, threshold, isMappingWithOldImage):
    isStreamWithFullScreen = gl.get_value("isStreamWithFullScreen")
    TemplateForCourseTitle = cv2.convertScaleAbs(
        cv2.imread("./sampleImgs/courseTitleMapping.png"
                    if not isStreamWithFullScreen
                    else "./sampleImgs/courseTitleMapping_fullScreen_old.png"
                    if isMappingWithOldImage
                    else "./sampleImgs/courseTitleMapping_fullScreen.png"))

    TemplateForCourseClear = cv2.convertScaleAbs(
        cv2.imread("./sampleImgs/courseClearMapping.png"
                    if not isStreamWithFullScreen
                    else "./sampleImgs/courseClearMapping_fullScreen_old.png"
                    if isMappingWithOldImage
                    else "./sampleImgs/courseClearMapping_fullScreen.png"))

    template = TemplateForCourseTitle if templateName == "courseTitleMapping" else TemplateForCourseClear
    if templateName == "courseTitleMapping":
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
        templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)
        targetGray = cv2.cvtColor(sourceObj, cv2.COLOR_BGR2RGB)
    else:
        if isStreamWithFullScreen:
            x = 482
            y = 469
            h = 137
            w = 953
        else:
            x = 0
            y = 200
            h = 300
            w = 1000
        sourceObj = sourceObj[y:y+h, x:x+w]
        templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        targetGray = cv2.cvtColor(sourceObj, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('EasyOCR2', templateGray) 
        # cv2.waitKey(1000)
        # cv2.imshow('EasyOCR3', targetGray) 
        # cv2.waitKey(1000)

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
        # print("Not match well!" + str(templateName) + ", " + str(minVal))
        return False

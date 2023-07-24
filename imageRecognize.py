import cv2
import numpy as np
import configparser
import time

config = configparser.ConfigParser()
config.read(r'config.ini', encoding="utf8")
isStreamWithFullScreen = config.get(
    'StreamSettings', 'isStreamWithFullScreen') == "True"

TemplateFor321 = cv2.convertScaleAbs(
    cv2.imread("./sampleImgs/321Mapping.png" if not isStreamWithFullScreen else "./sampleImgs/321Mapping_fullScreen.png"))
TemplateForCourseClear = cv2.convertScaleAbs(
    cv2.imread("./sampleImgs/courseClearMapping.png" if not isStreamWithFullScreen else "./sampleImgs/courseClearMapping_fullScreen.png"))


def isSimilarToTargetTemplate(templateName, sourceObj, threshold):
    if templateName != "321Mapping":
        startTime = time.perf_counter()
    global TemplateFor321
    global TemplateForCourseClear
    template = TemplateFor321 if templateName == "321Mapping" else TemplateForCourseClear
    large_image = sourceObj

    method = cv2.TM_SQDIFF_NORMED
    result = cv2.matchTemplate(template, large_image, method)

    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    minLocX = minLoc[0]
    minLocY = minLoc[1]
    # print(minLocX, minLocY)
    loc = np.where(result <= threshold)
    if templateName != "321Mapping":
        endtime = time.perf_counter()
        print(endtime - startTime)
    for pt in zip(*loc[::-1]):
        if pt != None:
            # special handle for checking 1's position
            global isStreamWithFullScreen
            if templateName == "321Mapping" and isStreamWithFullScreen and\
                    ((minLocY < 400 or minLocY > 500) or
                     (minLocX < 1000 or minLocX > 1150)):
                # print("Not match well with pos!", templateName, minVal, minLoc)
                return False

            print("Matching Well with", templateName, minVal, minLoc)
            return True
    else:
        #        if templateName == "321Mapping":
        # print("Not match well!", templateName, minVal)
        return False

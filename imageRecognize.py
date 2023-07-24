import cv2
import numpy as np

TemplateFor321 = cv2.convertScaleAbs(
    cv2.imread("./sampleImgs/321Mapping1.png"))
TemplateForCourseClear = cv2.convertScaleAbs(
    cv2.imread("./sampleImgs/courseClearMapping.png"))


def isSimilarToTargetTemplate(templateName, sourceObj, threshold):
    global TemplateFor321
    global TemplateForCourseClear
    template = TemplateFor321 if templateName == "321Mapping" else TemplateForCourseClear
    large_image = sourceObj

    method = cv2.TM_SQDIFF_NORMED
    result = cv2.matchTemplate(template, large_image, method)

    loc = np.where(result <= threshold)
    for pt in zip(*loc[::-1]):
        if pt != None:
            print("Matching Well with", templateName)
            return True
    else:
        # print("Not match well!")
        return False

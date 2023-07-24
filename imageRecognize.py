import cv2
import numpy as np


def isSimilarToTargetTemplate(templatePath, sourceObj, threshold):
    small_image = cv2.convertScaleAbs(cv2.imread(templatePath))
    large_image = sourceObj

    method = cv2.TM_SQDIFF_NORMED
    result = cv2.matchTemplate(small_image, large_image, method)

    loc = np.where(result <= threshold)
    for pt in zip(*loc[::-1]):
        if pt != None:
            print("Matching Well with", templatePath)
            return True
    else:
        # print("Not match well!")
        return False

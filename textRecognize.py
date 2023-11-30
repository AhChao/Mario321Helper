import easyocr
import re
import io
import cv2
from PIL import Image


def is_valid_courseName(input_string):
    pattern = re.compile(r'^\w+-\w+-\w+$')
    return bool(pattern.match(input_string))


def recognizeTheImage(source, isFullScreen, isDebugWithCompareFrame):
    reader = easyocr.Reader(['en'])
    if isFullScreen:
        roi = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)[250:400, 0:500]
    else:
        roi = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)[250:400, 350:550]
    if isDebugWithCompareFrame:
        cv2.imshow('EasyOCR', roi)  # check mapping course id area
    result = reader.readtext(roi)

    for idx, item in enumerate(result):
        ocrText = item[1]
        if is_valid_courseName(ocrText):
            return ocrText

import cv2
import numpy as np


def compareWithTargetTemplate(templatePath, sourceObj, threshold):
    # small_image = cv2.convertScaleAbs(cv2.imread("./sampleImgs/321Mapping.png"))
    small_image = cv2.convertScaleAbs(cv2.imread(templatePath))
    assert small_image is not None, "file could not be read, check with os.path.exists()"
    # large_image = cv2.convertScaleAbs(cv2.imread("./testImgs/321Test6.jpg"))
    large_image = sourceObj
    assert large_image is not None, "file could not be read, check with os.path.exists()"

    method = cv2.TM_SQDIFF_NORMED
    result = cv2.matchTemplate(small_image, large_image, method)

    mn, maxVal, mnLoc, maxLoc = cv2.minMaxLoc(result)
    # minVal, maxVal, minLoc, maxLoc

    # Draw the rectangle:
    # Extract the coordinates of our best match
    MPx, MPy = mnLoc

    # Step 2: Get the size of the template. This is the same size as the match.
    trows, tcols = small_image.shape[:2]

    loc = np.where(result <= threshold)
    for pt in zip(*loc[::-1]):
        if pt != None:
            print("Matching Well with", templatePath)
            break
    else:
        print("Not match well!")

    # print(mn, maxVal, mnLoc, maxLoc)
    # Step 3: Draw the rectangle on large_image
    cv2.rectangle(large_image, (MPx, MPy),
                  (MPx+tcols, MPy+trows), (0, 0, 255), 2)

    # Display the original image with the rectangle around the match.
    # cv2.imshow('output', large_image)

    # The image is only displayed if we call this
    # cv2.waitKey(0)

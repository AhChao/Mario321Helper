import cv2
import numpy as np

method = cv2.TM_SQDIFF_NORMED

# Read the images from the file
small_image = cv2.convertScaleAbs(cv2.imread("./sampleImgs/321Mapping.png"))
assert small_image is not None, "file could not be read, check with os.path.exists()"
large_image = cv2.convertScaleAbs(cv2.imread("./testImgs/321Test6.jpg"))
assert large_image is not None, "file could not be read, check with os.path.exists()"

result = cv2.matchTemplate(small_image, large_image, method)

# We want the minimum squared difference
mn, maxVal, mnLoc, maxLoc = cv2.minMaxLoc(result)
# minVal, maxVal, minLoc, maxLoc

# Draw the rectangle:
# Extract the coordinates of our best match
MPx, MPy = mnLoc

# Step 2: Get the size of the template. This is the same size as the match.
trows, tcols = small_image.shape[:2]

threshold = 0.55
loc = np.where(result <= threshold)
for pt in zip(*loc[::-1]):
    print("pt", pt)
    if pt != None:
        print("Matching Well")
        break
else:
    print("Not match well!")

print(mn, maxVal, mnLoc, maxLoc)
# Step 3: Draw the rectangle on large_image
cv2.rectangle(large_image, (MPx, MPy), (MPx+tcols, MPy+trows), (0, 0, 255), 2)
# cv2.putText(large_image, maxVal, (100, 200), "Microsoft JhengHei",
#             2.5, (255, 255, 255), 2, cv2.LINE_AA)

# Display the original image with the rectangle around the match.
cv2.imshow('output', large_image)

# The image is only displayed if we call this
cv2.waitKey(0)

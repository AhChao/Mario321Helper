import cv2
from imageRecognize import compareWithTargetTemplate

cap = cv2.VideoCapture("testImgs/321TestVideo.mkv")
cap.set(cv2.CAP_PROP_POS_FRAMES, 240*60)
fps = int(cap.get(cv2.CAP_PROP_FPS))
save_interval = 0.4
frame_count = 0

while cap.isOpened:
    ret, frame = cap.read()
    frame_count += 1
    cv2.imshow('frame', frame)

    # Compare Per 0.5 seconds
    if frame_count % (fps * save_interval) == 0:
        # Compare with 321 template
        compareWithTargetTemplate(
            "./sampleImgs/321Mapping.png", cv2.convertScaleAbs(frame), 0.55)  # 2 count then plus 1
        compareWithTargetTemplate(
            "./sampleImgs/courseClearMapping.png", cv2.convertScaleAbs(frame), 0.1)  # cd for 5 seconds
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

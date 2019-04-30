import cv2
import dlib

model_detector = dlib.simple_object_detector("tld.svm")

cam=cv2.VideoCapture(0)

while (1):
    ret,frame=cam.read()

    boxes = model_detector(frame)
    for box in boxes:
        print (box)
        (x, y, xb, yb) = [box.left(), box.top(), box.right(), box.bottom()]
        cv2.rectangle(frame, (x, y), (xb, yb), (0, 0, 255), 2)

    cv2.imshow("Frame",frame)

    key = cv2.waitKey(1)
    if cv2.waitKey(1)==ord('q'):
        break

cv2.destroyAllWindows()
cam.release()
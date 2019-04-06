import sys
import cv2
import numpy as np
if __name__ == '__main__':
    def nothing(*arg):
        pass
cv2.namedWindow( "result" ) 
cv2.namedWindow( "settings" ) 
img = cv2.imread("roof.png")
cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
cv2.createTrackbar('v1', 'settings', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings', 255, 255, nothing)
cv2.createTrackbar('s2', 'settings', 255, 255, nothing)
cv2.createTrackbar('v2', 'settings', 255, 255, nothing)
crange = [0,0,0, 0,0,0]
while True:
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h1 = cv2.getTrackbarPos('h1', 'settings')
    s1 = cv2.getTrackbarPos('s1', 'settings')
    v1 = cv2.getTrackbarPos('v1', 'settings')
    h2 = cv2.getTrackbarPos('h2', 'settings')
    s2 = cv2.getTrackbarPos('s2', 'settings')
    v2 = cv2.getTrackbarPos('v2', 'settings')
    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)
    thresh = cv2.inRange(hsv, h_min, h_max)
    cv2.imshow('result', thresh) 
     ch = cv2.waitKey(5)
    if ch == 27:
        break
print(type(img))
cap.release()
cv2.destroyAllWindows()

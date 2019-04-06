import cv2
import numpy as np
if __name__ == '__main__':
   def callback(*arg):
       pass
cv2.namedWindow( "result" ) 
cv2.namedWindow( "result1" )
img = cv2.imread("roof.png")
#red
#2green
#3circule
hsv_min1 = np.array((0, 62, 170), np.uint8) 
hsv_max1 = np.array((255, 124, 239), np.uint8)
hsv1 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
thresh = cv2.inRange(hsv1, hsv_min1, hsv_max1)
st1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3), (1,1))
#st2 = cv2.getStructuringElement(cv2.MORPH_RECT, (11,11), (5,5))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, st1)
#thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, st2)
contour1, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(img, contour1, -1, (0, 255, 0), 2)
contour=[]
if contour1:
    for cnt in contour1:
        moment = cv2.moments(cnt, 1)
        dm01 = moment['m01'] 
        dm10 = moment['m10'] 
        darea = moment['m00'] 
        if darea >= 900:
            x = int(dm10/darea)
            y = int(dm01/darea)
            contour.append(cnt)
            # cv2.circle(img, (x, y), 5, (0, 0, 255), 2)
            # cv2.putText(img, 'x: '+str(x)+'  '+'y: '+str(y), (x+10, y+10), 
            # cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
cv2.drawContours(img, contour, -1, (0, 255, 0), 2)
print(len(contour))
while True:
    cv2.imshow('result', img) 
    cv2.imshow('result1', thresh)
    ch = cv2.waitKey(5)
    if ch == 27:
        break
    cv2.destroyAllWindows()


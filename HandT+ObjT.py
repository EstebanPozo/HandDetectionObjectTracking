import cv2
import time
import HandTrackingModule as htm
import math

##########PARAMETERS################
wCam, hcam = 640, 480  # adjusts the size of the frame
####################################

# Basic setup for running a webcam
cap = cv2.VideoCapture(0)  # 0  for webcam 2 for Intel CAM
cap.set(3, wCam)  # prompt ID at 3 is wCam
cap.set(4, hcam)
pTime = 0
detector = htm.handDetector(detectionCon=0.7)


#tracker = cv2.legacy_TrackerMOSSE.create()#https://docs.opencv.org/4.5.1/javadoc/org/opencv/tracking/legacy_TrackerMOSSE.html
tracker = cv2.TrackerCSRT_create()
success, img = cap.read()
bbox = cv2.selectROI(" ", img, False)
tracker.init(img,bbox)

def drawBox(img,bbox): # Rectangular region of interest ROI
    x,y,w,h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    #x, y, w, h = 50,200,100,100
    cv2.rectangle(img,(x,y),((x+w),(y+h)), (255,0,255), 3,1)
    cv2.putText(img, "", (75, 75), cv2.FONT_HERSHEY_PLAIN, 0.7, (255, 0, 0), 2)


#
while True:

    success, img = cap.read()  # this will enable the frame
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[8], lmList[12])
        #x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        #x1, y1 = lmList[12][1], lmList[12][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        # cx,cy = (x1+x2)//2,(y1+y2)//2
        #cv2.circle(img, (0, 0), 10, (0, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (0, 0, 0), cv2.FILLED)
        cv2.line(img, (0, 0), (x2, y2), (255, 0, 0), 3)
        #cv2.line(img, (xb, yb), (x2, y2), (255, 0, 0), 3)
        #cv2.line(img, ((x+w),(y+h)), (x2, y2), (255, 0, 0), 3)

        #length = math.hypot(x2 , y2 )
        length = ((bbox[0] - x2)**2+(bbox[1] - y2)**2)**0.5
        print(length)
        if length <= 400:
            print('stop')
            cv2.putText(img, f'Signal: {int(1)}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0),
                        2)
        else:
            print('go')
            cv2.putText(img, f'Signal: {int(0)}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0),
                        2)

            # write a frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)  # current time step - previous time step
    pTime = cTime

    # add fps Tag to image so it gets displayed in real time
    #cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0),
        #        2)  # Syntax: cv2.putText(image, text, org, font, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]]) - https://www.geeksforgeeks.org/python-opencv-cv2-puttext-method/
    ##
    timer = cv2.getTickCount()

    success, img = cap.read()
    success, bbox = tracker.update(img)
    print(bbox)

    if success:
        drawBox(img, bbox)
    else:
        cv2.putText(img, "Lost", (75, 75), cv2.FONT_HERSHEY_PLAIN, 0.7, (255, 0, 0), 2)

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    cv2.putText(img, str(int(fps)), (40, 50), cv2.FONT_HERSHEY_PLAIN, 0.7, (255, 0, 0), 2)
    cv2.imshow("", img)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    ###
    #cv2.imshow("Image", img)
    cv2.waitKey(1)


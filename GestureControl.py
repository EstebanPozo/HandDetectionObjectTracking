import cv2
import time
import HandTrackingModule as htm
import math

##########PARAMETERS################
wCam, hcam = 640, 480 #adjusts the size of the frame
####################################

# Basic setup for running a webcam
cap = cv2.VideoCapture(0) # 0  for webcam
cap.set(3,wCam) #prompt ID at 3 is wCam
cap.set(4,hcam)
pTime=0
detector = htm.handDetector(maxHands=1, detectionCon=0.7)



while True:
    success, img = cap.read() # this will enable the frame
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        #print(lmList[8], lmList[12])

        x1,y1 = lmList[12][1], lmList[12][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        #cx,cy = (x1+x2)//2,(y1+y2)//2
        cv2.circle(img, (x1,y1), 10, (0, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (0, 0, 0), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,0),3)

        length = math.hypot(x2 - x1, y2 - y1)
        print(length)
        if length <= 30:
            print('closed')
        else:
         print('open')


    #write a frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)# current time step - previous time step
    pTime = cTime

    #add fps Tag to image so it gets displayed in real time
    cv2.putText(img,f'FPS: {int(fps)}',(40,50),cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0),2) # Syntax: cv2.putText(image, text, org, font, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]]) - https://www.geeksforgeeks.org/python-opencv-cv2-puttext-method/

    cv2.imshow("Image", img)
    cv2.waitKey(1)



import cv2
import time
import HandTrackingModule as htm
import math
from pyModbusTCP.client import ModbusClient



##########PARAMETERS################
wCam, hcam = 640, 480 #adjusts the size of the frame
####################################

# Basic setup for running a webcam
cap = cv2.VideoCapture(0) # 0  for webcam
cap.set(3,wCam) #prompt ID at 3 is wCam
cap.set(4,hcam)
pTime=0
detector = htm.handDetector(maxHands=1, detectionCon=0.7)
a=0


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
            cv2.putText(img, f'Signal: {int(1)}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0),
                        2)
            a = 1
            print(a)
        else:
            
         print('open')
         cv2.putText(img, f'Signal: {int(0)}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0),
                     2)
         a = 0
         # write a frame rate
         print(a)


    #write a frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)# current time step - previous time step
    pTime = cTime

    PLC= ModbusClient(host="194.94.86.33", port=502, auto_open=True)
  
      
    Dis1 = a
    Dis2 = 35

    #Holding Register 1
    holding_register_value_1 = Dis1
    print(Dis1)

    #Holding Register 2
    holding_register_value_2 = Dis2
    print(Dis2)

    PLC.write_single_register(0,(holding_register_value_1))
    PLC.write_single_register(1,(holding_register_value_2))

    #print(Feedback)
    PLC.close()

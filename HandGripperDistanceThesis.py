import cv2
import time
import HandTrackingModule as htm
import math

import easymodbus.modbusClient


import easymodbus as em

##########PARAMETERS################
wCam, hcam = 640, 480  # adjusts the size of the frame
####################################

# Basic setup for running a webcam
cap = cv2.VideoCapture(1)  # 0  for webcam
cap.set(3, wCam)  # prompt ID at 3 is wCam
cap.set(4, hcam)
pTime = 0
detector = htm.handDetector(detectionCon=0.7)
a=0


while True:

    success, img = cap.read()  # this will enable the frame

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[8], lmList[12])

        #x1, y1 = lmList[12][1], lmList[12][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        # cx,cy = (x1+x2)//2,(y1+y2)//2
        cv2.circle(img, (0, 0), 10, (0, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (0, 0, 0), cv2.FILLED)
        cv2.line(img, (0, 0), (x2, y2), (255, 0, 0), 3)

        length = math.hypot(x2 , y2 )
        print(length)
        if length <= 200:
            #print('too close!')
            print('1')
            cv2.putText(img, f'Signal: {int(1)}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0),
                        2)
            a=1
            print(a)
        else:
            #print('ok')
            print('0')
            cv2.putText(img, f'Signal: {int(0)}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0),
                        2)
            a = 0
            # write a frame rate
            print(a)
    cTime = time.time()
    fps = 1 / (cTime - pTime)  # current time step - previous time step
    pTime = cTime

    # add fps Tag to image so it gets displayed in real time
    #cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0),
        #        2)  # Syntax: cv2.putText(image, text, org, font, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]]) - https://www.geeksforgeeks.org/python-opencv-cv2-puttext-method/
    ##
    #modbus_client = easymodbus.modbusClient.ModbusClient("194.94.28.231", 502)
    #modbus_client = easymodbus.modbusClient.ModbusClient("194.94.86.6", 502)
    modbus_client = easymodbus.modbusClient.ModbusClient("127.0.0.1", 8100)
    modbus_client.connect()

    register_values = modbus_client.read_holdingregisters(0, 3)
    ###
    cv2.imshow("Image", img)

    print("Val" + str(register_values[0]))
    print("Val1" + str(register_values[1]))
    print("Val2" + str(register_values[2]))

    holding_registers_value = a
    holding_registers_value1 = 1
    holding_registers_value2 = 3

    modbus_client.write_single_register(0, holding_registers_value)
    modbus_client.write_single_register(1, holding_registers_value1)
    modbus_client.write_single_register(2, holding_registers_value2)

    print("Val" + str(register_values[0]))
    print("Val1" + str(register_values[1]))
    print("Val2" + str(register_values[2]))
    modbus_client.close()

    cv2.waitKey(1)


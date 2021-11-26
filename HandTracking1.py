#Hand Tracking 30 FPS using CPU | OpenCV Python (2021) | Computer Vision
#taken from https://www.youtube.com/watch?v=NZde8Xt78Iw&t=2630s

import cv2
import mediapipe as mp
import time

# Basic setup for running a webcam
cap = cv2.VideoCapture(2) # 0  for webcam

mpHands = mp.solutions.hands

#Hands() - (self, static_image_mode=False, If it is set as static (True) it will only detect and never track
# max_num_hands=2,
# min_detection_confidence=0.5,
# min_tracking_confidence=0.5): if confidence level drops below 50%, it will switch to detection again
hands = mpHands.Hands() #ctrl+click to see Hands function's syntax

#function to draw lines between the points in the hand
mpDraw = mp.solutions.drawing_utils

pTime=0 #previous Time
pTime=0 #current Time

while True:
    success, img = cap.read() # this will enable the frame

    #send RGB image to object, because hands object only uses RGB images
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB) #the method called process, will process the frame and give the result

    #if we would like to test if the camera is tracking, we can carry out a routine without displaying the objects by using>
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            #routine to link index number (each point in the hand) with the proportional ratio of the image
            for id, lm in enumerate(handLms.landmark):
                #print(id,lm)
                #ratio values must be multiplied with width and height in order to determine the pixel value
                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                #ids must be added to determine which point is paired with each coordinate.
                print(id,cx,cy)
                #highlighting a determined id
                if id==4:
                    cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)

            #get the information from each hand. get the ID number and the landmark information
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS) # handLms represent the points
    #time step definition
    cTime = time.time()
    fps = 1/(cTime-pTime)# current time step - previous time step
    pTime = cTime
    #time step display
    cv2.putText(img,f'FPS: {int(fps)}',(40,50),cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0),2)
    # Syntax: cv2.putText(image, text, org, font, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]]) - https://www.geeksforgeeks.org/python-opencv-cv2-puttext-method/


    cv2.imshow("Image", img)
    cv2.waitKey(1)

    cv2.imshow("Image2", img)
    cv2.waitKey(1)
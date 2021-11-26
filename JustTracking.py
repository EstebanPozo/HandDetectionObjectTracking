import cv2
cap = cv2.VideoCapture(0)  # 0  for webcam 2 for intel

#tracker = cv2.legacy_TrackerMOSSE.create() #https://docs.opencv.org/4.5.1/javadoc/org/opencv/tracking/legacy_TrackerMOSSE.html
tracker = cv2.TrackerCSRT_create()
success, img = cap.read()
bbox = cv2.selectROI("Tracking", img, False)
tracker.init(img,bbox)

def drawBox(img,bbox):
    x,y,w,h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img,(x,y),((x+w),(y+h)), (255,0,255), 3,1)
    cv2.putText(img, "Tracking", (75, 75), cv2.FONT_HERSHEY_PLAIN, 0.7, (255, 0, 0), 2)


while True:
    timer = cv2.getTickCount()

    success, img = cap.read()
    success, bbox = tracker.update(img)
    print(bbox)

    if success:
        drawBox(img,bbox)
    else:
        cv2.putText(img, "Lost", (75, 75), cv2.FONT_HERSHEY_PLAIN, 0.7, (255, 0, 0), 2)


    fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
    cv2.putText(img, str(int(fps)), (40, 50), cv2.FONT_HERSHEY_PLAIN, 0.7, (255, 0, 0), 2)
    cv2.imshow("Tracking",img)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
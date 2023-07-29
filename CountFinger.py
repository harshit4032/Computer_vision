import cv2
import mediapipe
import os
import time
import HandTrackingWorkingModule as htm
wCam,hCam = 640,480
captue = cv2.VideoCapture(0)
# captue.set(3,wCam)
# captue.set(4,hCam)
forderPath = 'handTracking/Fingers/New'
# myList = os.listdir(forderPath)
myList = ['1.jpj','2.jpg','3.jpg','4.jpg','5.jpg','6.jpg']
overLayList = []
tipId = [4,8,12,16,20 ]
for imgPath in myList:
    image = cv2.imread(f'{forderPath}/{imgPath}')
    overLayList.append(image)
print(len(overLayList))
pTime=0
detector = htm.handDetector(detectionCon=0.75)
while True:
    success,img = captue.read()
######### detecting and mapping hands
    img = detector.findHands(img)
########## getting all the landmark points of the hand
    lmList = detector.findPositions(img,draw = False)
    cv2.rectangle(img,(1130,28),(1230,82),(255,0,0),thickness = 2)        
    if len(lmList)!=0:
        fingers = []
######### For Thumb
        if lmList[tipId[0]][1]<lmList[tipId[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

######## for fingers
        for id in range(1,5):
            if lmList[tipId[id]][2]<lmList[tipId[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # print(fingers)
        totalFinger = fingers.count(1)
        cv2.putText(img,f'Fingers Count : {totalFinger}',(40,700),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255),3)
        print(totalFinger)
######## shows green box if the detection was there
        cv2.rectangle(img,(1130,30),(1180,80),(0,255,0),cv2.FILLED)
        cv2.putText(img,f'Detecting',(1100,110),cv2.FONT_HERSHEY_PLAIN,2,(0,255,255),2)
######## fingers image impose on the video
        # h,w,c =overLayList[totalFinger-1].shape
        # img[0:h,0:w] = overLayList[totalFinger-1]
    else:
        cv2.rectangle(img,(1180,30),(1230,80),(0,0,255),cv2.FILLED)        
        cv2.putText(img,f'Not Detecting',(1050,110),cv2.FONT_HERSHEY_PLAIN,2,(0,255,255),2)
    

######## fps
    cTime = time.time()
    fps  =1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS : {int(fps)}',(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow('Video',img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
captue.release
cv2.destroyAllWindows()
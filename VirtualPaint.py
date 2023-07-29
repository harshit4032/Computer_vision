import cv2
import time
import numpy as np
import os
import HandTrackingWorkingModule as htm
#########################################
brushThickness = 10
########################################
############ Blanck canvas 
blankCanvas =np.zeros((720,1280,3),np.uint8)
#########################
folder = "handTracking/Header"
myList = os.listdir(folder)
overLayList=[]
xp,yp=0,0
for imPath in myList[::-1]:
    image = cv2.imread(f'{folder}/{imPath}')
    overLayList.append(image)
header = overLayList[0]
capture = cv2.VideoCapture(0)
capture.set(3,1280)
capture.set(4,720)
detector = htm.handDetector(detectionCon=0.85)
drawColor  = (255,100,255)
while True:
    #1 import image
    success, img = capture.read()
    # flip img 
    img = cv2.flip(img,1 )
    # 2 find hand landmarks
    img  = detector.findHands(img,draw = True)
    lmList = detector.findPositions(img,draw=False)
    if len(lmList)!=0:
        # print(lmList)

        ## tip of index finger
        x1,y1 = lmList[8][1:]
        ## tip of index finger
        x2,y2 = lmList[12][1:]

        # 3 check which finger is up
        fingers =detector.fingersUp()
        print(fingers)
        # 4 if selection mode - 2 fingers are up
        if fingers[1] and fingers[2]:
            print("Selection Mode")
            xp,yp=0,0

        #### checking for the click
            if y1<125:
                if 250<x1<450:
                    header = overLayList[0]
                    drawColor  = (255,100,255)
                    brushThickness = 10

                elif 550<x1<750:
                    header = overLayList[1]
                    drawColor  = (255,0,0)
                    brushThickness = 10

                elif 800<x1<950:
                    header = overLayList[2]
                    drawColor  = (0,255,0)
                    brushThickness = 10

                elif 1050<x1<1200:
                    header = overLayList[3]
                    drawColor  = (0,0,0)
                    brushThickness = 80

            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)
            
        # 5 if drawing mode - index finger is up
        if fingers[1] and not fingers[2]:
            cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
            print("Drawing Mode")
            if xp==0 & yp==0:
                xp,yp = x1,y1
            cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
            cv2.line(blankCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)

            xp,yp = x1,y1
    imgGray = cv2.cvtColor(blankCanvas,cv2.COLOR_BGR2GRAY)
    _,img_INV = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    img_INV = cv2.cvtColor(img_INV,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,img_INV)
    img = cv2.bitwise_or(img,blankCanvas)

    
    # setting header to the img
    img[0:125,0:1280] = header
    # img =  cv2.addWeighted(img,0.5,blankCanvas,0.5,0)
    cv2.imshow('Video',img)
    # cv2.imshow('Canvas',blankCanvas)
    # cv2.imshow('VideoINV',img_INV)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
capture.release
cv2.destroyAllWindows()


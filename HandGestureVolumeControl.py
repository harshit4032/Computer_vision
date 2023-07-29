import cv2
import time
import numpy as np
import HandTrackingWorkingModule as htm
import math
import pyautogui
# from ctypes import cast, POINTER
# from comtypes import CLSCTX_ALL
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
##########################
wCam,hCam  = (640,480)
##########################
capture  = cv2.VideoCapture(0)
# capture.set(4,wCam)
# capture.set(3,hCam)
pTime=0
detector = htm.handDetector(detectionCon=0.7)


 
# devices = AudioUtilities.GetSpeakers()
# interface = devices.Activate(
#     IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
# volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(-20.0, None)


volBar= 400
volper=0
while True:
    success,img = capture.read()
    img = detector.findHands(img)
    lmList  = detector.findPositions(img,False)
    if len(lmList)!=0:
         
        x1,y1  =lmList[4][1],lmList[4][2]
        x2,y2 = lmList[8][1],lmList[8][2]
        cx,cy = (x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(x1,y1),12,(0,255,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),12,(0,255,255),cv2.FILLED)
        cv2.circle(img,(cx,cy),12,(0,255,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),3)
       

        lenght = math.hypot((x2-x1),(y2-y1))
        volBar = np.interp(lenght,[50,215],[400,150])
        volper = np.interp(lenght,[50,215],[0,100])

        print(lenght)
        if lenght<80:
            cv2.circle(img,(cx,cy),12,(0,0,255),cv2.FILLED)
            pyautogui.press('down')
            cv2.putText(img,f'Volume Down',(10,475),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)

        if lenght>200:
            cv2.circle(img,(cx,cy),12,(255,0,0),cv2.FILLED)
            pyautogui.press('up')
            cv2.putText(img,f'Volume UP',(10,475),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)


    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,255),cv2.FILLED)
    cv2.putText(img,f'{int(volper)}%',(40,450),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)


    cTime=time.time()
    fps = 1/(cTime-pTime)
    pTime= cTime
    cv2.putText(img,f'FPS : {int(fps)}',(40,70),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)
    cv2.imshow('Video',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
capture.release
cv2.destroyAllWindows() 

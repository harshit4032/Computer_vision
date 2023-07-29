import cv2
import mediapipe as mp
import time
capture =  cv2.VideoCapture(0)
mphand = mp.solutions.hands
hands = mphand.Hands()
mpDraw = mp.solutions.drawing_utils
cTime=0
pTime=0
while True:
    isTrue,frame  = capture.read()
    frameRGB  =cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results = hands.process(frameRGB)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                h,w,c = frame.shape
                cx,cy = (int(lm.x*w),int(lm.y*h))
                print(id,cx,cy)
                if id==8 :
                    cv2.circle(frame,(cx,cy),15,(255,255,0),cv2.FILLED)
                if id==4 :
                    cv2.circle(frame,(cx,cy),15,(255,255,0),cv2.FILLED)
            mpDraw.draw_landmarks(frame , handLms , mphand.HAND_CONNECTIONS)
           
            # print(handLms)
    haar_cascade = cv2.CascadeClassifier('haar_face.xml')
    face_rect = haar_cascade.detectMultiScale(gray,scaleFactor = 1.1, minNeighbors = 8)
    print(len(face_rect))
    for (x,y,w,z)  in face_rect:
        cv2.rectangle(frame,(x,y),(x+w,y+z),(0,255,0),thickness = 2)
    cTime=time.time()
    fps = 1/(cTime-pTime)
    pTime=cTime
    cv2.putText(frame,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),3)
    cv2.imshow("video",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
capture.release()
cv2.deleteAllWindows()
       


import cv2
import mediapipe as mp
import time
class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5,modelComplexity=1,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipId = [4,8,12,16,20]
    def findHands(self,image,draw=True):
        imageRGB = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image
    def findPositions(self,image, handNo=0, draw=True):
        self.lmlist = []
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(Hand.landmark):
                h,w,c = image.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                self.lmlist.append([id,cx,cy])
            if draw:
                if id==8 :
                    cv2.circle(image,(cx,cy), 15 , (255,0,255), cv2.FILLED)

        return self.lmlist
    def fingersUp(self):
        fingers = []
######### For Thumb
        if self.lmlist[self.tipId[0]][1]>self.lmlist[self.tipId[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

######## for fingers
        for id in range(1,5):
            if self.lmlist[self.tipId[id]][2]<self.lmlist[self.tipId[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
def main():
    cap = cv2.VideoCapture(0)
    tracker = handDetector()
    cTime=0
    pTime=0
    while True:
        success,img = cap.read()
        img = tracker.findHands(img)
        lmList = tracker.findPositions(img)
        if len(lmList) != 0:
            # print(lmList[4])
            fingers = tracker.fingersUp()
            print(fingers)
        cTime=time.time()
        fps = 1/(cTime-pTime)
        pTime=cTime
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),3)
        cv2.imshow("Video",img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release
    cv2.destroyAllWindows
if __name__ == "__main__":
    main()
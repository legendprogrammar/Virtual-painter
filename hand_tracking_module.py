import cv2 as cv
import mediapipe as mp
import time

from numpy import true_divide

class handdectator():
    def __init__(self,mode=False,max_hands=2,complexity=1,dectaction_confidence=0.5,track_confidence=0.5) :
        self.mode=mode
        self.max_hands=max_hands
        self.dectaction = dectaction_confidence
        self.complexity = complexity
        self.track_confidence= track_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.max_hands,self.complexity,self.dectaction,self.track_confidence)
        self.mpdraw = mp.solutions.drawing_utils
        self.tipIDS = [4,8,12,16,20]
        
    def findhand(self,frame,draw=True):
        ctime = 0
        ptime = 0
        self.img_rgb = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        self.results = self.hands.process(self.img_rgb)
        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(frame, handlms, self.mpHands.HAND_CONNECTIONS)
        
        
        ctime =time.time()
        fps = 1/(ctime-ptime)
        ptime = time.time()
        return frame
    
    def findposition(self,frame,handnum=0,draw=True):
        self.Imlist = []
        self.img_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(self.img_rgb)
        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                for id, Im in enumerate(handlms.landmark):
                    # print(id,Im)
                    h ,w ,c =frame.shape
                    cx,cy = int(Im.x*w) , int(Im.y*h)
                    # print(id,cx,cy)
                    self.Imlist.append([id,cx,cy])
                    # print(self.Imlist)
                    if draw:
                        cv.circle(frame,(cx,cy),7,(0,155,70),cv.FILLED)
        return self.Imlist

    def findfinger(self):
        fingers = []
        if self.Imlist[self.tipIDS[0]][1]>self.Imlist[self.tipIDS[0]-1][2]:
                fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1,5):
            if self.Imlist[self.tipIDS[id]][2]<self.Imlist[self.tipIDS[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers

def main():
    ctime = 0 
    ptime = 0
    print("hello")
    vid = cv.VideoCapture(0)
    dictactor  = handdectator()

    while(True):
        img ,frame= vid.read()
        ctime =time.time()
        Imlist = dictactor.findposition(frame)
        if len(Imlist)!=0:
            print(Imlist[4])
        fps = 1/(ctime-ptime)
        ptime = time.time()
        frame=dictactor.findhand(frame,draw=True)
        cv.putText(frame,str(int(fps)),(70,70),cv.FONT_HERSHEY_TRIPLEX,1.2,(0,255,0),2)

        cv.imshow('frame',frame)
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            cv.destroyAllWindows()

# After the loop release the cap object
# vid.release()
# Destroy all the windows
cv.destroyAllWindows()
# main()
# main()
if __name__ == "main":
    main()
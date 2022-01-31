import cv2 as cv
import os
import time
import numpy as np
import hand_tracking_module as htm

brushthickness = 15
eraserthickness = 40

folderPath = 'Virtual_painter/Design'
overlaylist = []
myList = os.listdir(folderPath)
print(myList)
drawcolor = (0,0,0)

xp = 0
yp = 0

for Impath in myList:
    image = cv.imread(f'{folderPath}/{Impath}')
    overlaylist.append(image)
print(len(overlaylist))
header = overlaylist[0]

imgcanvas = np.zeros((720,1280,3),np.uint8)

detector = htm.handdectator(dectaction_confidence=0.85)


cap = cv.VideoCapture(0)
cap.set(3,1279)
cap.set(4,710)

while True:
    success,img = cap.read()
    img = cv.flip(img, 1)
    # img[0:160,0:1279] = header
    #Find Hand Landmarks
    img = detector.findhand(img)
    # Imlist = detector.findposition(img,draw=False)
    Imlist = detector.findposition(img,draw=False)
    if len(Imlist)!=0:
        # print(Imlist[4])
        
        x1,y1 = Imlist[8][1:]
        x2,y2 = Imlist[12][1:]
        fingers = detector.findfinger()
        
        if fingers[1] and fingers[2]:
                xp = 0
                yp = 0
                if y1<125:
                    if 224<x1<350:
                        header = overlaylist[1]
                        drawcolor = (0,0,255)
                    elif 450<x1<550:
                        header = overlaylist[2]
                        drawcolor = (0,255,0)
                    elif 650<x1<790:
                        drawcolor=(255,255,255)
                        header = overlaylist[3]
                    elif 840<x1<940:
                        header = overlaylist[4]
                        drawcolor = (0,155,70)
                    elif 1068<x1<1200:
                        header = overlaylist[5]
                        drawcolor = (00,00,00)
                    
                    
                cv.rectangle(img,(x1,y1-15),(x2,y2+15),(drawcolor),cv.FILLED)

        if fingers[1] and fingers[2]==False:
            
            # print("painting mode")
            cv.circle(img,(x1,y1),15,(0,255,0),cv.FILLED)
            if xp==0 and yp==0:
                xp,yp = x1,y1
            if drawcolor==(0,0,0):
               cv.line(img,(xp,yp),(x1,y1),drawcolor,eraserthickness)
               cv.line(imgcanvas,(xp,yp),(x1,y1),drawcolor,eraserthickness)
            else:
                cv.line(img,(xp,yp),(x1,y1),drawcolor,brushthickness)
                cv.line(imgcanvas,(xp,yp),(x1,y1),drawcolor,brushthickness)

            xp,yp = x1,y1

    imggray = cv.cvtColor(imgcanvas,cv.COLOR_BGR2GRAY)
    _, imginv = cv.threshold(imggray,50,255,cv.THRESH_BINARY_INV)
    imginv = cv.cvtColor(imginv,cv.COLOR_GRAY2BGR)
    img = cv.bitwise_and(img,imginv)
    img = cv.bitwise_or(img,imgcanvas)

    h,w,c=overlaylist[0].shape
    img[0:h,0:w] =header
    # img = cv.addWeighted(img,0.7,imgcanvas,0.5,0)
    cv.imshow('Image',img)
    # cv.imshow('canvas',imgcanvas)
    if cv.waitKey(1) & 0xFF == ord('q'):
        cv.destroyAllWindows()
        break
import cv2
from imutils.video import FPS

# faceCascade = cv2.CascadeClassifier('faceCascade.xml')
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
fullBody = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
upperBody = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')
lowerBody = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_lowerbody.xml')

# url='http://192.168.0.17:8080/shot.jpg'

# cap = cv2.VideoCapture(url)
videoName = 'src/videos/people_bodies.mp4'
cap = cv2.VideoCapture(videoName)

# if cap.isOpened():
#     print("Cam initializatized")
# else:
#     sys.exit("Cam disconnected")

while True:

    # cap.open(videoName)
    ret, frame = cap.read()
    
    if ret: # Verificar si ha leído correctamente.
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=3)
        bodies = fullBody.detectMultiScale(gray,1.1,3)
        # upperBody = upperBody.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=5)
        # lowerBody = lowerBody.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=5)
    
    
        # for (x,y,w,h) in faces:
        #     cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

        for (x,y,w,h) in bodies:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            # cv2.imshow("body detection", frame)
        # for (x,y,w,h) in upperBody:
        #     cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        # for (x,y,w,h) in lowerBody:
        #     cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        cv2.imshow('img',frame)
        
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

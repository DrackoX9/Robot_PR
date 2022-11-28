import cv2
import sys

faceCascade = cv2.CascadeClassifier('faceCascade.xml')

url='http://192.168.0.17:8080/shot.jpg'

cap = cv2.VideoCapture(url)

if cap.isOpened():
    print("Cam initializatized")
else:
    sys.exit("Cam disconnected")
    

while True:
     
    ret, frame = cap.read()
    
    if ret: # Verificar si ha leído correctamente.
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=3)
    
    
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

        cv2.imshow('img',frame)
        
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

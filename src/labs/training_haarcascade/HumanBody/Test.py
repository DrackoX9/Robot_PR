import cv2


cascade = cv2.CascadeClassifier('cascade.xml')

url='http://192.168.0.17:8080/shot.jpg'

cap = cv2.VideoCapture(url)


while 1:
    
    cap.open(url)
    _,frame = cap.read() 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    trafficSignal = cascade.detectMultiScale(gray, 1.01,5)

    for (x,y,w,h) in trafficSignal:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)


    cv2.imshow('img',frame)
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

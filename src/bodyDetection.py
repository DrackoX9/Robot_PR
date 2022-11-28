import cv2
# from cvzone.Posemo

url='http://192.168.0.17:8080/shot.jpg'

cap = cv2.VideoCapture(url)

while True:
    cap.open(url)
    success, img = cap.read()
    cv2.imshow("Result", img)

    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break
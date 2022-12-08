import cv2

from tkinter import *

# from lineFollowerRobot import saveImg

# faceCascade = cv2.CascadeClassifier('faceCascade.xml')
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
fullBody = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
upperBody = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')
lowerBody = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_lowerbody.xml')


url='http://192.168.0.16:8080/shot.jpg'

cap = cv2.VideoCapture(url)
# videoName = 'src/videos/people_bodies.mp4'
# cap = cv2.VideoCapture(videoName)

# if cap.isOpened():
#     print("Cam initializatized")
# else:
#     sys.exit("Cam disconnected")

def faceDetection(rawImagen):
    
    isObject = False   # Verdadero si encuentra un objeto
    
    cx,cy = 0,0  #centroide (x), centroide (y)
                       
    ################# Procesamiento de la Imagen ##########
    gray = cv2.cvtColor(rawImagen, cv2.COLOR_BGR2GRAY) # Convertir a RGB a grises

    ########### Segmentación,Extracción de características,Reconocimiento ################
    faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=4) # Deteccion de objeto
    
    if len(faces):
        print('Se encontró una cara')
        for (x,y,w,h) in faces:
            cx = int(x+w/2)
            cy = int(y+h/2)
            cv2.rectangle(rawImagen,(x,y),(x+w,y+h),(77, 210, 212),2) # CELESTE
            cv2.circle(rawImagen,(cx,cy), 5, (255,255,0), -1)

def upperBodyDetection(rawImagen):
    
    isObject = False   # Verdadero si encuentra un objeto
    
    cx,cy = 0,0  #centroide (x), centroide (y)
                       
    ################# Procesamiento de la Imagen ##########
    gray = cv2.cvtColor(rawImagen, cv2.COLOR_BGR2GRAY) # Convertir a RGB a grises

    ########### Segmentación,Extracción de características,Reconocimiento ################
    upperBodies = upperBody.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=4) # Deteccion de objeto
    
    if len(upperBodies):
        print('Se encontró una parte superior de un cuerpo')
        for (x,y,w,h) in upperBodies:
            cx = int(x+w/2)
            cy = int(y+h/2)
            cv2.rectangle(rawImagen,(x,y),(x+w,y+h),(207, 94, 212),2) # ROSADO
            cv2.circle(rawImagen,(cx,cy), 5, (255,255,0), -1)

def lowerBodyDetection(rawImagen):
    
    isObject = False   # Verdadero si encuentra un objeto
    
    cx,cy = 0,0  #centroide (x), centroide (y)
                       
    ################# Procesamiento de la Imagen ##########
    gray = cv2.cvtColor(rawImagen, cv2.COLOR_BGR2GRAY) # Convertir a RGB a grises

    ########### Segmentación,Extracción de características,Reconocimiento ################
    lowerBodies = lowerBody.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=4) # Deteccion de objeto
    
    if len(lowerBodies):
        print('Se encontró una parte inferior de un cuerpo')
        for (x,y,w,h) in lowerBodies:
            cx = int(x+w/2)
            cy = int(y+h/2)
            cv2.rectangle(rawImagen,(x,y),(x+w,y+h),(85, 227, 108),2) # VERDE
            cv2.circle(rawImagen,(cx,cy), 5, (255,255,0), -1)

def fullBodyDetection(rawImagen):
    
    isObject = False   # Verdadero si encuentra un objeto
    
    cx,cy = 0,0  #centroide (x), centroide (y)
                       
    ################# Procesamiento de la Imagen ##########
    gray = cv2.cvtColor(rawImagen, cv2.COLOR_BGR2GRAY) # Convertir a RGB a grises

    ########### Segmentación,Extracción de características,Reconocimiento ################
    fullBodies = fullBody.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=4) # Deteccion de objeto
    
    if len(fullBodies):
        print('Se encontró un cuerpo completo')
        for (x,y,w,h) in fullBodies:
            cx = int(x+w/2)
            cy = int(y+h/2)
            cv2.rectangle(rawImagen,(x,y),(x+w,y+h),(217, 90, 90),2) # ROJO
            cv2.circle(rawImagen,(cx,cy), 5, (255,255,0), -1)
        

while True:

    cap.open(url)
    ret, frame = cap.read()


    
    if ret: # Verificar si ha leído correctamente.

        faceDetection(frame)
        upperBodyDetection(frame)
        lowerBodyDetection(frame)
        fullBodyDetection(frame)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=3)
        bodies = fullBody.detectMultiScale(gray,1.1,3)
        # upperBody = upperBody.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=5)
        # lowerBody = lowerBody.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=5)
    
    
        # for (x,y,w,h) in faces:
        #     cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

        # for (x,y,w,h) in bodies:

            # a = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            
            # if a.all != None:
                # saveImg()
                # print('tomar foto')
                
                 
            # a.all = None
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

############## Importar modulos #####################
from pyArduino import *

from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

import os
import cv2
import numpy as np
import sys

import time

# Modelos entrenados por defecto
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
fullBody = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
upperBody = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')
lowerBody = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_lowerbody.xml')

# URL_LINE_DETECTION = 'http://192.168.0.16:8080/shot.jpg' # JOSEPH
URL_LINE_DETECTION = 'http://192.168.0.17:8080/shot.jpg' # OMAR
URL_BODY_DETECTION = 'http://192.168.0.16:8080/shot.jpg' # OMAR

directorySelected = False
lastTimePhotoTaked = 0

def takePhoto():
    '''Toma foto cuando detecta a una persona y lo guarda en la computadora'''
    capBodyDetection.open(urlBodyDetection) # Antes de capturar el frame abrimos la url
    ret, frame = capBodyDetection.read()

    if ret:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img.thumbnail((300,300))
        tkimage = ImageTk.PhotoImage(img)
        labelLastPhoto.configure(image = tkimage)
        labelLastPhoto.image = tkimage
        cv2.imwrite(os.getcwd()+"\imagen"+str(numImage.get())+".jpg",frame)
        numImage.set(numImage.get() + 1)

def folder():
    '''Directorio en donde se guardarán las fotos tomadas'''
    global directorySelected
    directorio = filedialog.askdirectory()

    # C:\Users\SnakeHacKx\developer\Robot_PR\src\screenshots #OMAR

    if directorio != "":
        os.chdir(directorio)
        directorySelected = True
        
def drawRectangle(objectToDetect, rawImage, strokeColor, message):
    '''Dibuja el rectangulo cuando detecta el objeto especificado'''
    global directorySelected
    global lastTimePhotoTaked

    if len(objectToDetect):
        if directorySelected == True:
            # Toma la foto cuando se detecte un objeto y si el directoria ha sido seleccionado
            
            actualTime = time.time()
            timePassed = actualTime - lastTimePhotoTaked

            # Toma una foto cada x segundos o si todavia no ha tomado ninguna foto
            if timePassed >= 10.0 - ((actualTime - lastTimePhotoTaked) % 10.0) or lastTimePhotoTaked == 0:
                print("***********TOMÓ UNA FOTO ***********")
                lastTimePhotoTaked = time.time()
                takePhoto() 
            
        print(message)
        for (x, y, w, h) in objectToDetect:
            cx = int(x + w / 2)
            cy = int(y + h / 2)
            cv2.rectangle(rawImage, (x, y),(x+w, y+h), strokeColor, 2) # ROSADO
            cv2.circle(rawImage, (cx, cy), 5, (255, 255, 0), -1)

def faceDetection(rawImagen):
    '''Detecta el rostro de una persona'''                  
    ################# Procesamiento de la Imagen ##########
    gray = cv2.cvtColor(rawImagen, cv2.COLOR_BGR2GRAY) # Convertir a RGB a grises

    ########### Segmentación,Extracción de características,Reconocimiento ################
    # const int scale = 3;
    # cv2.Mat resized_frame_gray( cvRound( frame_gray.rows / scale ), cvRound( frame_gray.cols / scale ), CV_8UC1 );
    # cv2.resize( frame_gray, resized_frame_gray, resized_frame_gray.size() );
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4) # Deteccion de objeto
    drawRectangle(faces, rawImagen, (77, 210, 212), 'Se detectó la cara una persona') # CELESTE

def upperBodyDetection(rawImagen):
    '''Detecta la parte alta del cuerpo de una persona'''                  
    ################# Procesamiento de la Imagen ##########
    gray = cv2.cvtColor(rawImagen, cv2.COLOR_BGR2GRAY) # Convertir a RGB a grises

    ########### Segmentación,Extracción de características,Reconocimiento ################
    upperBodies = upperBody.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4) # Deteccion de objeto
    drawRectangle(upperBodies, rawImagen, (199, 87, 216), 'Se detectó la parte superior de una persona') # ROSADO


def lowerBodyDetection(rawImagen):
    '''Detecta la parte baja del cuerpo de una persona'''                  
    ################# Procesamiento de la Imagen ##########
    gray = cv2.cvtColor(rawImagen, cv2.COLOR_BGR2GRAY) # Convertir a RGB a grises

    ########### Segmentación,Extracción de características,Reconocimiento ################
    lowerBodies = lowerBody.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4) # Deteccion de objeto
    drawRectangle(lowerBodies, rawImagen, (85, 227, 108), 'Se detectó la parte inferior de una persona') # VERDE


def fullBodyDetection(rawImagen):
    '''Detecta el cuerpo entero de una persona'''                 
    ################# Procesamiento de la Imagen ##########
    gray = cv2.cvtColor(rawImagen, cv2.COLOR_BGR2GRAY) # Convertir a RGB a grises

    ########### Segmentación,Extracción de características,Reconocimiento ################
    fullBodies = fullBody.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4) # Deteccion de objeto
    drawRectangle(fullBodies, rawImagen, (217, 90, 90), 'Se detectó el cuerpo completo de una persona') # ROJO

def toggle():
    btn.config(text=btnVar.get())
  
def onClossing():
    # arduino.sendData([0,0])
    # arduino.close()
    root.quit()         #Salir del bucle de eventos.
    cap.release()       #Cerrar camara
    capBodyDetection.release()
    # cv2.destroyAllWindows()
    print("IP CAMS Desconectadas")
    root.destroy()      #Destruye la ventana creada  
    
def thresholdValue(int):
    umbralValue.set(slider.get())
    
def objectDetection(rawImage):
    kernel = np.ones((10,10),np.uint8)  # Nucleo
    isObject = False                    # Verdadero si encuentra un objeto
    cx,cy = 0,0                         # centroide (x), centroide (y)
    
    minArea = 500                       # Area minima para considerar que es un objeto

    ################# Procesamiento de la Imagen ################
    
    gray = cv2.cvtColor(rawImage, cv2.COLOR_BGR2GRAY)       #transformacion a escala de grises 
    t,binary = cv2.threshold(gray, umbralValue.get(), 255, cv2.THRESH_BINARY_INV) #tranformacion a threshold
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)      #transformacion de erosion seguida de dilatacion

    ################# Segmentacion de la Imagen ################
    contours,_ = cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        momentos = cv2.moments(cnt)         #calculo del centroide de los segmentos que tengan area mayor a la minima
        area = momentos['m00']
        if (area > minArea):
            cx = int(momentos['m10'] / momentos['m00'])     
            cy = int(momentos['m01'] / momentos['m00'])
            isObject = True
            
    return isObject, binary, cx, cy

    
def callback():
        ################## Adquisición de la Imagen ############
        
        cap.open(url) # Antes de capturar el frame abrimos la url
        ret, frame = cap.read() # Leer Frame

        capBodyDetection.open(urlBodyDetection)
        ret, frameBodyDetection = capBodyDetection.read()    

        if ret:
            
            uRef = 0        #valor inicial de las velocidades 
            wRef = 0

            # Llama a las funciones para detectar distintas partes de una persona
            faceDetection(frameBodyDetection)
            upperBodyDetection(frameBodyDetection)
            #lowerBodyDetection(frameBodyDetection)
            #fullBodyDetection(frameBodyDetection)
                         
            isObject,binary,cx,cy = objectDetection(frame) #comentar esto cuando se usa todo el reconocimiento
            
            cv2.circle(frame,(cx,cy),10, (0,0,255), -1)
            cv2.circle(frame,(cxd,cyd),10, (0,255,0), -1)

            if isObject:
                
                hx = frame.shape[1]/2-cx        #calculo del centro de la imagen
                hxe  = hxd-hx                   #diferencia entre el centro de la imagen y el centro de la forma 
                K = 0.0035                      #constante
                
                uRef = 0.05     # Velocidad de lineal las ruedas
                wRef = -K*hxe   #velocidad angular 

            else:
                uRef = 0
                wRef = 0

            # if btnVar.get() == 'Start':
            #     arduino.sendData([uRef,wRef])
            # else:
            #     arduino.sendData([0,0])

            

            imgBodyDetection = cv2.cvtColor(frameBodyDetection, cv2.COLOR_BGR2RGB)    
            imgBodyDetection = Image.fromarray(imgBodyDetection)
            imgBodyDetection.thumbnail((300,300))
            tkimageBD = ImageTk.PhotoImage(imgBodyDetection)
            labelBDCam.configure(image = tkimageBD)
            labelBDCam.image = tkimageBD
            
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)    
            img = Image.fromarray(img)
            img.thumbnail((300,300))
            tkimage = ImageTk.PhotoImage(img)
            label.configure(image = tkimage)
            label.image = tkimage
            
            img1 = Image.fromarray(binary)
            img1.thumbnail((300,300))
            tkimage1 = ImageTk.PhotoImage(img1) 
            label1.configure(image = tkimage1)
            label1.image = tkimage1
            
            root.after(10,callback)
        else:
            onClossing()
            
########################### Ip Cam ###########################

# Camara de deteccion de linea  
url = URL_LINE_DETECTION

cap = cv2.VideoCapture(url)

if cap.isOpened():
    print("Se inicializpó IP Cam correctamente (cap)")
else:
    sys.exit("IP Cam desconectada (cap)")

cap.open(url)    
ret, frame = cap.read()


# Camara de deteccion de cuerpos

urlBodyDetection = URL_BODY_DETECTION

capBodyDetection = cv2.VideoCapture(urlBodyDetection)

cap.open(url) # Antes de capturar el frame abrimos la url Leer Frame

capBodyDetection.open(urlBodyDetection) 

if capBodyDetection.isOpened():
    print("Se inicializpó IP Cam correctamente (capBodyDetection)")
else:
    sys.exit("IP Cam desconectada (capBodyDetection)")

####################### Desired position in pixels ##############

cxd = int(frame.shape[1]/2)
cyd = int(frame.shape[0]/2)

hxd = 0

########################### Serial communication ###########

# port = 'COM3'
# arduino = serialArduino(port)
# arduino.readSerialStart()

############################## HMI design #################

root = Tk()
root.protocol("WM_DELETE_WINDOW",onClossing)
root.title("Proyecto Robotica - Vision Artificial") # titulo de la ventana

# Numero de los Screeshots para el nombre en carpeta
numImage = IntVar()
numImage.set(0)

buttonDir = Button(root,text ="Carpeta Destino",command=folder) 
buttonDir.grid(row= 2, padx=20,pady=20)

label=Label(root)
label.grid(row=0,padx=20,pady=20)

label1=Label(root)
label1.grid(row= 0,column=1,padx=20,pady=20)

labelBDCam=Label(root)
labelBDCam.grid(row= 4,column=0,padx=20,pady=20)

labelLastPhoto=Label(root)
labelLastPhoto.grid(row= 4,column=1,padx=20,pady=20)

umbralValue = IntVar()
slider = Scale(root,label = 'Threshold value', from_=0, to=255, orient=HORIZONTAL,command=thresholdValue,length=400)   #Creamos un dial para recoger datos numericos
slider.grid(row = 1)

btnVar = StringVar(root, 'Pause')
btn = Checkbutton(root, text=btnVar.get(), width=12, variable=btnVar,
                  offvalue='Pause', onvalue='Start', indicator=False,
                  command=toggle)
btn.grid(row = 1,column = 1)

root.after(10,callback) # Es un método definido para todos los widgets tkinter.
root.mainloop()
############## Importar modulos #####################
from pyArduino import *

from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk #pip install pil

import os
import cv2
import numpy as np
import sys

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
fullBody = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
upperBody = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')
lowerBody = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_lowerbody.xml')

# URL_LINE_DETECTION = 'http://192.168.0.16:8080/shot.jpg' # JOSEPH
URL_LINE_DETECTION = 'http://192.168.0.17:8080/shot.jpg' # OMAR
URL_BODY_DETECTION = 'http://192.168.0.16:8080/shot.jpg' # OMAR


def takePhoto():
    '''Toma foto cuando detecta a una persona y lo guarda en la computadora'''
    capBodyDetection.open(urlBodyDetection) # Antes de capturar el frame abrimos la url
    ret, frame = capBodyDetection.read()
    if ret:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        tkimage = ImageTk.PhotoImage(img)
        label1.configure(image = tkimage)
        label1.image = tkimage
        cv2.imwrite(os.getcwd()+"\imagen"+str(numImage.get())+".jpg",frame)
        numImage.set(numImage.get()+1)

def folder():
    '''Directorio en donde se guardarán las fotos tomadas'''
    directorio = filedialog.askdirectory()
    if directorio !="":
        os.chdir(directorio)

def faceDetection(rawImagen):
    '''Detecta el rostro de una persona'''
    # isObject = False   # Verdadero si encuentra un objeto
    
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
    '''Detecta la parte alta del cuerpo de una persona'''
    # isObject = False   # Verdadero si encuentra un objeto
    
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
    '''Detecta la parte baja del cuerpo de una persona'''
    # isObject = False   # Verdadero si encuentra un objeto
    
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
    '''Detecta el cuerpo entero de una persona'''
    
    # isObject = False   # Verdadero si encuentra un objeto
    
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
    kernel = np.ones((10,10),np.uint8) # Nucleo
    isObject = False     # Verdadero si encuentra un objeto
    cx,cy = 0,0          #centroide (x), centroide (y)
    
    minArea = 500  # Area minima para considerar que es un objeto

    ################# Procesamiento de la Imagen ################
    
    gray = cv2.cvtColor(rawImage, cv2.COLOR_BGR2GRAY)
    t,binary = cv2.threshold(gray, umbralValue.get(), 255, cv2.THRESH_BINARY_INV)
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    ################# Segmentacion de la Imagen ################
    contours,_ = cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        momentos = cv2.moments(cnt)
        area = momentos['m00']
        if (area>minArea):
            cx = int(momentos['m10']/momentos['m00'])     
            cy = int(momentos['m01']/momentos['m00'])
            isObject = True
            
    return isObject,binary,cx,cy

    
def callback():

        ################## Adquisición de la Imagen ############
        
        cap.open(url) # Antes de capturar el frame abrimos la url
        ret, frame = cap.read() # Leer Frame

        capBodyDetection.open(urlBodyDetection)
        ret, frameBodyDetection = capBodyDetection.read()    
        

        if ret:
            
            uRef = 0
            wRef = 0

            # Llama a las funciones para detectar distintas partes de una persona
            faceDetection(frameBodyDetection)
            upperBodyDetection(frameBodyDetection)
            lowerBodyDetection(frameBodyDetection)
            fullBodyDetection(frameBodyDetection)
                
            
            isObject,binary,cx,cy = objectDetection(frame)
            
            cv2.circle(frame,(cx,cy),10, (0,0,255), -1)
            cv2.circle(frame,(cxd,cyd),10, (0,255,0), -1)

            if isObject:
                
                hx = frame.shape[1]/2-cx
                
                
                hxe  = hxd-hx
                

                K = 0.0035
                
                uRef = 0.05 #Velocidad de las ruedas
                wRef = -K*hxe

            else:
                uRef = 0
                wRef = 0

            # if btnVar.get() == 'Start':
            #     arduino.sendData([uRef,wRef])
            # else:
            #     arduino.sendData([0,0])

            # cv2.imshow('imgBodyDetection',frameBodyDetection)

            imgBodyDetection = cv2.cvtColor(frameBodyDetection, cv2.COLOR_BGR2RGB)    
            imgBodyDetection = Image.fromarray(imgBodyDetection)
            imgBodyDetection.thumbnail((400,400))
            tkimageBD = ImageTk.PhotoImage(imgBodyDetection)
            labelBDCam.configure(image = tkimageBD)
            labelBDCam.image = tkimageBD
            
            
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)    
            img = Image.fromarray(img)
            img.thumbnail((400,400))
            tkimage = ImageTk.PhotoImage(img)
            label.configure(image = tkimage)
            label.image = tkimage
            
            img1 = Image.fromarray(binary)
            img1.thumbnail((400,400))
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

# Camara de deteccion de cuerpoos

urlBodyDetection = URL_BODY_DETECTION

capBodyDetection = cv2.VideoCapture(urlBodyDetection)

if capBodyDetection.isOpened():
    print("Se inicializpó IP Cam correctamente (capBodyDetection)")
else:
    sys.exit("IP Cam desconenctada (capBodyDetection)")

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

umbralValue = IntVar()
slider = Scale(root,label = 'Threshold value', from_=0, to=255, orient=HORIZONTAL,command=thresholdValue,length=400)   #Creamos un dial para recoger datos numericos
slider.grid(row = 1)

btnVar = StringVar(root, 'Pause')
btn = Checkbutton(root, text=btnVar.get(), width=12, variable=btnVar,
                  offvalue='Pause', onvalue='Start', indicator=False,
                  command=toggle)
btn.grid(row = 1,column = 1)

root.after(10,callback) #Es un método definido para todos los widgets tkinter.
root.mainloop()


     

# while True:

    
    
#     if ret: # Verificar si ha leído correctamente.

#         faceDetection(frame)
#         upperBodyDetection(frame)
#         lowerBodyDetection(frame)
#         fullBodyDetection(frame)
        
#         # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         # faces = faceCascade.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=3)
#         # bodies = fullBody.detectMultiScale(gray,1.1,3)
#         # upperBody = upperBody.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=5)
#         # lowerBody = lowerBody.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=5)
    
    
#         # for (x,y,w,h) in faces:
#         #     cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

#         # for (x,y,w,h) in bodies:

#             # a = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            
#             # if a.all != None:
#                 # saveImg()
#                 # print('tomar foto')
                
                 
#             # a.all = None
#             # cv2.imshow("body detection", frame)
#         # for (x,y,w,h) in upperBody:
#         #     cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

#         # for (x,y,w,h) in lowerBody:
#         #     cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

#         cv2.imshow('img',frame)
        
#     k = cv2.waitKey(10) & 0xff
#     if k == 27:
#         break





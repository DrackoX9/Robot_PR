############## Importar modulos #####################
from pyArduino import *

from tkinter import *
from PIL import Image, ImageTk

import cv2
import numpy as np
import sys

def toggle():
    btn.config(text=btnVar.get())
    
def onClossing():
    arduino.sendData([0,0,0])   # Detener los motores
    arduino.close()             # Cerrar puerto serial
    root.quit()                 #Salir del bucle de eventos.
    cap.release()               #Cerrar camara
    print("Ip Cam Disconected")
    root.destroy()              #Destruye la ventana tkinter creada
    
def objectDetection(rawImagen):
    
    isObject = 0   # o no hay objeto, 1 giro izquierda, 2 giro derecha, 3 detener
                       
    ################# Procesamiento de la Imagen ##########
    gray = cv2.cvtColor(rawImagen, cv2.COLOR_BGR2GRAY) # Convertir a RGB a grises

    ########### Segmentación,Extracción de características,Reconocimiento ################
    left = leftCascade.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=3) # Deteccion de objeto
    right = rightCascade.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=3) # Deteccion de objeto
    stop = stopCascade.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=3) # Deteccion de objeto

    if len(stop):
        isObject = 3
        for (cx,cy,w,h) in stop:
            cv2.rectangle(rawImagen,(cx,cy),(cx+w,cy+h),(0,0,255),2)
    elif len(right):
        isObject = 2
        for (cx,cy,w,h) in right:
            cv2.rectangle(rawImagen,(cx,cy),(cx+w,cy+h),(0,255,0),2)
    elif len(left):
        isObject = 1
        for (cx,cy,w,h) in left:
            cv2.rectangle(rawImagen,(cx,cy),(cx+w,cy+h),(255,0,0),2)
    else:
        isObject = 0

    return isObject,rawImagen   
    
def callback():
    ################## Adquisición de la Imagen ############
    
    cap.open(url) # Antes de capturar el frame abrimos la url
    ret, frame = cap.read() # Leer Frame

    if ret:
        
        ulRef = 0.3

        isObject,frame = objectDetection(frame)

        if isObject==1 and btnVar.get() == 'Start': #gire a la izquierda
            arduino.sendData([0,ulRef,0])
        elif isObject==2 and btnVar.get() == 'Start':
            arduino.sendData([0,-ulRef,0]) #gire a la derecha
        else:
            arduino.sendData([0,0,0])# Detener robot
                    

        # Mostrar imagen en el HMI    
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img) 
            
        tkimage = ImageTk.PhotoImage(img)
             
        label.configure(image = tkimage )
        label.image = tkimage
            
        
        root.after(10,callback) # Llamar a callback despues de 10 ms
    else:
        onClossing()


        
# Objetos haar-cascada
leftCascade  = cv2.CascadeClassifier('left.xml')
rightCascade = cv2.CascadeClassifier('right.xml')
stopCascade  = cv2.CascadeClassifier('stop.xml')

########################### Ip Cam ###########################

url='http://192.168.0.16:8080/shot.jpg'

cap = cv2.VideoCapture(url)

if cap.isOpened():
    print("Ip Cam initializatized")
else:
    sys.exit("Ip Cam disconnected")
    
########################### Serial communication ###########

port = 'COM17' 

arduino = serialArduino(port)

arduino.readSerialStart()

############################## HMI design #################
root = Tk()
root.protocol("WM_DELETE_WINDOW",onClossing)
root.title("Vision Artificial") # titulo de la ventana
    
label=Label(root) 
label.grid(padx=20,pady=20)

btnVar = StringVar(root, 'Pause')
btn = Checkbutton(root, text=btnVar.get(), width=12, variable=btnVar,
                  offvalue='Pause', onvalue='Start', indicator=False,
                  command=toggle)

btn.grid(row = 1, padx=20,pady=20)

root.after(10,callback) # Llamar a callback despues de 10 ms
root.mainloop() #Inicia el bucle de eventos de Tkinter



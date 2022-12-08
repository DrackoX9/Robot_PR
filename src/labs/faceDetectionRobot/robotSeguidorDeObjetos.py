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
    # arduino.sendData([0,0,0])   # Detener los motores
    # arduino.close()             # Cerrar puerto serial
    root.quit()                 #Salir del bucle de eventos.
    cap.release()               #Cerrar camara
    print("Ip Cam Disconected")
    root.destroy()              #Destruye la ventana tkinter creada
    
def objectDetection(rawImagen):
    
    isObject = False   # Verdadero si encuentra un objeto
    
    cx,cy = 0,0  #centroide (x), centroide (y)
                       
    ################# Procesamiento de la Imagen ##########
    gray = cv2.cvtColor(rawImagen, cv2.COLOR_BGR2GRAY) # Convertir a RGB a grises

    ########### Segmentación,Extracción de características,Reconocimiento ################
    faces = faceCascade.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=3) # Deteccion de objeto
    
    if len(faces):
        isObject = True
        for (x,y,w,h) in faces:
            cx = int(x+w/2)
            cy = int(y+h/2)
            cv2.rectangle(rawImagen,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.circle(rawImagen,(cx,cy), 5, (255,255,0), -1)

    else:
        isObject = False
        
    return isObject,rawImagen,x,y
    
    
def callback():

     ################## Adquisición de la Imagen ############
    
     cap.open(url) # Antes de capturar el frame abrimos la url
     ret, frame = cap.read() # Leer Frame

     if ret:
         
          minDist = 30
            
          cv2.circle(frame,(int(cxd),int(cyd)), minDist, (0,255,0),3)

          isObject,frame,cx,cy = objectDetection(frame)
          
          
          if isObject:
               

               ################## Conversion coordenadas ############
               
               hxd = frame.shape[1]/2 - cxd
               hyd = frame.shape[0]/2 - cyd

               hx = frame.shape[1]/2 - cx
               hy = frame.shape[0]/2 - cy
              
               # Distancia minima de error (Distancia Euclidiana)
               distance = np.sqrt((hxd-hx)**2+(hyd-hy)**2)

               if distance>minDist:
                   
                    ################## Control cámara en mano ############
                   
                    # phi.set(arduino.rawData[0]) # Leer ángulo de orientacion del robot

                    # Errores
                    hxe  =   hxd-hx;
                    hye  =   hyd-hy;
                    phie =   phid-phi.get()

                    
                    # Vector columna 3x1 de errores
                    he = np.array([[hxe],[hye],[phie]])
                    
                    # Matriz diagonal 3x3 de ganancias
                    K = np.diag([0.002,0.002,0.005])

                    # Matriz Jacobiana
                    J = np.array([[-np.sin(phi.get()),-np.cos(phi.get()),0],
                                  [ np.cos(phi.get()),-np.sin(phi.get()),0],
                                  [ 0                ,0                 ,1]])
                    # Ley de control
                    qp = np.linalg.inv(J)@(K@he)

                    # Separar acciones de control con dos decimales de precision
                    ufRef.set(round(qp[0][0],2))
                    ulRef.set(round(qp[1][0],2))
                    wRef.set(round(qp[2][0],2))
                    
               else:
                    ufRef.set(0)
                    ulRef.set(0)
                    wRef.set(0)
          else:
              ufRef.set(0)
              ulRef.set(0)
              wRef.set(0)
               
          # Mostrar velocidades en el HMI         
          varUf.set("Linear frontal velocity : "+str(ufRef.get()))
          varUl.set("Linear lateral velocity : "+str(ulRef.get()))
          varW.set("Angular velocity : "+str(wRef.get()))
          varPhi.set("Orientation : "+str(phi.get()))

          # Boton de inicio
        #   if btnVar.get() == 'Start':
        #       arduino.sendData([ufRef.get(),ulRef.get(),wRef.get()])
                    
        #   else:
        #       arduino.sendData([0,0,0])

          # Mostrar imagen en el HMI    
          img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
          img = Image.fromarray(img)
          img.thumbnail((400,400)) 
            
          tkimage = ImageTk.PhotoImage(img)
             
          label.configure(image = tkimage )
          label.image = tkimage
            
        
          root.after(10,callback) # Llamar a callback despues de 10 ms
     else:
          onClossing()

# Objeto haar-cascada
# faceCascade = cv2.CascadeClassifier('faceCascade.xml')
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'faceCascade.xml')

########################### Ip Cam ###########################

url='http://192.168.0.16:8080/shot.jpg'

cap = cv2.VideoCapture(url)

if cap.isOpened():
    print("Ip Cam initializatized")
else:
    sys.exit("Ip Cam disconnected")
    
####################### Desired position in pixels ##############

cxd  = 340
cyd  = 150

phid = 0 # orientacion deseada siempre a 0 grados (Siempre camara al frente)

########################### Serial communication ###########

# port = 'COM17' 

# arduino = serialArduino(port)

# arduino.readSerialStart()

############################## HMI design #################
root = Tk()
root.protocol("WM_DELETE_WINDOW",onClossing)
root.title("Vision Artificial") # titulo de la ventana

label=Label(root) #image = imagen camara opencv / relief = decoracion de borde
label.grid(padx=20,pady=20)


ufRef = DoubleVar(root,0)
varUf = StringVar(root,"Linear frontal velocity : 0.00")        
labelUf = Label(root, textvariable = varUf)
labelUf.grid(row=1,column = 0,padx=20,pady=20)

ulRef = DoubleVar(root,0)
varUl = StringVar(root,"Linear lateral velocity : 0.00")        
labelUl = Label(root, textvariable = varUl)
labelUl.grid(row=2,column = 0,padx=20,pady=20)

wRef = DoubleVar(root,0)
varW = StringVar(root,"Angular velocity : 0.00")        
labelW = Label(root, textvariable = varW)
labelW.grid(row=3,column = 0,padx=20,pady=20)

phi = DoubleVar(root,0)
varPhi = StringVar(root,"Orientation : 0.00")        
labelPhi = Label(root, textvariable = varPhi)
labelPhi.grid(row=4,column = 0,padx=20,pady=20)

btnVar = StringVar(root, 'Pause')
btn = Checkbutton(root, text=btnVar.get(), width=12, variable=btnVar,
                  offvalue='Pause', onvalue='Start', indicator=False,
                  command=toggle)
btn.grid(row = 5,column = 0, padx=20,pady=20)

root.after(10,callback) # Llamar a callback despues de 10 ms
root.mainloop() #Inicia el bucle de eventos de Tkinter


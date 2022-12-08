from tkinter import filedialog
from tkinter import *
import os
from PIL import Image, ImageTk
import cv2
import time
import numpy as np
import sys


def onClossing():

    root.quit()         #finaliza este programa    
    cap.release()       #finaliza camara
    print("Camera Disconected")
    root.destroy()      #Cierra la ventana creada

def folder():
    directorio = filedialog.askdirectory()
    if directorio !="":
        os.chdir(directorio)

def saveImg():
    cap.open(url) # Antes de capturar el frame abrimos la url
    ret, frame = cap.read()
    if ret:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        tkimage = ImageTk.PhotoImage(img)
        label1.configure(image = tkimage)
        label1.image = tkimage
        cv2.imwrite(os.getcwd()+"\imagen"+str(numImagen.get())+".jpg",frame)
        numImagen.set(numImagen.get()+1)
    
def callback():
    
        cap.open(url) # Antes de capturar el frame abrimos la url
        ret, frame = cap.read()
     
        if ret:
            
            img= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convertir imágen del espacio BGR a RGB
            img = Image.fromarray(img)

            tkimage = ImageTk.PhotoImage(img)
            
            label.configure(image = tkimage )
            label.image = tkimage
            
            root.after(10,callback)
        else:
            onClossing()
        
url='http://192.168.137.187:8080/shot.jpg'
cap = cv2.VideoCapture(url)

if cap.isOpened():
    print("Ip Cam initializatized")
else:
    sys.exit("Ip Cam disconnected")

        
root = Tk()
root.protocol("WM_DELETE_WINDOW",onClossing)
root.title("Photo Capture") # titulo de la ventana

numImagen = IntVar()
numImagen.set(0) 
                     

label=Label(root) #image = imagen camara opencv / relief = decoracion de borde
label.grid(row=1,padx=20,pady=20)

label1=Label(root)
label1.grid(row= 1,column=1,padx=20,pady=20)

buttonDir = Button(root,text ="Folder",command=folder) 
buttonDir.grid(row= 2, padx=20,pady=20)

buttonSave = Button(root,text ="Save Image",command=saveImg) 
buttonSave.grid(row= 2,column = 1, padx=20,pady=20)
 
root.after(10,callback) #Es un método definido para todos los widgets tkinter.
root.mainloop()

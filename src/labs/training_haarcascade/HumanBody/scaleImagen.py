import cv2
import numpy as np
import os
import glob

path = os.getcwd()
print(path)

originalImg = "\crop"
cropImg  = "\p"

filenames = glob.glob(path+originalImg+"\*.jpg")


dim = (24,32) #(width,heigth) pixeles

numImg = 1

for filename in filenames:
    img = cv2.imread (filename)
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    cv2.imwrite(os.getcwd()+cropImg+"\scale("+str(numImg)+").jpg",resized)
    numImg = numImg+1


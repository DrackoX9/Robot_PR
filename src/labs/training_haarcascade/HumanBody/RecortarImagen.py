import cv2
import glob
import os

def click_and_crop(event, x, y, flags, param):

	global refPt, cropping

	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		cropping = True
	elif event == cv2.EVENT_LBUTTONUP:
            
		refPt.append((x, y))
		cropping = False
		cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
		cv2.imshow("image", image)

		

path = os.getcwd()
print(path)

originalImg = "\Dataset"
cropImg  = "\crop"

filenames = glob.glob(path+originalImg+"\*.jpg")

image, clone = None,None

numImg = 1

for filename in filenames:
    
    refPt = []
    cropping = False
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop)

    image = cv2.imread(filename)
    clone = image.copy()
        
    while True:
    
            cv2.imshow("image", image)
            key = cv2.waitKey(1) & 0xFF
    
            if key == ord("r"):
                    image = clone.copy()
                    refPt = []
            elif key == ord("c"):
                    break
    if len(refPt) == 2:
        roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        cv2.imshow("ROI", roi)
        cv2.imwrite(os.getcwd()+cropImg+"\crop("+str(numImg)+").jpg",roi)
    else:
        cv2.imwrite(os.getcwd()+cropImg+"\crop("+str(numImg)+").jpg",image)
        
    numImg = numImg+1
    
    cv2.waitKey(0)
    
    cv2.destroyAllWindows()


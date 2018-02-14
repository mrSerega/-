import numpy as np
import cv2

image = np.zeros((800,600))
#image = cv2.imread('C:\\Users\\User\\Desktop\\photo_2018-01-21_23-27-37.jpg')
fontFace = cv2.FONT_HERSHEY_PLAIN
fontScale = 2.0
thickness = 3
textOrg = (50, 50)
cv2.putText(image,'Hello World!', textOrg, fontFace, fontScale, 255, thickness, 9)
cv2.imshow('Hello World! Press any key...', image)
cv2.waitKey()
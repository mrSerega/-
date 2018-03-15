import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread(r"apple.jpg")
# imcopy = cv.imread(r"10.jpg")
imgcv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
# cv.imshow('image',imgcv)
cv.waitKey(0)
#cv.destroyWindow('image')

por = 100

img1 = imgcv[:,:,2]

# print(imgcv[125,164])



msk = img1 > por
print(msk[125, 164])
msk1 = np.empty(msk.shape,dtype="uint8")
for i in range(msk.shape[0]):
    for j in range(msk.shape[1]):
        if msk[i, j] == True:
            msk1[i, j] = int(1)
        else:
            msk1[i,j]= int(0)


res = cv.bitwise_and(img, img, mask = msk1)

#ret, bin_img = cv.threshold(img, por, 255, cv.THRESH_BINARY)

cv.imshow('image1', res)
cv.waitKey(0)
cv.destroyWindow('image1')
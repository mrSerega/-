import cv2
import numpy as np
from matplotlib import pyplot as plt
img =cv2.imread("moscow.jpg")
nimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(nimg)
plt.show()
img_gr = cv2.cvtColor(nimg, cv2.COLOR_BGR2GRAY)

plt.imshow(img_gr, cmap='gray')
plt.show()

hist,bins = np.histogram(img_gr.flatten(),256,[0,256])
h, w = img.shape[:2]
s = h*w
k = 0
q = 0.05
n = s*q
indB = 0
for i,v in enumerate(hist):
    k+=v
    if(k>=n):
        indB=i
        break
k = 0
indW = 0
for i, v in enumerate(reversed(hist)):
    k+=v
    if(k>=n):
        indW=i
        break
indW = len(hist)-indW
print(indB,indW)
plt.plot(hist)
plt.show()

def fun(x):
    if x < indB:
        return 0
    if x >= indW:
        return 255
    return (x - indW) * 255 / (indW - indB) + 255

newim = img_gr.copy()
for i in range(img_gr.shape[0]):
    for j in range(img_gr.shape[1]):
        newim[i,j] = fun(img_gr[i,j])

hist = cv2.calcHist([newim],[0],None,[256],[0,256])
plt.plot(hist)
plt.show()

plt.imshow(newim, cmap='gray')
plt.show()
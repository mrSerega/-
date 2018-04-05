import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys
import time

plt.ion()

r = 2  #радиус окна
image_path = 'clahe_1.jpg'   #путь до картики

img = np.array(cv2.imread(image_path,0))

clahe = cv2.createCLAHE(tileGridSize=(r,r))

#clipLimit=2.0, tileGridSize=(8,8)

height = img.shape[0]
width = img.shape[1]

print (img)

full = height*width

print ('start')

for h in range(height):
    for w in range(width):
        
        step = h*width+w
        sys.stdout.flush()
        sys.stdout.write('{} / {} % ({}/{})\r'.format(int(step/full * 100),100, step, full))

        left_up_h = h-r
        left_up_w = w-r
        right_down_h = h+r
        right_down_w = w+r
        
        if left_up_h < 0: left_up_h = 0
        if left_up_w < 0: left_up_w = 0
        if right_down_h < 0: right_down_h = 0
        if right_down_w < 0: right_down_w = 0

        if left_up_h > height-1: left_up_h = height-1
        if left_up_w > width-1: left_up_w = width-1
        if right_down_h > height-1: right_down_h = height-1
        if right_down_w > width-1: right_down_w = width-1

        # print('---')
        # print(left_up_h)
        # print(left_up_w)
        # print(right_down_h)
        # print(right_down_w)
        # time.sleep(1)

        sl = img[left_up_h:right_down_h,left_up_w:right_down_w]
        #sl = clahe.apply(sl)
        sl = cv2.equalizeHist(sl)
        img[left_up_h:right_down_h,left_up_w:right_down_w] = sl[:]

        # plt.imshow(img,cmap='gray')
        # plt.pause(0.1)

print (img)

cv2.imwrite('clahe_2.jpg',img)
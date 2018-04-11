import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys
import time

mode = 0
pic = 0

plt.ion()

r = 100  #радиус окна
if pic == 0:
    image_path = 'clahe_1.jpg'   #путь до картики
elif pic == 1:
    image_path = 'cl_1.jpg'   #путь до картики

img = np.array(cv2.imread(image_path,0))

clahe = cv2.createCLAHE( clipLimit=2.0)

#clipLimit=2.0, tileGridSize=(8,8) 0.81919

height = img.shape[0]
width = img.shape[1]

# print (img)

full = height*width

print ('start')

count = 0
step_to_show = 1
d = r

new_pic = np.zeros((height,width))

if mode == 0:
    for h in range(r,height-r, int(r/d)):
        for w in range(r,width-r, int(r/d)):
            
            count += 1

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
            sl = clahe.apply(sl)
            # sl = cv2.equalizeHist(sl)
            new_pic[left_up_h:right_down_h,left_up_w:right_down_w] = sl[:]

            # if (count % step_to_show) == 0:
            #     plt.imshow(img,cmap='gray')
            #     plt.pause(0.1)
elif mode == 1:
    sl = img[0:r,0:r]
    elem = sl[:]
    # sl = img[:]
    img1 = clahe.apply(img)
    elem_clahe = clahe.apply(sl)
    sl = clahe.apply(sl)
    img[0:r,0:r] = sl[:]
    # img[:]=sl[:]
    


print (img)

if mode == 0:
    cv2.imwrite('clahe_0.jpg',new_pic)

if mode == 1:
    cv2.imwrite('clahe_2.jpg',img)
    cv2.imwrite('clahe.jpg',img1)
    cv2.imwrite('elem_clahe.jpg',elem_clahe)
    cv2.imwrite('elem.jpg',elem)
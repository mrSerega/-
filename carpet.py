import numpy as np
import cv2
import matplotlib.pyplot as plt


image = np.zeros((256,256,3), dtype=np.uint8)

for i in range(image.shape[0]):
  for j in range(image.shape[1]):
      image[i, j, 0] = 64 * np.sin(i/16) + 128
      image[i, j, 1] = 64 * np.sin(j/32) + 128
      image[i, j, 2] = 64 * np.sin(k/64) + 128

plt.imshow(image)
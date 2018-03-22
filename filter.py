import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# Create a dummy input image.
canvas = np.zeros((100, 100), dtype=np.uint8)
#canvas = cv2.circle(canvas, (50, 50), 20, (255,), -1)
canvas = cv.imread('moscow.jpg')

plt.imshow(canvas)
plt.show()

kernel = np.array([[-0.5, 0.5]])

dst = cv.filter2D(canvas, -1, kernel)
plt.imshow(dst)
plt.show()
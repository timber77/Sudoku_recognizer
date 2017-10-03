import cv2
import numpy as np
import os

img = cv2.imread('C:/Users/Jonas Martin/Desktop/Numbers.jpg')

grayed = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(grayed,127, 255, cv2.THRESH_BINARY)

cv2.imwrite("C:/Users/Jonas Martin/Desktop/Numbersbn.jpg", thresh)

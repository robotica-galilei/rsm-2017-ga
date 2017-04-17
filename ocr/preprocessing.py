import cv2
import numpy as np

def preprocess(im):
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,80,255,cv2.THRESH_BINARY)

    kernel = np.ones((5,5), np.uint8)

    ############################# preprocessing #########################
    img = thresh
    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    return img

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

def check_rectangle(area):
    if area > 10000 and area < 85000:
        return True
    else:
        return False

def roismall(img,x,y,w,h):
    roi = img[y:y+h,x:x+w]
    roismall = cv2.resize(roi,(10,10))
    roismall = roismall.reshape((1,100))
    roismall = np.float32(roismall)
    return roismall

def check_ratio(x,y,w,h):
    ratio = float(h)/float(w)
    if(ratio > 1 and ratio < 2.8):
        return True
    else:
        return False

def ratio(x,y,w,h):
    return float(h)/float(w)

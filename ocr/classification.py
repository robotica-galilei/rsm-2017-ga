import sys
import os
import time

import numpy as np
import cv2

def classify(directory, label, samples, responses,v):
    images = os.listdir(path="./training_data/" + directory)
    for i in images:
        actual = str("./training_data/" + directory + i)
        print(actual)
        im = cv2.imread(actual)
        im3 = im.copy()


        gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(gray,90,255,cv2.THRESH_BINARY)

        kernel = np.ones((5,5), np.uint8)

        img = thresh
        img = cv2.erode(img, kernel, iterations=3)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)

        pre_processed = img.copy()

        #################      Now finding Contours         ###################

        i,contours,h = cv2.findContours(image=img,mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)

        keys = [i for i in range(48,58)]
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 22000 and area < 80000:
                if v:
                    print("AREA: %s" % (area))
                [x,y,w,h] = cv2.boundingRect(cnt)
                if  h>28:
                    cv2.rectangle(pre_processed,(x,y),(x+w,y+h),(0,0,255),2)
                    roi = pre_processed[y:y+h,x:x+w]
                    roismall = cv2.resize(roi,(10,10))
                    responses.append(label)
                    sample = roismall.reshape((1,100))
                    samples = np.append(samples,sample,0)
            elif area>5000 and area < 200000:
                if v:
                    print("UNRECOGNIZED area: %s" % (area))
                pass
    return samples, responses

if __name__=='__main__':
    if '-v' in sys.argv:
        v = True
    else:
        v = False
    labels = ['S', 'U', 'H']
    samples =  np.empty((0,100))
    responses = []

    for d in range(3):
        samples, responses = classify(labels[d] + '/', d, samples, responses,v=v)

    responses = np.array(responses,np.float32)
    responses = responses.reshape((responses.size,1))
    print ("training complete")
    np.savetxt('generalsamples.data',samples)
    np.savetxt('generalresponses.data',responses)
    cv2.destroyAllWindows()

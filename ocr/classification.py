import sys
import os

import time
import numpy as np
import cv2

import utils

def classify(directory, label, samples, responses,v):
    images = os.listdir(path="./training_data/" + directory)
    for i in images:
        actual = str("./training_data/" + directory + i)
        print(actual)
        im = cv2.imread(actual)

        img = utils.preprocess(im)

        pre_processed = img.copy()

        #################      Now finding Contours         ###################

        i,contours,h = cv2.findContours(image=img,mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)

        keys = [i for i in range(48,58)]
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if utils.check_rectangle(area):
                if v:
                    print("AREA: %s" % (area))
                [x,y,w,h] = cv2.boundingRect(cnt)
                if  utils.check_ratio(x,y,w,h):
                    cv2.rectangle(pre_processed,(x,y),(x+w,y+h),(0,0,255),2)
                    responses.append(label)
                    sample = utils.roismall(pre_processed,x,y,w,h)
                    samples = np.append(samples,sample,0)
                    if v:
                        print("Rec: %s" % directory[:1])
                elif v:
                    print("Wrong Ration %s" % utils.ratio(x,y,w,h))
            elif area>5000 and area < 200000:
                if v:
                    print("UNRECOGNIZED area: %s" % (area))

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

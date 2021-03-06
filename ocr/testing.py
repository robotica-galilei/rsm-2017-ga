import sys

import cv2
import numpy as np

import utils

def classify(v):
    #######   training part    ###############
    samples = np.loadtxt('generalsamples.data',np.float32)
    responses = np.loadtxt('generalresponses.data',np.float32)
    responses = responses.reshape((responses.size,1))

    model = cv2.ml.KNearest_create()
    model.train(samples,cv2.ml.ROW_SAMPLE,responses)

    ############################# testing part  #########################

    cap = cv2.VideoCapture(1)
    labels = ['S', 'U', 'H']

    while(True):
        ret, im = cap.read()
        #print(str('train' + str(i)+'.jpg'))
        #im = cv2.imread(str('train/' + str(i)+'.jpg'))

        img = utils.preprocess(im)
        im2 = img.copy()

        image, contours,hierarchy = cv2.findContours(im2,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        ############################# classification #########################
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if utils.check_rectangle(area):
                [x,y,w,h] = cv2.boundingRect(cnt)
                if  utils.check_ratio(x,y,w,h):
                    cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
                    retval, results, neigh_resp, dists = model.findNearest(utils.roismall(img, x,y,w,h), k = 3)
                    string = labels[int(results[0][0])]
                    cv2.putText(im,string,(x+3,y+h+3),0,2,(255,0,0),thickness=3)

        cv2.imshow('im',im)
        #cv2.imshow('processed',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    if "-v" in sys.argv:
        v = True
    else:
        v = False

    classify(v)

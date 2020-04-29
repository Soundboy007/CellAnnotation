# Concatnates nine image segments into one large image

import cv2
import numpy as np
import os

#basepath = os.getcwd()
#finalpath = basepath + '/combineimages/'

def postprocess(basepath = "C:/Users/Anand/Desktop/Sai Anand Maringanti/combineimages/"):
    files = []
    images = []

    finalpath = basepath

    # Please replace the image names accordingly
    for entry in os.listdir(basepath):
        #print(entry)
        if ('merged_U0') in entry:
            files.append(entry)

    for a, b, c in zip(*[iter(files)]*3):

        vis = np.concatenate((cv2.imread(finalpath + a), cv2.imread(finalpath + b)), axis=1)
        vis = np.concatenate((vis, cv2.imread(finalpath + c)), axis=1)
        images.append(vis)

    for a, b, c in zip(*[iter(images)]*3):
        vis = np.concatenate((a, b), axis=0)
        vis = np.concatenate((vis, c), axis=0)


    cv2.imwrite('CombinedAllHITs.jpg', vis)

  # Main method.
if __name__ == '__main__':
    postprocess()

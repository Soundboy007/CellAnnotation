
"""
Author: Trishul Nagenalli (tn74@duke.edu)
Organization: Duke Energy Data Analytics Lab

Description:
Use this script if you want to cut up a large image before posting it online so that Turkers can annotate small portions of the image. Once you have run this script, a folder will be created inside toWeb/public/images called the name of the image you cut up without the file extension.

If you would like to process large images, follow the steps below
1. Set imageToCut as the name of the image you would like to cut and run PreprocessLargeImage.py
2. Wait for Annotations
3. Run PostprocessLargeImage.py with the specified Batch ID to concatenate all smaller images into final large image

Variable Information

imageToCut				-	Name of large image that needs to be cut. It must be located inside the folder imToCut
length					-	Sidelength (in pixels) for the images you would like to cut out
overlap 				- 	Overlap between images that get cut
"""
#==================================== Set Variables below ========================================#
imageToCut_original = 'C:/Users/Anand/Desktop/Sai Anand Maringanti/imToCut/embryo-d_lifeact_000.tif'
imageToCut_annotation = 'C:/Users/Anand/Desktop/Sai Anand Maringanti/imToCut/embryo-d_TA_000.tif'
length = 400
overlap = 100
#==================================================================================================#

import os
from imCut import cut
import cv2
from matplotlib import pyplot as plt

def preprocess(imageToCut_original, imageToCut_annotation):
    #iname1 = (imageToCut_original.split('/'))[-1].split('.')[0]
    #iname2 = (imageToCut_annotation.split('/'))[-1].split('.')[0]

    cut(imageToCut_original, length, overlap)
    cut(imageToCut_annotation, length, overlap)

    lifeact = plt.imread(imageToCut_original)
    ta = plt.imread(imageToCut_annotation)
    merged = (cv2.add(lifeact, ta))
    cv2.imwrite('C:/Users/Anand/Desktop/Sai Anand Maringanti/imToCut/merged.tif', merged[:, :, ::-1])

    cut('C:/Users/Anand/Desktop/Sai Anand Maringanti/imToCut/merged.tif', length, overlap)

if __name__ == '__main__':
    preprocess(imageToCut_original, imageToCut_annotation)


# if not os.path.exists('toWeb/public/images/merged_' + iname1):
#     cut(merged, length, overlap)

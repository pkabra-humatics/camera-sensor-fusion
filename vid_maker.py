#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 12:11:22 2021

@author: pkabra
"""

import cv2 as cv
import numpy as np
import glob


def video_maker(source_folder_path, img_ext, dest_vid_path, vid_name, vid_ext):
        img_array = []
        for filename in glob.glob(source_folder_path +'/*' + '.' + img_ext):
            img = cv.imread(filename)
            height, width, layers = img.shape
            size = (width,height)
            img_array.append(img)
         
         
        out = cv.VideoWriter(dest_vid_path + '/' + vid_name+ '.' + vid_ext ,cv.VideoWriter_fourcc(*'DIVX'), 29, size)
         
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
        return None
    
##############################################################################

def main():
    
    video_maker('/home/pkabra/Documents/calib_dataset','jpg','/home/pkabra/Documents', 'vid_6m','mp4')
    return None  

##############################################################################

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 18:08:03 2021

@author: pkabra
"""

import numpy as np
import cv2
import os


if __name__ == '__main__':

    # hard coding camera parameters obtained from calibration
    camera_matrix = cv2.UMat(np.array([[1998.15246, 0, 930.038011],
                      [0, 2001.83824, 455.698378],
                      [0, 0, 1]]))
     
    newcameramtx = cv2.UMat(np.array([[1630.51440, 0, 917.779736],
                     [0, 1631.31604, 454.389080],
                     [0, 0, 1]]))
    
    dist_coefs = cv2.UMat(np.array([[-0.501805121,  0.341780070,  0.00572374528,  0.000145274274, -0.205520504]]))


    i=0
    source = cv2.VideoCapture('/home/pkabra/Documents/videos_v2/videos_v2/video_on_38_0_0.mp4')
    dst_array = []
    while True:
        i += 1
        if isinstance(source, list):
            # glob
            if i == len(source):
                break
            img = cv2.imread(source[i])
            
        else:
            # processing video frames, one at a time
            retval, img = source.read()
            if not retval:
                break
            else:
   
                # correcting the frame
                dst = cv2.undistort(img, camera_matrix, dist_coefs, None, newcameramtx)
                dst = dst.get()
  
                height, width, layers = np.array(dst).shape
                size = (width,height)
                # appending corrected frames one by one
                dst_array.append(dst)
                
    # creating output video file object, framerate = 29.970030(maintain same framerate as input video)        
    out = cv2.VideoWriter('/home/pkabra/Documents/videos_v2/videos_v2/cal_video_on_38_0_0.mp4' ,cv2.VideoWriter_fourcc(*'DIVX'), 29.970030, size)
    
    # writing the corrected frames to the output object
    for i in range(len(dst_array)):
        out.write(dst_array[i])
    out.release()

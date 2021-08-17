#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 15:23:07 2021

@author: pkabra
"""

import numpy as np
import cv2
import os
import os.path
from os import path

if __name__ == '__main__':
# hard coding camera parameters obtained from calibration, current parameters are from every 50th frame of calib_big.mp4
# drive link for calib_big.mp4 : https://drive.google.com/file/d/1aChxXT8hb079eVEwFcDuQDlDkHjV72GW/view?usp=sharing
    camera_matrix = cv2.UMat(np.array([
                      [2000.98323, 0, 924.558794],
                      [0, 2004.29646, 462.122541],
                      [0, 0, 1]]))
     
    newcameramtx = cv2.UMat(np.array([
                     [1637.37048, 0, 911.321429],
                     [0, 1634.49756, 460.785059],
                     [0, 0, 1]]))
    
    dist_coefs = cv2.UMat(np.array([[-0.491911364,  0.301216930,  0.00510246566,  0.000360248373, -0.156562794]]))
    
    input_path = "/home/pkabra/Documents/videos_hz_5min/orig/"
    output_path = "/home/pkabra/Documents/videos_hz_5min/cal/"
    
    # for every file in input path
    for file in os.listdir(input_path):
        if file.endswith(".mp4"):
            path=os.path.join(input_path, file)

            filename, _ = os.path.splitext(file)
            
            # continue with the loop, if corrected video exists in output path
            if (os.path.isfile(output_path + filename + '.mp4')):
                continue
            
            i=0
            
            source = cv2.VideoCapture(path)
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
            out = cv2.VideoWriter('/home/pkabra/Documents/videos_hz_5min/cal/'+filename+'.mp4' ,cv2.VideoWriter_fourcc(*'DIVX'), 29.970030, size)
             
            # writing the corrected frames to the output object
            for i in range(len(dst_array)):
                out.write(dst_array[i])
            out.release()
        

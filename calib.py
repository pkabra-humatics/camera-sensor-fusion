# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# Outputs camera matrix, distortion coefficients, rms error, roi to crop black border in the image

#!/usr/bin/env python
import numpy as np
import cv2
import os
import argparse
import yaml
import pickle
from glob import glob

if __name__ == '__main__':
    # see comments for description, other arguments are optional, but still could be explored if useful like: 
    # path to directory where calibration files will be saved, output corners file etc.
    
    parser = argparse.ArgumentParser(description='Calibrate camera using a video of a chessboard or a sequence of images.')
    parser.add_argument('input',nargs="?", help='input video file or glob mask')
    parser.add_argument('out',nargs="?",help='output calibration yaml file')
    parser.add_argument('--debug_dir',nargs="?", help='path to directory where images with detected chessboard will be written', 
                        default='/media/pkabra/UBUNTU 20_0/Pooja/draw_pattern')                                       # enter path to directory where images with 
                                                                                                                      # detected chessboard will be written, optional
    parser.add_argument('--output_dir',nargs="?",help='path to directory where calibration files will be saved.',default='./calibrationFiles')
    parser.add_argument('-c', '--corners',nargs="?", help='output corners file', default=None)
    parser.add_argument('-fs', '--framestep',nargs="?", help='use every nth frame in the video', default=50, type=int) # use every nth frame in the video
    parser.add_argument('--height',nargs="?", help='Height in pixels of the image',default=1080,type=int)          # we are using a video for calibration, 
    parser.add_argument('--width',nargs="?", help='Width in pixels of the image',default=1920,type=int)            # so use video dimension
    parser.add_argument('--mm',nargs="?",help='Size in mm of each square.',default=125,type=int)  # size of square in the printed calibration target in mm
    # parser.add_argument('--figure', help='saved visualization name', default=None)
    args = parser.parse_args()
    
    source = cv2.VideoCapture('/media/pkabra/UBUNTU 20_0/Pooja/calib_big.mp4') # path of the video



    # square_size = float(args.get('--square_size', 1.0))
    
    pattern_size = (13, 8) # enter grid dimensions here, consider only the corners for inner squares in the checkerboard
    pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
    pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
    # pattern_points *= square_size

    obj_points = []
    img_points = []
    h, w = args.height, args.width
    i = -1
    image_count=0
    # image_goal=500             # minimum no. of frames to be used, currently not used, to use uncomment this line with line 82, 83, 84
    while True:
        i += 1
        # if video exists
        if isinstance(source, list):
            # glob
            if i == len(source):
                break
            img = cv2.imread(source[i])
        else:
            # cv2.VideoCapture
            retval, img = source.read()
            if not retval:
                break
            if i % args.framestep != 0:
                continue

        # looking for grid in the frame
        print('Searching for chessboard in frame ' + str(i) + '...'),
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = img.shape[:2]
        found, corners = cv2.findChessboardCorners(img, pattern_size, flags=cv2.CALIB_CB_FILTER_QUADS) # returns corners if chessboard found
        
        if not found: 
            print('not found')
            continue # go on to the next frame in the video
        
        if found:
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, args.mm, 0.1)
            cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)
#            image_count=image_count+1
#            if image_count==image_goal:
#                break

        # script will ask for user approval (control comes here only if script approves the grid)
        if args.debug_dir:
            img_chess = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            cv2.drawChessboardCorners(img_chess, pattern_size, corners, found)     # draw grid on the frame
            cv2.imwrite(os.path.join(args.debug_dir, '%04d.png' % i), img_chess)   # save the frame           
            cv2.imshow('drawChessboardCorners',img_chess)                          # show the frame
            
            key = cv2.waitKey(2) & 0xFF                                            # waiting for 2 sec for user to approve the detected grid, press y/n
            
            if key == ord('y'):                                                    # if y
                image_count=image_count+1
                if image_count==image_goal:
                    break
                    
                img_points.append(corners.reshape(1, -1, 2))                      # img_points are detected corner points (changes with frame) in image plane 2D
        
                obj_points.append(pattern_points.reshape(1, -1, 3))               # obj_points are pattern points in world coordinate sys 3D
                                                                                  # they are always the same, because world coordinate sys is stuck on the 
                                                                                  # chessboard. Even if chessboard orientation is different, the points will
                                                                                  # have same values.
                print('ok')
                continue
                
            elif key == ord('n'):                                                 # if n
                print('rejected')
                continue
            else:                                                                 # timeout
                print('missed')


    if args.corners:
        with open(args.corners, 'wb') as fw:
            pickle.dump(img_points, fw)
            pickle.dump(obj_points, fw)
            pickle.dump((w, h), fw)
        

    print('\nPerforming calibration...')
    rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h), None, None) # find camera params and transformation vectors
                                                                                                                   # from world coordinate sys to image plane
    

    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coefs, (w,h), 1, (w,h))
    
    print("RMS:", rms)
    print("camera matrix:\n", camera_matrix)
    print("new camera matrix:\n", newcameramtx) 
    print("distortion coefficients: ", dist_coefs)
#    print("rvecs: ", rvecs)
#    print("tvecs: ", tvecs)


#    calibration = {'rms': rms, 'camera_matrix': camera_matrix.tolist(), 'dist_coefs': dist_coefs.tolist() }
#
#    ##OUTPUT DIRECTORIES
#    file1 = args.output_dir + "/cameraMatrix.txt"
#    np.savetxt(file1,camera_matrix,delimiter=',')
#    file2 = args.output_dir + "/cameraDistortion.txt"
#    np.savetxt(file2,dist_coefs,delimiter=',')

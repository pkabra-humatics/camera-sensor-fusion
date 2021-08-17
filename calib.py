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
    parser = argparse.ArgumentParser(description='Calibrate camera using a video of a chessboard or a sequence of images.')
    parser.add_argument('input',nargs="?", help='input video file or glob mask')
    parser.add_argument('out',nargs="?",help='output calibration yaml file')
    parser.add_argument('--debug_dir',nargs="?", help='path to directory where images with detected chessboard will be written',
                        default='/media/pkabra/UBUNTU 20_0/Pooja/draw_pattern')
    parser.add_argument('--output_dir',nargs="?",help='path to directory where calibration files will be saved.',default='./calibrationFiles')
    parser.add_argument('-c', '--corners',nargs="?", help='output corners file', default=None)
    parser.add_argument('-fs', '--framestep',nargs="?", help='use every nth frame in the video', default=50, type=int)
    parser.add_argument('--height',nargs="?", help='Height in pixels of the image',default=1080,type=int)
    parser.add_argument('--width',nargs="?", help='Width in pixels of the image',default=1920,type=int)
    parser.add_argument('--mm',nargs="?",help='Size in mm of each square.',default=125,type=int)
    # parser.add_argument('--figure', help='saved visualization name', default=None)
    args = parser.parse_args()
    source = cv2.VideoCapture('/media/pkabra/UBUNTU 20_0/Pooja/calib_big.mp4')



    # square_size = float(args.get('--square_size', 1.0))
    
    pattern_size = (13, 8)
    pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
    pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
    # pattern_points *= square_size

    obj_points = []
    img_points = []
    h, w = args.height, args.width
    i = -1
    image_count=0
    image_goal=500
    while True:
        i += 1
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


        print('Searching for chessboard in frame ' + str(i) + '...'),
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = img.shape[:2]
        found, corners = cv2.findChessboardCorners(img, pattern_size, flags=cv2.CALIB_CB_FILTER_QUADS)
        
        if not found:
            print('not found')
            continue
        
        if found:
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, args.mm, 0.1)
            cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)
#            image_count=image_count+1
#            if image_count==image_goal:
#                break
        if args.debug_dir:
            img_chess = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            cv2.drawChessboardCorners(img_chess, pattern_size, corners, found)
            cv2.imwrite(os.path.join(args.debug_dir, '%04d.png' % i), img_chess)
            
            cv2.imshow('drawChessboardCorners',img_chess)
            
            key = cv2.waitKey(2) & 0xFF
            
            if key == ord('y'):
                image_count=image_count+1
                if image_count==image_goal:
                    break
                img_points.append(corners.reshape(1, -1, 2))
                obj_points.append(pattern_points.reshape(1, -1, 3))
                print('ok')
                continue
                
            elif key == ord('n'): 
                print('rejected')
                continue
            else:
                print('missed')


    if args.corners:
        with open(args.corners, 'wb') as fw:
            pickle.dump(img_points, fw)
            pickle.dump(obj_points, fw)
            pickle.dump((w, h), fw)
        

    print('\nPerforming calibration...')
    rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h), None, None)
    

    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coefs, (w,h), 1, (w,h))
    
    print("RMS:", rms)
    print("camera matrix:\n", camera_matrix)
    print("new camera matrix:\n", newcameramtx)
    print("distortion coefficients: ", dist_coefs)
#    print("rvecs: ", rvecs)
#    print("tvecs: ", tvecs)
    
    # # fisheye calibration
    # rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.fisheye.calibrate(
    #     obj_points, img_points,
    #     (w, h), camera_matrix, np.array([0., 0., 0., 0.]),
    #     None, None,
    #     cv2.fisheye.CALIB_USE_INTRINSIC_GUESS, (3, 1, 1e-6))
    # print "RMS:", rms
    # print "camera matrix:\n", camera_matrix
    # print "distortion coefficients: ", dist_coefs.ravel()

    # undistort
    dst = cv2.undistort(img, camera_matrix, dist_coefs, None, newcameramtx)

#    mapx, mapy = cv2.initUndistortRectifyMap(camera_matrix, dist_coefs, None, newcameramtx, (w1,h1), 5)
#    dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

    # crop the image
    x, y, w, h = roi
    print('x,y,w,h=',x,y,w,h)
    dst = dst[y:y+h, x:x+w]



#    calibration = {'rms': rms, 'camera_matrix': camera_matrix.tolist(), 'dist_coefs': dist_coefs.tolist() }
#
#    ##OUTPUT DIRECTORIES
#    file1 = args.output_dir + "/cameraMatrix.txt"
#    np.savetxt(file1,camera_matrix,delimiter=',')
#    file2 = args.output_dir + "/cameraDistortion.txt"
#    np.savetxt(file2,dist_coefs,delimiter=',')
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 16:34:03 2021

@author: pkabra
"""

# importing the module
import cv2
   
# function to display the coordinates of
# of the points clicked on the image 
def click_event(event, x, y, flags, params):
  
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
  
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
  
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
                    str(y), (x,y), font,
                    1, (255, 0, 0), 2)
        cv2.imshow('image', img)
  
    # checking for right mouse clicks     
    if event==cv2.EVENT_RBUTTONDOWN:
  
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
  
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        cv2.putText(img, str(b) + ',' +
                    str(g) + ',' + str(r),
                    (x,y), font, 1,
                    (255, 255, 0), 2)
        cv2.imshow('image', img)
  
# driver function
if __name__=="__main__":
  
    
    i=0
    # video
    source = cv2.VideoCapture('/home/pkabra/Desktop/find_center/repl/cal/video_on_ss1_hz_10_9_40.mp4')

    while i==0:
        i += 1
        if isinstance(source, list): 
            img = cv2.imread(source[i])

        else:
            # cv2.VideoCapture
            retval, img = source.read()
            if not retval:
                break
            else:
		# first frame of video
                cv2.imwrite('test.png', img)
    # reading the image
    # img = cv2.imread('/home/pkabra/Documents/image.png')
  
    # displaying the image
    cv2.imshow('image', img)
  
    # setting mouse hadler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('image', click_event)
  
    # wait for a key to be pressed to exit
    cv2.waitKey(0)
  
    # close the window
    cv2.destroyAllWindows()

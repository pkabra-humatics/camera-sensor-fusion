# this file can be used to correct wrongly named video files

import os

import math

# wrong function, used to record all the data 
def rad2deg(radians):
    totalSeconds = int(round(radians * 180 * 3600 / (math.pi)))
    seconds = totalSeconds % 60
    minutes = int(round(totalSeconds / 60))%60 # changed
    degrees = int(round(totalSeconds / 3600))  # changed
    return (degrees,minutes,seconds)

# right function 
def rad2deg_(radians):
    totalSeconds = int(round(radians * 180 * 3600 / (math.pi)))
    seconds = totalSeconds % 60
    minutes = int(math.floor(totalSeconds / 60))%60
    degrees = int(math.floor(totalSeconds / 3600))
    return (degrees,minutes,seconds)

delta = 0.0015029223920 # 5 min 10 sec

counts = 683 
for i in range(counts):

    print('-------------------------------------------------------------')
    print('i:',i)
    print('theta in rad', i*delta)
    print('theta in deg, min, sec:')
    degrees,minutes,seconds = rad2deg(i*delta)
    print('previously: ', degrees,minutes,seconds)
    degrees_,minutes_,seconds_ = rad2deg_(i*delta)
    print('now: ', degrees_,minutes_,seconds_)
    
    print("correcting LED on file...")
    src = "/home/pkabra/Documents/videos_hz_5min/orig/video_on_ss1_hz_{0}_{1}_{2}.mp4".format(degrees,minutes,seconds)
    dst = "/home/pkabra/Documents/videos_hz_5min/orig/video_on_ss1_hz_{0}_{1}_{2}.mp4".format(degrees_,minutes_,seconds_)
    os.rename(src, dst)

    print("correcting LED off file...")
    src = "/home/pkabra/Documents/videos_hz_5min/orig/video_off_ss1_hz_{0}_{1}_{2}.mp4".format(degrees,minutes,seconds)
    dst = "/home/pkabra/Documents/videos_hz_5min/orig/video_off_ss1_hz_{0}_{1}_{2}.mp4".format(degrees_,minutes_,seconds_)
    os.rename(src, dst)

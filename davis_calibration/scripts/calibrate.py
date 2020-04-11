#!/usr/bin/env python

import numpy as np
import matplotlib.image as mpimg
import cv2
import sys
import pickle
import os

def calibrate(directory, size):
    #This functions return the camera matrix and distortion coefficients by perfroming calibration on a set of chessboard images
    #obtaining files in directory
    cal_files = os.listdir(directory)

    #defining image and object points
    img_points = []
    obj_points = []
    objp = np.zeros((size[0]*size[1],3), np.float32)
    objp[:,:2] = np.mgrid[0:size[0], 0:size[1]].T.reshape(-1,2)

    #iterating over images in directory 
    for file in cal_files:
        
        #reading image
        if(file[-3:]=="png"):
            cal_img = mpimg.imread(directory + file)

            #converting to grayscale
            gray = cv2.cvtColor(cal_img, cv2.COLOR_RGB2GRAY)
            gray = np.uint8(gray*255)

            #obtaining corners in chessboard
            ret, corners = cv2.findChessboardCorners(gray, size)
            if (ret):
                print("2")
                img = cv2.drawChessboardCorners(cal_img, size, corners, ret)
                cv2.imshow('img',img)
                cv2.waitKey(500)

                img_points.append(corners)
                obj_points.append(objp)

    #performing calibration
    ret, cam_mtx, dist_coef, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

    return cam_mtx, dist_coef

	
def main(argvs):
    print(argvs)
    if len(argvs) > 1:
        calibrate_img_dir = argvs[1]
        
        if calibrate_img_dir[-1] != "/":
            calibrate_img_dir += "/"
    else:
        print('Please provide directory of calibration images')
        sys.exit()		
    print("ok")
    #initialize
    chess_size = (7, 9) #size of chessboard in calibration images
    mtx = np.ndarray(shape=(3,3)) #setting camera matrix as global variables
    dist = np.ndarray(shape=(1,5))  #setting distortion coefficients as global variables


    #perform calibration
    [mtx, dist] = calibrate(calibrate_img_dir, chess_size)
    print mtx
    print dist

    #save calibration parameters
    cal_mtx_dir = "cal_mtx.sav"
    cal_dist_dir = "cal_dist_dir"
    pickle.dump(mtx, open(cal_mtx_dir, 'wb'))
    pickle.dump(dist, open(cal_dist_dir, 'wb'))

if __name__ == '__main__':
    print("1")
    main(sys.argv)
    sys.exit()
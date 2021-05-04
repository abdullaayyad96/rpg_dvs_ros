#!/usr/bin/env python

import numpy as np
import matplotlib.image as mpimg
import cv2
import sys
import pickle
import os
from datetime import date

chess_size = (5, 8) #size of chessboard in calibration images

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
                img = cv2.drawChessboardCorners(cal_img, size, corners, ret)
                cv2.imshow('img',img)
                cv2.waitKey(100)

                img_points.append(corners)
                obj_points.append(objp)

    #performing calibration
    ret, cam_mtx, dist_coef, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

    return cam_mtx, dist_coef, rvecs, tvecs

	
def main(argvs):
    print(argvs)
    if len(argvs) > 1:
        calibrate_img_dir = argvs[1]
        
        if calibrate_img_dir[-1] != "/":
            calibrate_img_dir += "/"
    else:
        print('Please provide directory of calibration images')
        sys.exit()		
    #initialize

    mtx = np.ndarray(shape=(3,3)) #setting camera matrix as global variables
    dist = np.ndarray(shape=(1,5))  #setting distortion coefficients as global variables


    #perform calibration
    [mtx, dist, rvecs, tvecs] = calibrate(calibrate_img_dir, chess_size)
    print mtx
    print dist

    #save calibration parameters
    calibration_results = {"camera_matrix": mtx,
                            "distortion_coefficients": dist}
    calibration_results_dir = 'calibration_' + str(date.today()) + '.pickle'
    pickle.dump(calibration_results, open(calibration_results_dir, 'wb'))

if __name__ == '__main__':
    main(sys.argv)
    sys.exit()
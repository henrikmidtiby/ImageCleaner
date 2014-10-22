# Script for cleaning up images of hand drawn sketches.
# Author: Henrik Skov Midtiby
# Date: 2014-10-10
# Version: 0.1

import sys
sys.path.append('/opt/ros/hydro/lib/python2.7/dist-packages')
import cv2
import numpy as np

def locateFirstAndLastFalse(inputlist):
    firstIndexOfFalseValue = -1
    lastIndexOfFalseValue = -1
    for idx, elem in enumerate(inputlist.tolist()):
        if(elem is False):
            if(firstIndexOfFalseValue is -1):
                firstIndexOfFalseValue = idx
            lastIndexOfFalseValue = idx
    return (firstIndexOfFalseValue, lastIndexOfFalseValue)

def main(filename):
    kernelsize = 25
    img = cv2.imread(filename)
    kernel = np.ones((kernelsize, kernelsize), np.uint8)
    blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)
    temp = 255 - blackhat

    # Threshold image.
    grayscale = cv2.cvtColor(temp, cv2.cv.CV_RGB2GRAY)
    _, thresholded = cv2.threshold(grayscale, 220, 255, cv2.THRESH_BINARY)
    thresholdedfilename = "%s.thresholded.png" % filename
    cv2.imwrite(thresholdedfilename, thresholded)

    # Crop image
    xlow, xhigh = locateFirstAndLastFalse(np.sum(thresholded, axis=0) == thresholded.shape[0] * 255)
    ylow, yhigh = locateFirstAndLastFalse(np.sum(thresholded, axis=1) == thresholded.shape[1] * 255)
    cropped = thresholded[(ylow-2):(yhigh+2), (xlow-2):(xhigh+2)]
    croppedfilename = "%s.cropped.png" % filename
    cv2.imwrite(croppedfilename, cropped)

    # Downscale image and crop it.
    small = cv2.resize(thresholded,  (0,0), fx=0.3, fy=0.3)
    xlow, xhigh = locateFirstAndLastFalse(np.sum(small, axis=0) == small.shape[0] * 255)
    ylow, yhigh = locateFirstAndLastFalse(np.sum(small, axis=1) == small.shape[1] * 255)
    cropped = small[(ylow-2):(yhigh+2), (xlow-2):(xhigh+2)]
    croppedfilename = "%s.small.cropped.png" % filename
    cv2.imwrite(croppedfilename, cropped)


if(len(sys.argv) == 1):
    print("Program called with no input files.")
    print("Drag a file onto the program.")
    var = raw_input("Please enter something: ")

main(sys.argv[1])



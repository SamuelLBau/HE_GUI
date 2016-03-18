#!/usr/bin/python
#This file written by Eric and Jorge
import sys
import numpy as np 
from PIL import Image
import os
import glob

import Tkinter as tk

def therm_to_bmp(file_path="", min_temp = None, max_temp = None, suffix = ""):
    infile = None
    try:
        if(file_path == ""):
            file_path = getDir()
            if(not os.path.isfile(file_path)):
                #TODO LOGGER
                print("WARNING: file not valid, cannot convert new thermal image")
                print("NOTE: Failed image %s" %(file_path))
                return ""
        # open the binary file with thermal data
        length = len(file_path)
        
        extension = file_path[length-3:]
        if(extension != "ftd"):
            file_path = file_path.replace(extension,"ftd")
            
        if(not os.path.isfile(file_path)):
            #TODO LOGGER
            print("WARNING: file not valid, cannot convert new thermal image")
            print("NOTE: Failed image %s" %(file_path))
            return ""

        infile = open(file_path, "rb")
        
		
		# parse out the temperature data
        tempList = []
        data = infile.read() # read all the data
        for i in range(0, len(data), 2):
            value = (ord(data[i]) << 8) | ord(data[i+1])
            tempList.append(value)
        infile.close()

		# rescale from deg C * 100 to deg C
        floatList = [i/100. for i in tempList]

		# use min/max if specified, otherwise use min/max from image
        if(min_temp is None):
            fMin = min(floatList)
        else:
            fMin = min_temp
        if(max_temp is None):
            fMax = max(floatList)
        else:
            fMax = max_temp
        

		# max/min for 8-bit
        nMax = 255
        nMin = 0

		# do the maths for the 8-bit img
        normList = [((255/(fMax-fMin))*(x-fMin)) for x in floatList]

		# change to image format for export
        grayArr = np.array(normList)
        grayArr.resize((288, 384))
        im = Image.fromarray(np.uint8(grayArr))
        img = im.rotate(270)
        img = img.transpose(Image.FLIP_LEFT_RIGHT)

		# save wherever the original ftd file is, add suffix and bmp
        outPath = os.path.splitext(file_path)[0] + suffix + ".bmp"
        img.save(outPath)
        return outPath

    finally:
        if(not infile is None):
            infile.close()

def process_thermal_dir(dir_path):
    for therm_img in glob.glob(dir_path + '/*.ftd'):
        therm_to_bmp(therm_img)
        
def getDir(initialDir=""):
    root = tk.Tk()
    root.withdraw()
    if(initialDir != ""):
        file_path = tkFileDialog.askdirectory(initialdir=initialDir)
    else:
        file_path = tkFileDialog.askdirectory()
    root.destroy()

    return file_path
def main():
    if len(sys.argv) is not 2:
        print "Usage: process_thermal.py directory"
        sys.exit(1)

    process_thermal_dir(sys.argv[1])

if __name__ == "__main__":
    main()

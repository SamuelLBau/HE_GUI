from qgis.core import *

import Tkinter as tk
import os
import sys

#import scipy
#from scipy import ndimage
from PIL import Image, ImageTk
import gdal
from gdalconst import * 

class QGISmapFrame(tk.Frame):
    maxSize = 20000000.0 #Maximum size of each band (in bytes) currently 20,000,000

    imagePath = 0
    degreesFromNorth = 0
    xRotation = 0
    yRotation = 0
    dataset = 0
    pointList = 0
    curPoint = 0
    
    
    longBufferFactor = 0.1
    latBufferFactor = 0.1
    
    def __init__(self,master=None,tiffImagePath="",pointList=[],curPoint=[0,0]):
        tk.Frame.__init__(self,bg='#F0F0F0')
        
        
        self.initQgis()
        
        
        self.imagePath = tiffImagePath
        self.dataset = gdal.Open(self.imagePath, GA_ReadOnly)
        self.curPoint = curPoint
        self.pointList = pointList
        
        
        #self.loadAndCropData()
    def initQgis(self):
        # supply path to where is your qgis installed
        QgsApplication.setPrefixPath("C:\Program Files\QgisEssen2-14-0", True)

        # load providers
        QgsApplication.initQgis()
        
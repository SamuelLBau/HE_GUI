import Tkinter as tk
import os
import sys

#import scipy
#from scipy import ndimage
from PIL import Image, ImageTk
import gdal
from gdalconst import * 

class mapFrame(tk.Frame):
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
        self.imagePath = tiffImagePath
        self.dataset = gdal.Open(self.imagePath, GA_ReadOnly)
        self.curPoint = curPoint
        self.pointList = pointList
        
        
        self.loadAndCropData()
        
    def loadAndCropData(self):
        #This function loads data from the dataset, then crops it to fit the path
        cols = self.dataset.RasterXSize
        rows = self.dataset.RasterYSize
        bands = self.dataset.RasterCount
        driver = self.dataset.GetDriver().LongName
        geotransform = self.dataset.GetGeoTransform()
        
        #adfGeoTransform[0] /* top left x */
        #adfGeoTransform[1] /* w-e pixel resolution */
        #adfGeoTransform[2] /* rotation, 0 if image is "north up" */
        #adfGeoTransform[3] /* top left y */
        #adfGeoTransform[4] /* rotation, 0 if image is "north up" */
        #adfGeoTransform[5] /* n-s pixel resolution */ 
        
        xResolution = geotransform[1]
        yResolution = geotransform[5]
        leftEdge = geotransform[0]
        topEdge = geotransform[3]
        bottomEdge = topEdge + yResolution * rows
        rightEdge = leftEdge + xResolution * cols
        print("cols [%d] rows[%d] bands[%d] driver [%s]"%(cols,rows,bands,driver))
        print("Left edge [%f] right edge [%f] topEdge [%f] bottomEdge [%f]" %(leftEdge,rightEdge,topEdge,bottomEdge))
        if(len(self.pointList) != 0):
            [pointLeftEdge, pointRightEdge, pointTopEdge,pointBottomEdge] = self.getPointEdges()
        else:
            [pointLeftEdge, pointRightEdge, pointTopEdge,pointBottomEdge] = [leftEdge,rightEdge,topEdge,bottomEdge]
        longRange = pointRightEdge - pointLeftEdge
        latRange = pointTopEdge - pointBottomEdge
        
        longBuffer = longRange * self.longBufferFactor
        latBuffer = latRange * self.latBufferFactor
        
        newLeftEdge = max(pointLeftEdge - longBuffer,leftEdge)
        newRightEdge = min(pointRightEdge + longBuffer,rightEdge)
        newBottomEdge = max(pointBottomEdge - latBuffer,bottomEdge)
        newTopEdge = min(pointTopEdge + latBuffer,topEdge)
        
        print("longBuffer = %f, latBuffer = %f" %(longBuffer,latBuffer))
        print("NLE = %f, NRE = %f, NTE = %f, NBE = %f" %(newLeftEdge,newRightEdge,newTopEdge,newBottomEdge))
        
        newLongRange = int((newRightEdge - newLeftEdge) / xResolution)       # these are all in lat/long units
        newLatRange = int((newTopEdge - newBottomEdge) / yResolution )
        
        xOffset = int((newLeftEdge - leftEdge) / xResolution)
        yOffset = int((newTopEdge - topEdge) / yResolution);
        
        #This is xOffset
        
        bandList = []
        lineList = []
        
        i=0
        
        #This segment should decrease size of map to nicer resolution
        newGeoTransform = list(geotransform)
        #newGeoTransform[1] = 
        
        OutFormat   = "GTiff"
        OutDriver = gdal.GetDriverByName(OutFomat)
        OutDS = OutDriver.Create(OutRas,OutCols,OutRows,1,GDT_Float32 )
        
        
        print("xOffset=%d,yOffset=%d,NLOR=%f,NLAR=%f"%(xOffset,yOffset,newLongRange,newLatRange))
        while i < bands:
            band = self.dataset.GetRasterBand(i+1)
            bandtype = gdal.GetDataTypeName(band.DataType)
            lineList.append(band.ReadRaster(xOffset,yOffset,newLongRange,newLatRange,newLongRange,newLatRange))
            i=i+1
        #Line list now holds the cropped values for eah band

        temp = input("Eulalia?")
        
        
        
        
    def getPointEdges(self,):
        length = len(self.pointList)
        
        i=0
        xmin=180
        xmax = -180
        ymin=90
        ymax=-90
        while i < length:
            if(self.pointList[i][0] < xmin):
                xmin = self.pointList[i][0]
            elif(self.pointList[i][0] > xmax):
                xmax = self.pointList[i][0]
                
            if(self.pointList[i][1] < ymin):
                ymin = self.pointList[i][1]
            elif(self.pointList[i][1] > ymax):
                ymax = self.pointList[i][1]
        
            i=i+1
        return [xmin,xmax,ymin,ymax]
        
    def checkSize(self,imSize):
        newWidth = imSize[0]
        newHeight = imSize[1]
    
        if(imSize[0] > self.maxWidth):
            ratio = imSize[0] / self.maxWidth
            newWidth = self.maxWidth
            newHeight = imSize[1] / ratio
            
        if(imSize[1] > self.maxHeight):
            ratio = imSize[1] / self.maxHeight
            newHeight = self.maxHeight
            newWidth = imSize[0] / ratio
            
        imSize = [newWidth, newHeight]    
        widthRatio = imSize[0] / self.maxWidth
        heightRatio = imSize[1] / self.maxHeight
        
        #These are already maxed out at 1,
        #These calculations should not be able to make them bigger
        #Than the max values
        newWidth = imSize[0]
        newHeight = imSize[1]
        if(heightRatio > widthRatio):
            newWidth = imSize[0] / heightRatio
            newHeight = imSize[1] / heightRatio
        else:
            newWidth = imSize[0] / widthRatio
            newHeight = imSize[1] / widthRatio
            
            
        return [int(newWidth), int(newHeight)]
#!/usr/bin/env python
import Tkinter as tk
from PIL import Image, ImageTk
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'metaReaders'))

from flightImagePanel import flightImagePanel
from mapPanel import mapPanel
from metaDataPanel import metaDataPanel
from fileSelectorFrame import fileSelectorFrame

from logParser import *
from MetaFileReader import MetaFileReader
from HEdataObject import HEdataObject

from simpleDialogs import *
from tempRangeDialog import temperatureDialog

class mainFrame(tk.Frame):
    visImageFrame = 0
    irImageFrame = 0
    mapImageFrame = 0
    metaDataFrame = 0
    imageListFrame = 0
    
    image = 0;
    
    guiImagePath = ""
    defaultIRImageDir = ""
    defaultVisImagePath = ""
    defaultTiffPath = ""
    defaultMetaFile = ""
    metaFileReader = 0
    
    visSuffix = ".png"
    irSuffix = ".png"
    
    metaFilePath = defaultMetaFile
    
    def __init__(self,master):
        tk.Frame.__init__(self,master,bg='#F0F0F0')
        self.guiImagePath = os.path.dirname(os.path.realpath(__file__)) + '/res/guiImages/'
        self.defaultIRImageDir = os.path.dirname(os.path.realpath(__file__)) + "/res/sampleRun/ir/"
        self.defaultVisImageDir = os.path.dirname(os.path.realpath(__file__)) + "/res/sampleRun/vis/"
        self.defaultTiffPath = os.path.dirname(os.path.realpath(__file__)) + '/res/sampleRun/tiff/Belize-map.gif'
        self.defaultMetaFile = os.path.dirname(os.path.realpath(__file__)) + '/res/sampleRun/logs/log.txt'
    
        self.guiImagePath = self.guiImagePath.replace("\\","/")
        self.defaultIRImageDir = self.defaultIRImageDir.replace("\\","/")
        self.defaultVisImageDir = self.defaultVisImageDir.replace("\\","/")
        self.defaultTiffPath = self.defaultTiffPath.replace("\\","/")
        self.defaultMetaFile = self.defaultMetaFile.replace("\\","/")
        
        
    
        #self.metaFilePath = 
    
      #  self.guiImagePath = os.path.dirname(os.path.realpath(__file__)) + '/guiImages/'
      #  self.defaultTiffDir = os.path.dirname(os.path.realpath(__file__)) + '/defaultTiff/'
      #  self.defaultMetaFile = os.path.dirname(os.path.realpath(__file__)) + '/defaultMetaFile/log.txt'

        self.metaFileReader = MetaFileReader()

        #self.grid()
        self.placeFrames()
        self.update()
        
        self.selectNewIRImageDir(self.defaultIRImageDir)
        self.selectNewVisImageDir(self.defaultVisImageDir)
        self.selectNewMetaFile(self.defaultMetaFile)
        
        
    def placeFrames(self):
        
        
        self.visImageFrame = flightImagePanel(self, self.guiImagePath + "eagleT.jpg",
            frameTitle='Visible Image',suffix=self.visSuffix)
        self.irImageFrame = flightImagePanel(self, self.guiImagePath + "eagleBWT.jpg",
            frameTitle='Infra-red image',suffix=self.irSuffix)
        self.mapImageFrame = mapPanel(self, self.defaultTiffPath)
        self.metaDataFrame = metaDataPanel(self)
        self.imageListFrame = fileSelectorFrame(self,self.newImageSelected,self.selectNewMetaFile)
        
        self.visImageFrame.grid(row = 0, column = 0,rowspan=2,sticky='wens')
        self.irImageFrame.grid(row = 0, column = 1,rowspan=2,sticky='wens')
        self.mapImageFrame.grid(row=0,column = 2,sticky='wens')
        self.metaDataFrame.grid(row=1,column = 2,sticky='wens')
        self.imageListFrame.grid(row=0,rowspan = 2,column = 3,sticky='wens')
        
        self.visImageFrame.setupFirstButton("Select Visible image directory",self.selectNewVisImageDir)
        
        self.irImageFrame.setupFirstButton("Select infra-red image directory",self.selectNewIRImageDir)
        self.irImageFrame.setupSecondButton("Change temperature Range",self.createTempRangeDialog)
       

#    def changeImage(self):
#        programPath = os.path.dirname(__file__);
#        self.image = Image.open(imagePath)
#        photo = ImageTk.PhotoImage(self.image)
#        #try:
#        self.image = photo
#        self.canvas.create_image(1,1,image=self.image,anchor='nw')
#        self.update()

        
    def newImageSelected(self,imageID):
        #This function is called by fileSelectorPanel, it updates
        #Each image panel, the metaFile and eventually the geotiff panel
        print("In main application, imageID = %s" %(imageID))
        
        self.visImageFrame.findNewImage(imageID)
        self.irImageFrame.findNewImage(imageID)
        
        #This should just be an array of strings, easy to print
        row = self.metaFileReader.getImageRow(imageID)
        dataObject = logLineParser(row)

        self.metaDataFrame.loadData(dataObject.printArray())
        #print(dataObject.printArray())
        #dataList = dataObject.printArray()
        
        #self.metaDataFrame.updateData(dataList)
    
        
        
        
#These functions are related to selecting what data to use
    def selectNewMetaFile(self,metaFile=""):
        print("new meta file: %s" %(metaFile))
        if(metaFile == ""):
            metaFile = getFile()
            
        if(not os.path.isfile(metaFile)):
            print("Selection was not a file, cannot read")
            return    
        self.metaFileReader.setNewMetaFile(metaFile)
        #imageIDList = self.metaFileReader.getColumn('imageID')
        self.imageListFrame.loadNewImages(self.metaFileReader.getColumn('imageID'))
        self.imageListFrame.setMetaFile(metaFile)
        
    def createTempRangeDialog(self):
        dialog = temperatureDialog(self,self.changeIRTempRange)
        dialog.grid()
    
    def changeIRTempRange(self,values):
        lowTemp = values[0]
        highTemp = values[1]
        print("Low temp = [%d], HighTemp = [%d]" %(lowTemp,highTemp))
        
        print("TODO: Use low and high values to edit IR image")
        
    def selectNewTiffFile(self):
        print("TODO: Make Tiff file selectable, link to a button on mapPanel")
        
    def selectNewVisImageDir(self,directory=""):
        if(directory==""):
            directory = getDir() + '/'
        
        if(not os.path.isdir(directory)):
            print("Selection was not a directory, cannot read")
            return          
        self.visImageFrame.setDir(directory)
        
    def selectNewIRImageDir(self,directory=""):
        if(directory==""):
            directory = getDir() + '/'
        
        if(not os.path.isdir(directory)):
            print("Selection was not a directory, cannot read")
            return          
        self.irImageFrame.setDir(directory)
        
    def saveProfile():
        print("TODO: Add load profile code:")
    def loadProfile():
        print("TODO: Add load profile code:")
    def quit():
        root.destroy()
        
    def quitter(self):
        root.destroy()

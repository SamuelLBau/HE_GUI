#!/usr/bin/env python
import Tkinter as tk
from PIL import Image, ImageTk
import os
import sys

from flightImagePanel import flightImagePanel
from mapPanel import mapPanel
from metaDataPanel import metaDataPanel
from fileSelectorFrame import fileSelectorFrame

from logParser import *
from MetaFileReader import MetaFileReader
from HEdataObject import HEdataObject

from dirSelectDialog import getDir

class Application(tk.Frame):
    visImageFrame = 0
    irImageFrame = 0
    mapImageFrame = 0
    metaDataFrame = 0
    imageListFrame = 0
    
    image = 0;
    
    guiImagePath = os.path.dirname(os.path.realpath(__file__)) + '/guiImages/'
    defaultTiffDir = os.path.dirname(os.path.realpath(__file__)) + '/defaultTiff/'
    defaultMetaFile = os.path.dirname(os.path.realpath(__file__)) + '/defaultMetaFile/log.txt'
    metaFileReader = 0
    
    metaFilePath = defaultMetaFile
    
    def __init__(self,master=None):
        self.guiImagePath = self.guiImagePath.replace("\\","/")
        self.defaultTiffDir = self.defaultTiffDir.replace("\\","/")
        self.defaultMetaFile = self.defaultMetaFile.replace("\\","/")
    
        #self.metaFilePath = 
    
      #  self.guiImagePath = os.path.dirname(os.path.realpath(__file__)) + '/guiImages/'
      #  self.defaultTiffDir = os.path.dirname(os.path.realpath(__file__)) + '/defaultTiff/'
      #  self.defaultMetaFile = os.path.dirname(os.path.realpath(__file__)) + '/defaultMetaFile/log.txt'
        tk.Frame.__init__(self,master,bg='#F0F0F0')

        self.metaFileReader = MetaFileReader()

        self.grid()
        self.placeFrames()
        self.update()
        
        self.selectNewMetaFile(self.defaultMetaFile)
        
        
    def placeFrames(self):
        visPanelInitImage = 'eagle.jpg'
        irPanelInitImage = 'eagleBW.jpg'
        mapPanelInitImage = self.defaultTiffDir + 'Belize-map.gif' #'canyon_grid1_ortho.tiff'
        
        
        self.visImageFrame = flightImagePanel(self, visPanelInitImage,self.guiImagePath,
            frameTitle='Visible Image',suffix=".png")
        self.irImageFrame = flightImagePanel(self, irPanelInitImage,self.guiImagePath,
            frameTitle='Infra-red image',suffix=".png")
        self.mapImageFrame = mapPanel(self, mapPanelInitImage)
        self.metaDataFrame = metaDataPanel(self)
        self.imageListFrame = fileSelectorFrame(self,self.newImageSelected,self.selectNewMetaFile)
        
        self.visImageFrame.grid(row = 0, column = 0,rowspan=2,sticky='wens')
        self.irImageFrame.grid(row = 0, column = 1,rowspan=2,sticky='wens')
        self.mapImageFrame.grid(row=0,column = 2,sticky='wens')
        self.metaDataFrame.grid(row=1,column = 2,sticky='wens')
        self.imageListFrame.grid(row=0,rowspan = 2,column = 3,sticky='wens')
        
        self.visImageFrame.setupFirstButton("Select Visible image directory",self.selectNewVisImageDir)
        
        self.irImageFrame.setupFirstButton("Select infra-red image directory",self.selectNewIRImageDir)
        self.irImageFrame.setupSecondButton("Change temperature Range",self.changeIRTempRange)
#        
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
        if(metaFile == ""):
            metaFile = getDir()
            if(not os.path.isfile(metaFile)):
                print("Selection was not a file, cannot read")
                return
        self.metaFileReader.setNewMetaFile(metaFile)
        #imageIDList = self.metaFileReader.getColumn('imageID')
        self.imageListFrame.loadNewImages(self.metaFileReader.getColumn('imageID'))
        
    def changeIRTempRange(self):
        print("TODO: Make ir image temp range editable")
        
    def selectNewTiffFile(self):
        print("TODO: Make Tiff file selectable, link to a button on mapPanel")
        
    def selectNewVisImageDir(self):
        directory = getDir() + '/'
        self.visImageFrame.setDir(directory)
        
    def selectNewIRImageDir(self):
        directory = getDir() + '/'
        self.irImageFrame.setDir(directory)
        
        
    def quit():
        root.destroy()
        
    def quitter(self):
        root.destroy()

top = Application()
top.master.title('Harpy Eagle GUI')
top.mainloop()

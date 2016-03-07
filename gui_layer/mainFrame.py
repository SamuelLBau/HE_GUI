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
from logFileReader import logFileReader
from HEdataObject import HEdataObject
from access_meta_file import *

from simpleDialogs import *
from profileDialogs import *
from tempRangeDialog import temperatureDialog

class mainFrame(tk.Frame):
    profileDir = 0
    profileFieldList = ["metaFile","irDir","visDir","tiffFile"]
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
    logFileReader = 0
    
    visSuffix = ".png"
    irSuffix = ".png"
    
    metaFilePath = defaultMetaFile
    
    def __init__(self,master):
        tk.Frame.__init__(self,master,bg='#F0F0F0')
        self.profileDir = os.path.dirname(os.path.realpath(__file__)) + '/guiProfiles/'
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

        self.logFileReader = logFileReader()

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
       


        
    def newImageSelected(self,imageID):
        #This function is called by fileSelectorPanel, it updates
        #Each image panel, the metaFile and eventually the geotiff panel
        print("In main application, imageID = %s" %(imageID))
        
        self.visImageFrame.findNewImage(imageID)
        self.irImageFrame.findNewImage(imageID)
        
        #This should just be an array of strings, easy to print
        row = self.logFileReader.getImageRow(imageID)
        dataObject = logLineParser(row)

        self.metaDataFrame.loadData(dataObject.printArray())
    
        
        
        
#These functions are related to selecting what data to use
    def selectNewMetaFile(self,metaFile=""):
        print("new meta file: %s" %(metaFile))
        if(metaFile == ""):
            metaFile = getFile()
            
        if(not os.path.isfile(metaFile)):
            print("Selection was not a file, cannot read")
            return    
        self.logFileReader.setNewMetaFile(metaFile)
        #imageIDList = self.logFileReader.getColumn('imageID')
        self.imageListFrame.loadNewImages(self.logFileReader.getColumn('imageID'))
        self.imageListFrame.setMetaFile(metaFile)
        
    def createTempRangeDialog(self):
        dialog = temperatureDialog(self,self.changeIRTempRange)
        dialog.grid()
    
    def changeIRTempRange(self,values):
        lowTemp = values[0]
        highTemp = values[1]
        
        print("TODO: Use low and high values to edit IR image")
        
    def selectNewTiffFile(self,tiffFile=""):
        if(tiffFile==""):
            tiffFile = getFile() + '/'
            
        if(not os.path.isfile(tiffFile)):
            print("Selection was not a file, cannot read")
            return    
        
        self.mapImageFrame.setImage(tiffFile)
        
    def selectNewVisImageDir(self,directory=""):
        if(directory==""):
            directory = getFile()
        
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
        
    def saveProfile(self=None,filePath=""):
        #Assume at this time file either does not exist, or can be overwritten
        #Make sure this stays same as above
        #profileFieldList = ["metaFile","irDir","visDir","tiffFile"]
        stringList= []
        key = self.profileFieldList[0]
        value = self.imageListFrame.getFilePath()
        stringList.append(value)
        
        key = self.profileFieldList[1]
        value = self.irImageFrame.getDirectory()
        stringList.append(value)
        
        key = self.profileFieldList[2]
        value = self.visImageFrame.getDirectory()
        stringList.append(value)
        
        key = self.profileFieldList[3]
        value = self.mapImageFrame.getFilePath()
        stringList.append(value)

        
        dialog=saveProfileDialog(self.profileDir,self.profileFieldList,stringList)
        dialog.grab_set()
        dialog.wait_window(dialog)
        dialog.grab_release()
        #write_list_meta_file(filePath,fileA=self.profileFieldList,fieldB=stringList)
        
        
        
    def loadProfile(self=None,filePath=""):
        #This will be result from that file dialog
        if(filePath == ""):
            filePath = getFile(initialDir=self.profileDir)
            
        stringDict = {}
        for s in self.profileFieldList:
            stringDict[s]=read_meta_file(filePath,s)
            
        #Note: Defaults use relative paths,
        #none defaults do not
        curString = stringDict["metaFile"]
        if (curString != ""):
            self.selectNewMetaFile(curString)
            
        curString = stringDict["irDir"]
        if (curString != ""):        
            self.selectNewIRImageDir(curString)
            
        curString = stringDict["visDir"]
        if (curString != ""):  
            self.selectNewVisImageDir(curString)
            
        curString = stringDict["tiffFile"]
        if (curString != ""):  
            self.selectNewTiffFile(curString)
        
    def quit():
        root.destroy()
        
    def quitter(self):
        root.destroy()

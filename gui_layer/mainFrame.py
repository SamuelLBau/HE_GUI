#!/usr/bin/env python
import Tkinter as tk
from PIL import Image, ImageTk
import os
import sys
from shutil import copyfile

sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'metaReaders'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'additionalDialogs'))

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
from doubleImageDialog import doubleImageDialog
from loadRootDirDialog import loadRootDirDialog
#from enlargedMapDialog import enlargedMapDialog

class mainFrame(tk.Frame):
    enableMap = False
    
    
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
    defaultIRImagePath = ""
    defaultTiffPath = ""
    defaultMetaFile = ""
    logFileReader = 0
    
    
    #BEGIN CONFIG VARIABLES
    #These are sent to loadRootDirDialog when loading from root structure
    irDir = "thermal/"
    visDir = "visible/"
    logFile = "log.txt"
    #These are the expected file extensions for the images
    visSuffix = "_VIS.png"
    irSuffix = "_IR.png"
    
    
    metaFilePath = defaultMetaFile
    
    def __init__(self,master):
        tk.Frame.__init__(self,master,bg='#F0F0F0')
        self.profileDir = os.path.dirname(os.path.realpath(__file__)) + '/guiProfiles/'
        self.guiImagePath = os.path.dirname(os.path.realpath(__file__)) + '/res/guiImages/'
        self.defaultIRImageDir = os.path.dirname(os.path.realpath(__file__)) + "/res/guiImages/"
        self.defaultVisImageDir = os.path.dirname(os.path.realpath(__file__)) + "/res/guiImages/"
        self.defaultVisImagePath = self.defaultVisImageDir+"eagleT.png"
        self.defaultIRImagePath = self.defaultIRImageDir + "eagleBWT.png"
        self.defaultTiffPath = os.path.dirname(os.path.realpath(__file__)) + '/res/guiImages/belizeMap.jpg'
        self.defaultMetaFile = os.path.dirname(os.path.realpath(__file__)) + '/res/blankLog.txt'
    
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
        
        
        #This is placed here to expeditetesting, can freely remove when the opened image panel is successful
        #self.enlargeImages(self.defaultVisImagePath,self.defaultIRImagePath)
        
        #This is used to test the enlargeMapFunction
        #self.enlargeMap("C:/Users/Work/Documents/Files/Projects/HarpyEagle/HE_GUI/gui_layer/res/sampleRun/tiff/canyon_grid1_ortho.tiff")
        
        
    def placeFrames(self):
        
        
        self.visImageFrame = flightImagePanel(self, self.guiImagePath + "eagleT_VIS.png",
            frameTitle='Visible Image',exportDataFunc=self.exportDisplayedData,suffix=self.visSuffix)
        self.irImageFrame = flightImagePanel(self, self.guiImagePath + "eagleT_IR.png",
            frameTitle='Infra-red image',exportDataFunc=self.exportDisplayedData,suffix=self.irSuffix)
        self.mapImageFrame = mapPanel(self, self.defaultTiffPath)
        self.metaDataFrame = metaDataPanel(self)
        self.imageListFrame = fileSelectorFrame(self,self.newImageSelected,self.selectNewMetaFile)
        
        self.visImageFrame.grid(row = 0, column = 0,rowspan=2,sticky='wens')
        self.irImageFrame.grid(row = 0, column = 1,rowspan=2,sticky='wens')
        #self.mapImageFrame.grid(row=0,column = 2,sticky='wens')
        #self.metaDataFrame.grid(row=1,column = 2,sticky='wens')
        self.imageListFrame.grid(row=0,rowspan = 2,column = 3,sticky='wens')
        
        if(self.enableMap):
            self.mapImageFrame.grid(row=0,column = 2,sticky='wens')
            self.metaDataFrame.grid(row=1,column = 2,sticky='wens')
        else:
            self.metaDataFrame.grid(row=0,column = 2,sticky='wens')
        
        self.visImageFrame.setupFirstButton("Select Visible image directory",self.selectNewVisImageDir)
        
        self.irImageFrame.setupFirstButton("Select infra-red image directory",self.selectNewIRImageDir)
        self.irImageFrame.setupSecondButton("Change temperature Range",self.createTempRangeDialog)
       

    def prepEnlargeImages(self):
        visImagePath = self.visImageFrame.getImageFullPath()
        irImagePath = self.irImageFrame.getImageFullPath()
        self.enlargeImages(visImagePath,irImagePath)
        
    def enlargeImages(self,imageAPath,imageBPath):
        dialog = doubleImageDialog(imageAPath,imageBPath)
        dialog.grid()
    def enlargeMap(self,imagePath):
        dialog = enlargedMapDialog(self,tiffImagePath=imagePath)
        dialog.grid()
        #Will need to ensure this is destroyed on close
    def newImageSelected(self,imageID):
        #This function is called by fileSelectorPanel, it updates
        #Each image panel, the metaFile and eventually the geotiff panel
        print("In main application, imageID = %s" %(imageID))
        
        self.visImageFrame.findNewImage(imageID)
        self.irImageFrame.findNewImage(imageID)
        
        #This should just be an array of strings, easy to print
        dataObject = self.getDataObject(imageID)

        self.metaDataFrame.loadData(dataObject.printArray())
    
    def exportDisplayedData(self):
        #This should save the vis/IR image, the log line, the parsed log data
        #and maybe the tiff / name of tiff file used
        
        #be sure to add code that checks if file exists
        dirPath = getDir()
        if(not os.path.isdir(dirPath)):
            return
            #TODO:WARNING: Add warning / error message
            
        rootDir = getFiletoSave(dirPath)
        print(rootDir)
        
        if(os.path.exists(rootDir)):
            print("Please select a non-existant directory / file name")
            return
        
        lastIndex = rootDir.rindex('/')
        rootDirName = rootDir[lastIndex+1:] #The name that should be applied to this sample
        rootDir = rootDir + '/'
        
        print(rootDir)
        print(rootDirName)
        print(self.irImageFrame.getSuffix())
        irImagePath = self.irImageFrame.getImageFullPath()
        visImagePath = self.visImageFrame.getImageFullPath()
        imageID = self.imageListFrame.getActiveID()
        dataObject = self.getDataObject(imageID)
        logString = self.logFileReader.getImageRow(imageID)#Sent to writer as a list
        logString = [logLineParserString(logString)]
        newirImagePath = rootDir +rootDirName+self.irImageFrame.getSuffix()
        newvisImagePath = rootDir + rootDirName+self.visImageFrame.getSuffix()
        newlogFileName = rootDir+rootDirName + "_log.txt"
        newDataFileName = rootDir+rootDirName+"_data.txt"
        
        
        os.mkdir(rootDir)
        
        copyfile(irImagePath,newirImagePath)
        copyfile(visImagePath,newvisImagePath)
        
        print(newlogFileName)
        print(newDataFileName)
        
        write_list_meta_file(newlogFileName,logString)
        write_list_meta_file(newDataFileName,dataObject.printArray())
        
#These functions are related to selecting what data to use


    def selectRootDir(self):
        #This funtion selects a new directory,
        #It expects the following structure:
        #Rootdir (Any name)
        #   log.txt
        #   thermal
        #       *_ir.png
        #   visible
        #       *_vis.png
        
        #Need to, set directory, check for those folders
        #New dialog that presents each directory, 
        #Asks if you want to load a new tiff file
        #Button to save profileDialogs
        dialog = loadRootDirDialog(UDL=self.selectNewMetaFile,UDIR=self.selectNewIRImageDir,
            UDVIS=self.selectNewVisImageDir,UDTIFF=self.selectNewTiffFile,irDirName=self.irDir,
            visDirName=self.visDir,logFileName=self.logFile)
            
        dialog.grid()
        
        dialog.grab_set()
        dialog.wait_window(dialog)
        dialog.grab_release()
        
            
        
        
        
    def selectNewMetaFile(self,metaFile=""):
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
        
        #This stops rest of program from running until window returns
        dialog.grab_set()
        dialog.wait_window(dialog)
        dialog.grab_release()
    
    def changeIRTempRange(self,values):
        lowTemp = values[0]
        highTemp = values[1]
        
        print("TODO: Use low [%d] and high [%d] values to edit IR image"%(lowTemp,highTemp))
        
    def selectNewTiffFile(self,tiffFile=""):
        if(tiffFile==""):
            tiffFile = getFile()
            
        if(not os.path.isfile(tiffFile)):
            print("Selection was not a file, cannot read")
            print("Failed path: %s " %(tiffFile))
            return    
        
        self.mapImageFrame.setImage(tiffFile)
        
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
            
    def getDataObject(self,imageID):
        row = self.logFileReader.getImageRow(imageID)
        dataObject = logLineParser(row,structured=True)
        return dataObject
        
    def quit():
        root.destroy()
        
    def quitter(self):
        root.destroy()

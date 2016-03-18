#!/usr/bin/env python
import Tkinter as tk
from PIL import Image, ImageTk
import os
import sys
from shutil import copyfile
import numpy as np

from glob import glob

sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'metaReaders'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'additionalDialogs'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'supplementaryScripts'))

from flightImagePanel import flightImagePanel
from mapPanel import mapPanel
from metaDataPanel import metaDataPanel
from fileSelectorFrame import fileSelectorFrame

#These should be replaced by a system that reads from the CSV
from log2CSV import log2CSV
from process_thermal import therm_to_bmp
#from logParser import *
#from logFileReader import logFileReader
#from HEdataObject import HEdataObject       
#from access_meta_file import *

from simpleDialogs import *
from profileDialogs import *
from tempRangeDialog import temperatureDialog
from doubleImageDialog import doubleImageDialog
from loadRootDirDialog import loadRootDirDialog
#from enlargedMapDialog import enlargedMapDialog

class mainFrame(tk.Frame):
    enableMap = False
    VISandIR = False #This determines whether both Visible and IR panels are visible, enable if
    #You want to scroll by both visible and ir data
    
    
    profileDir = 0
    profileFieldList = ["irLogFile","visLogFile","irDir","visDir","tiffFile"]
    visImageFrame = 0
    irImageFrame = 0
    mapImageFrame = 0
    metaDataFrame = 0
    IRimageListFrame = 0
    VISimageListFrame = 0
    
    
    image = 0;
    
    guiImagePath = ""
    defaultIRImageDir = ""
    defaultVisImagePath = ""
    defaultIRImagePath = ""
    defaultTiffPath = ""
    defaultIRLogFile = ""
    defaultVISLogFile = ""
    logFileReader = 0
    
    
    #BEGIN CONFIG VARIABLES
    #These are sent to loadRootDirDialog when loading from root structure
    irDir = "thermal/"                      #irDir = "thermal/"
    visDir = "visible/"                     #visDir = "visible/"
    irLogFileName = "log.txt"               #irLogFileName = "log.txt"
    visLogFileName = "log.txt"              #visLogFileName = "log.txt"
    #These are the expected file suffix + extensions for the images
    visSuffix = "_VIS"                  #visSuffix = "_VIS.jpg"
    irSuffix = "_IR"                    #irSuffix = "_IR.bmp"
    editedSuffix = "_CONSTRAINED"
    
    visFileType = ".png"
    irFileType = ".png"
    
    
    
    #END CONFIG VARIABLES
    
    visFullSuffix = visSuffix + visFileType     #These are what is sent to each frame
    irFullSuffix = irSuffix + irFileType
    
    
    
    irLogFile = ""
    visLogFile = ""
    
    irNPData = 0 #This will hold the parsed data from the IR csv NP array
    visNPData = 0 #This will hold the parsed data from the VIS csv NP array
    
    #Just used to differentiate between the image list senders
    irID = "IR"
    visID = "VIS"
    
    def __init__(self,master):
        tk.Frame.__init__(self,master,bg='#F0F0F0')
        self.profileDir = os.path.dirname(os.path.realpath(__file__)) + '/guiProfiles/'
        self.guiImagePath = os.path.dirname(os.path.realpath(__file__)) + '/res/guiImages/'
        self.defaultIRImageDir = os.path.dirname(os.path.realpath(__file__)) + "/res/sampleRun/thermal/"
        self.defaultVisImageDir = os.path.dirname(os.path.realpath(__file__)) + "/res/sampleRun/visible/"
        self.defaultVisImagePath = os.path.dirname(os.path.realpath(__file__)) + "/res/guiImages/"+"eagleT.png"
        self.defaultIRImagePath = os.path.dirname(os.path.realpath(__file__)) + "/res/guiImages/" + "eagleBWT.png"
        self.defaultTiffPath = os.path.dirname(os.path.realpath(__file__)) + '/res/guiImages/belizeMap.jpg'
        self.defaultIRLogFile = os.path.dirname(os.path.realpath(__file__)) + '/res/sampleRun/thermal/log.txt'
        self.defaultVISLogFile = os.path.dirname(os.path.realpath(__file__)) + '/res/sampleRun/visible/log.txt'
    
        self.guiImagePath = self.guiImagePath.replace("\\","/")
        self.defaultIRImageDir = self.defaultIRImageDir.replace("\\","/")
        self.defaultVisImageDir = self.defaultVisImageDir.replace("\\","/")
        self.defaultTiffPath = self.defaultTiffPath.replace("\\","/")
        self.defaultIRLogFile = self.defaultIRLogFile.replace("\\","/")
        self.defaultVISLogFile = self.defaultVISLogFile.replace("\\","/")
        
        
        
        
    
        #self.metaFilePath = 
    
      #  self.guiImagePath = os.path.dirname(os.path.realpath(__file__)) + '/guiImages/'
      #  self.defaultTiffDir = os.path.dirname(os.path.realpath(__file__)) + '/defaultTiff/'
      #  self.defaultMetaFile = os.path.dirname(os.path.realpath(__file__)) + '/defaultMetaFile/log.txt'

        #TODO: Replace
        #self.logFileReader = logFileReader()

        #self.grid()
        self.placeFrames()
        self.update()
        
        self.selectNewIRImageDir(self.defaultIRImageDir)
        self.selectNewVisImageDir(self.defaultVisImageDir)
        self.selectNewLogFile(self.defaultIRLogFile,self.irID)
        self.selectNewLogFile(self.defaultVISLogFile,self.visID)
        
        
        #This is placed here to expeditetesting, can freely remove when the opened image panel is successful
        #self.enlargeImages(self.defaultVisImagePath,self.defaultIRImagePath)
        
        #This is used to test the enlargeMapFunction
        #self.enlargeMap("C:/Users/Work/Documents/Files/Projects/HarpyEagle/HE_GUI/gui_layer/res/sampleRun/tiff/canyon_grid1_ortho.tiff")
        
        
    def placeFrames(self):
        
        
        self.visImageFrame = flightImagePanel(self, self.guiImagePath + "eagleT_VIS.png",
            frameTitle='Visible Image',exportDataFunc=self.exportDisplayedData,suffix=self.visFullSuffix)
        self.irImageFrame = flightImagePanel(self, self.guiImagePath + "eagleT_IR.png",
            frameTitle='Infra-red image',exportDataFunc=self.exportDisplayedData,suffix=self.irFullSuffix)
        if(self.enableMap):
            self.mapImageFrame = mapPanel(self, self.defaultTiffPath)
        self.metaDataFrame = metaDataPanel(self)
        
        self.IRimageListFrame = fileSelectorFrame(self,self.newImageSelected,self.selectNewLogFile,ID=self.irID)
        self.VISimageListFrame = fileSelectorFrame(self,self.newImageSelected,self.selectNewLogFile,ID=self.visID)
        
        self.visImageFrame.grid(row = 0, column = 0,rowspan=2,sticky='wens')
        self.irImageFrame.grid(row = 0, column = 1,rowspan=2,sticky='wens')
        #self.mapImageFrame.grid(row=0,column = 2,sticky='wens')
        #self.metaDataFrame.grid(row=1,column = 2,sticky='wens')
        self.IRimageListFrame.grid(row=0,rowspan = 2,column = 3,sticky='wens')
        
        if(self.VISandIR):
            self.VISimageListFrame.grid(row=0,rowspan = 2,column = 4,sticky='wens')
        
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
        dialog = doubleImageDialog(imageAPath,imageBPath,PIC=self.IRimageListFrame.selectUp,NIC=self.IRimageListFrame.selectDown)
        dialog.grid()
        
    def enlargeMap(self,imagePath):
        dialog = enlargedMapDialog(self,tiffImagePath=imagePath)
        dialog.grid()
        
        #Will need to ensure this is destroyed on close
    def newImageSelected(self,imageID,senderID="IR"):
        #This function is called by fileSelectorPanel, it updates
        #Each image panel, the metaFile and eventually the geotiff panel
        #TODO LOGGER
        #print("In main application, imageID = %s" %(imageID))
        
        irImageID = imageID
        visImageID =  imageID
        
        
        if(senderID == self.visID):
            #ERRORCHECK
            rowNum = np.where(self.visNPData[:,0]==imageID)
            row = self.visNPData[rowNum[0][0],:]
            visImageID = imageID
            irImageID = row[1]
            #Note: From the visible file, visibleID is first,ir is second
        else:
            #ERRORCHECK
            rowNum = np.where(self.irNPData[:,0]==imageID)
            row = self.irNPData[rowNum[0][0],:]
            irImageID = imageID
            visImageID = row[1]
            
        
        self.visImageFrame.findNewImage(visImageID)
        self.irImageFrame.findNewImage(irImageID)
        
        #This updates the data panel
        stringList = self.generateStringList(imageID,senderID)

        self.metaDataFrame.loadData(stringList)
    
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
        
        irDir = self.irImageFrame.getDirectory()
        
        
        visImagePath = self.visImageFrame.getImageFullPath()
        imageID = self.IRimageListFrame.getActiveID()
        
        
        
            
                
        
        #For now, lets not worry about giving them the csv line
        #dataObject = self.getDataObject(imageID)
        logString = self.generateStringList(imageID,self.irID)
        
        
        newvisImagePath = rootDir + rootDirName+self.visImageFrame.getSuffix()
        newlogFileName = rootDir+rootDirName + "_log.txt"
        #newDataFileName = rootDir+rootDirName+"_data.txt"
        
        
        #print("Exporting images and matched IR data")
        #print("root directory: %s" %(rootDir))
        #print("Data name: %s" %(rootDirName))
        #print("Copying IR file: %s" %(irImagePath))
        #print("Copying VIS file: %s" %(visImagePath))
        #print("Data file Path: %s" %(newlogFileName))
        
        os.mkdir(rootDir)
        
        #Current image is
        IRlist = glob(irDir+imageID + '*')
        for s in IRlist:
            length = len(s)
            extension = s[length-3:length]
            if(self.editedSuffix in s):
                newFileName = rootDir + rootDirName + self.editedSuffix +'.'+ extension
            else:
                newFileName = rootDir + rootDirName+self.irImageFrame.getSuffix()
            copyfile(s,newFileName)
        
        copyfile(visImagePath,newvisImagePath)
        write_list_meta_file(newlogFileName,logString)
        #For now, lets not worry about giving them the csv line
        #write_list_meta_file(newDataFileName,dataObject.printArray())
        
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
        dialog = loadRootDirDialog(UDL=self.selectNewLogFile,UDIR=self.selectNewIRImageDir,
            UDVIS=self.selectNewVisImageDir,UDTIFF=self.selectNewTiffFile,irDirName=self.irDir,
            visDirName=self.visDir,IRlogFileName=self.irLogFileName,VISlogFileName=self.visLogFileName)
            
        dialog.grid()
        
        dialog.grab_set()
        dialog.wait_window(dialog)
        dialog.grab_release()
        
            
        
        
        
    def selectNewLogFile(self,logFile="",source="IR"): #TODO: ADAPT for IR / VIS source
        if(logFile == ""):
            logFile = getFile()
            
        if(not os.path.isfile(logFile)):
            #TODO LOGGER
            print("WARNING: Selection was not a file, cannot read")
            return
        #TODO LOGGER
        #print("logfile = %s"%(logFile))
        
        #This makes sure the CSV's exist
        #Called every time the log file is changed, ideally files are only selected together
        if(source == self.irID):
            irLogFile = logFile
            visLogFile = self.VISimageListFrame.getFilePath()
        else:
            irLogFile = self.IRimageListFrame.getFilePath()
            visLogFile = logFile
            
        [irCSVFile,visCSVFile] = self.convertLogtoCSV(irLogFile,visLogFile)
       # if(irCSVFile == "" or visCSVFile == ""):
       #     print("Could not find data log files")
       #     print("irCSVFile = %s" %(irCSVFile))
       #     print("visCSVFile = %s" %(visCSVFile))
       #     return
        
        #These are pointing to the generated CSVs
        if(source == self.irID):
            self.IRimageListFrame.setLogFile(irLogFile)
        else:
            self.VISimageListFrame.setLogFile(visLogFile)
            
        if(irCSVFile != ""):
            #TODO LOGGER
            #print("Loading %s log file: %s"%(source,irCSVFile))
            self.irNPData = np.loadtxt(irCSVFile,delimiter=',',skiprows=0,dtype="|S20")
            self.IRimageListFrame.loadNewImages(self.irNPData[2:,0])
        if(visCSVFile != ""):
            #TODO LOGGER
            #print("Loading %s log file: %s"%(source,visCSVFile))
            self.visNPData = np.loadtxt(visCSVFile,delimiter=',',skiprows=0,dtype="|S20")
            self.VISimageListFrame.loadNewImages(self.visNPData[2:,0])
            
            
            
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
        imagePath = self.irImageFrame.getDirectory()
        imagePath = imagePath + self.IRimageListFrame.getActiveID() + self.irFullSuffix
        if(imagePath == self.irFullSuffix):
            return
        #TODO ask eric if ftd file name can include _IR (Same as irSuffix)
        ftdPath = imagePath.replace(self.irFullSuffix,".ftd")#Removes suffix and replaces with .ftd
        newImagePath = therm_to_bmp(file_path=ftdPath,min_temp=lowTemp,max_temp=highTemp,suffix = self.editedSuffix)
        self.irImageFrame.setImage(newImagePath)
        
    def selectNewTiffFile(self,tiffFile=""):
        if(tiffFile==""):
            tiffFile = getFile()
            
        if(not os.path.isfile(tiffFile)):
            #TODO LOGGER
            print("WARNING: Tiff file selected was not a file, cannot read")
            print("NOTE: Failed path: %s " %(tiffFile))
            return    
        if(self.enableMap):
            self.mapImageFrame.setImage(tiffFile)
        
    def selectNewVisImageDir(self,directory=""):
        if(directory==""):
            directory = getDir() + '/'
        
        if(not os.path.isdir(directory)):
            #TODO LOGGER
            print("WARNING: VISIBLEDIR was not a directory, cannot read")
            print("NOTE: Failed path: %s " %(directory))
            return          
        self.visImageFrame.setDir(directory)
        
    def selectNewIRImageDir(self,directory=""):
        if(directory==""):
            directory = getDir() + '/'
        
        if(not os.path.isdir(directory)):
            #TODO LOGGER
            print("WARNING: IR Directory was not a directory, cannot read")
            print("NOTE: Failed path: %s " %(directory))
            return          
        self.irImageFrame.setDir(directory)
        
    def saveProfile(self=None,filePath=""):
        #Assume at this time file either does not exist, or can be overwritten
        #Make sure this stays same as above
        #profileFieldList = ["irLogFile","visLogFile","irDir","visDir","tiffFile"]
        stringList= []
        #key = self.profileFieldList[0]
        value = self.IRimageListFrame.getFilePath()
        stringList.append(value)
        
        #key = self.profileFieldList[1]
        value = self.VISimageListFrame.getFilePath()
        stringList.append(value)
        
        #key = self.profileFieldList[2]
        value = self.irImageFrame.getDirectory()
        stringList.append(value)
        
        #key = self.profileFieldList[3]
        value = self.visImageFrame.getDirectory()
        stringList.append(value)
        
        #key = self.profileFieldList[4]
        if(self.enableMap):
            value = self.mapImageFrame.getFilePath()
            stringList.append(value)
    
        #TODO LOGGER
        #print(self.profileFieldList)
        #print(stringList)
        dialog=saveProfileDialog(self.profileDir,self.profileFieldList,stringList)
        dialog.grab_set()
        dialog.wait_window(dialog)
        dialog.grab_release()
        dialog.destroy()
        #write_list_meta_file(filePath,fileA=self.profileFieldList,fieldB=stringList)
        
        
        
    def loadProfile(self=None,filePath=""):
        #This will be result from that file dialog
        
        if(filePath == ""):
            filePath = getFile(initialDir=self.profileDir)
        if(filePath == ""):
            #TODO LOGGER
            print("WARNING: Tried to load invalid profile file")
            print(filePath)
            return
        stringDict = {}
        for s in self.profileFieldList:
            stringDict[s]=read_meta_file(filePath,s)
            
        #Note: Defaults use relative paths,
        #none defaults do not
        #Make sure this stays same as above
        #profileFieldList = ["irLogFile","visLogFile","irDir","visDir","tiffFile"]
        curString = stringDict["irLogFile"]
        if (curString != ""):
            self.selectNewLogFile(curString,self.irID)
            
        curString = stringDict["visLogFile"]
        if (curString != ""):
            self.selectNewLogFile(curString,self.visID)
            
        curString = stringDict["irDir"]
        if (curString != ""):        
            self.selectNewIRImageDir(curString)
            
        curString = stringDict["visDir"]
        if (curString != ""):  
            self.selectNewVisImageDir(curString)
            
        curString = stringDict["tiffFile"]
        if (curString != ""):  
            self.selectNewTiffFile(curString)
            
    #def getDataObject(self,imageID):
    #    row = self.logFileReader.getImageRow(imageID)
    #    dataObject = logLineParser(row,structured=True)
    #    return dataObject
    def generateStringList(self,imageID,sourceID="IR"):
    
        if(sourceID == self.visID):
            #ERRORCHECK
            #TODO LOGGER
            columnIDs = self.visNPData[0,:]
        else:
            #ERRORCHECK
            #TODO LOGGER
            columnIDs = self.irNPData[0,:]
            
        if(sourceID == self.visID):
            #ERRORCHECK
            #TODO LOGGER
            rowNum = np.where(self.visNPData[:,0]==imageID)
            row = self.visNPData[rowNum[0][0],:]
        else:
            #ERRORCHECK
            #TODO LOGGER
            rowNum = np.where(self.irNPData[:,0]==imageID)
            row = self.irNPData[rowNum[0][0],:]

        length = len(columnIDs)
        i=0 
        stringList = []
        while i < length:
            stringList.append("%s: %s" %(columnIDs[i],row[i]))
            i=i+1
            
        return stringList
    def convertLogtoCSV(self,irLogFile="",visLogFile=""):
        continueConversion = True
        length = len(irLogFile)
        if(len(irLogFile) < 5):
            #TODO LOGGER
            print("WARNING: irLogFile is bad, cannot convert to CSV")
            print("NOTE: %s" %(irLogFile))
            continueConversion = False
        if(len(visLogFile) < 5):
            #TODO LOGGER
            print("WARNING: visLogFile is bad, cannot convert to CSV")
            print("NOTE: %s" %(visLogFile))
            continueConversion = False
            
        if(not continueConversion):
            return ["",""]
        
        IRcsvFile = irLogFile[0:length-3]
        IRcsvFile = IRcsvFile + "csv"
        
        VIScsvFile = visLogFile[0:length-3]
        VIScsvFile = VIScsvFile + "csv"
    
        #For now depend only on the isfile irLogFile
        if(not os.path.isfile(irLogFile) and not os.path.isfile(IRcsvFile)):
            #TODO LOGGER
            print("WARNING: IR Data not found at: %s" %(irLogFile))
            print("WARNING: Also did not find at: %s" %(IRcsvFile))
            continueConversion = False
            
        if(not os.path.isfile(visLogFile) and not os.path.isfile(VIScsvFile)):
            #TODO LOGGER
            print("WARNING: VIS Data not found at: %s" %(visLogFile))
            print("WARNING: Also did not find at: %s" %(VIScsvFile))
            continueConversion = False
            
        #if(os.path.isfile(IRcsvFile) and os.path.isfile(VIScsvFile)):
        #    print("CSV files already exist, skipping conversion")
        #    continueConversion = False
        
        #At this point, csv is made or can be made
        print("Making CSV names")
        print("irLogFile: %s" %(irLogFile))
        print("irLogFile: %s" %(visLogFile))
        print("IRcsvFile: %s" %(IRcsvFile))
        print("VIScsvFile: %s" %(VIScsvFile))
        log2CSV(irLogFile,visLogFile,IRcsvFile,VIScsvFile)
        print("After log2CSV")
        print("irLogFile: %s" %(irLogFile))
        print("irLogFile: %s" %(visLogFile))
        print("IRcsvFile: %s" %(IRcsvFile))
        print("VIScsvFile: %s" %(VIScsvFile))
            
        return [IRcsvFile, VIScsvFile]
        
    def quit():
        root.destroy()
        
    def quitter(self):
        root.destroy()

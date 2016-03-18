import Tkinter as tk
import tkFileDialog as filedialog
import tkSimpleDialog as simpledialog
from ToolTip import *

import sys
import os

from PIL import Image, ImageTk
from glob import glob


class flightImagePanel(tk.Frame):
    dynFindSuffix = False
    imageExtensionList = ["jpg","jpeg","bmp","png"] 


    image = 0 #this is needed to store the image\
    pathToolTip = 0
    defaultImagePath = 0
    imageDirLabel = 0
    imageSuffix = 0
    imageName = ""
    imageDir = ""
    imagePath = ""
    frameTitle = 0
    imageMaxHeight = 600.0
    imageMaxWidth = 600.0
    firstButton = 0
    secondButton = 0
    exportDataButton = 0
    exportDataFunc = 0
    def __init__(self,parent,defaultImagePath,frameTitle,exportDataFunc,suffix=".png"):

        tk.Frame.__init__(self,parent,bg='#F0F0F0',bd=1,relief='sunken')
        
        self.imageSuffix = suffix
        self.defaultImagePath = defaultImagePath
        self.exportDataFunc = exportDataFunc
        
        self.initWidgets(frameTitle)
       
        self.setImage(self.defaultImagePath) #NOTE: Later, will take in ID and append suffix
        
        
    def initWidgets(self,frameTitle):
        
        
        self.imageDirLabel = tk.Text(self,height=1,state='disable',bg='#F0F0F0',bd=0,wrap='char')
        self.imageDirLabel.grid(row=1,column = 0,columnspan=2)
        
        self.imageCanvas = tk.Canvas(self,bg='#F0F0F0',bd=0)
        self.imageCanvas.grid(row=2,column = 0,sticky = 'W',columnspan=2)
        
        self.frameTitle = tk.Text(self,height=1,state='disable',bg='#F0F0F0',bd=0,wrap='char',)
        self.frameTitle.grid(row=0,column = 0,columnspan=2)
        
        self.frameTitle.config(state='normal',width=len(frameTitle))
        self.frameTitle.delete(1.0, 'end')
        self.frameTitle.insert('insert',frameTitle)
        self.frameTitle.config(state='disable')
        
        self.exportDataButton = tk.Button(self,height=1,text="Export data",command=self.exportDataFunc)
        self.exportDataButton.grid(row=9,column=0)
        
        #if(self.FB != 0)
        #    FB.config(parent=self)
        
    
    def findNewImage(self,imageID):
        self.imageName = imageID
    
        path = self.imageDir + self.imageName + self.imageSuffix
        self.setImage(path)
            
        
    def setImage(self,path):
        if(not os.path.exists(path)):
            #TODO LOGGER
            print("WARNING: Failed to set image at path: %s " %(path))
            path = self.defaultImagePath
            print("NOTE: Image not found, using default image")
        #TODO LOGGER
        #print("Setting image at path: %s " %(path))
        self.imagePath = path   
        image = Image.open(path)
        imSize= image.size
        if(imSize[1] > self.imageMaxHeight):
            ratio = imSize[1] / self.imageMaxHeight
            #TODO LOGGER
            print("NOTE: Image too tall, changing max size to %f, image ratio %f" %(self.imageMaxHeight,1/ratio))
            imSize = (int(round(imSize[0] / ratio)),int(self.imageMaxHeight))
            image = image.resize(imSize)
        photo = ImageTk.PhotoImage(image)
        #try:
        self.image = photo
        self.imageCanvas.create_image(1,1,image=self.image,anchor='nw')
        self.imageCanvas.config(width=imSize[0],height=imSize[1])
        self.update()
        
        #createToolTip(self.imageCanvas,path)
        fullPath = path.replace("\\","/")
        lastIndex = fullPath.rindex('/')
        sLastIndex = fullPath.rindex('/',0,lastIndex-1)
        dispPath = fullPath[lastIndex+1:]
        
        #self.imageDir = fullPath[0:lastIndex+1]
        self.imageName = fullPath[lastIndex:]
        #dispPath = dispPath[sLastIndex:len(dispPath)]
        
        self.imageDirLabel.config(state='normal',width=len(dispPath))
        self.imageDirLabel.delete(1.0, 'end')
        self.imageDirLabel.insert('insert',dispPath)
        self.imageDirLabel.config(state='disable')
        #self.imageCanvas.pack_forget()
        
        
        createToolTip(self.imageDirLabel,fullPath)
    
    def setDir(self,dirName):
        self.imageDir = dirName
        
        if(self.dynFindSuffix):
            extension = self.findNewSuffix(dirName)
            self.imageSuffix = self.imageSuffix.split[0] + '.' + extension
            
        list = glob(dirName+ '*'+self.imageSuffix)
        for file in list:
            self.setImage(file)
            break#Only sets first image, then exits
        createToolTip(self.firstButton,dirName)
        
    def setupFirstButton(self,text="",func=0):
        self.firstButton = tk.Button(self,text=text,command = func,width=len(text))
        self.firstButton.grid(row=3,column=0)
        
    def setupSecondButton(self,text="",func=0):
        self.secondButton = tk.Button(self,text=text,command = func,width=len(text))
        self.secondButton.grid(row=4,column=0) 
        
    def getDirectory(self):
        return self.imageDir
    def getImageName(self):
        return self.imageName
    def getImageFullPath(self):
        return self.imagePath
    def getSuffix(self):
        return self.imageSuffix
    def findNewSuffix(self,dirName):
        list = glob(dirName+ '*')
        for s in list:
            s = s.split('.')
            length = len(s)
            extension = s[length-1]
            if(extension in self.imageExtensionList):
                return extension
         
        #This is only reached if a valid suffix is not found
        return self.imageSuffix.split('.')[1]
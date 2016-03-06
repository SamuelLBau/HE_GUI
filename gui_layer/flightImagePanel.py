import Tkinter as tk
import tkFileDialog as filedialog
import tkSimpleDialog as simpledialog
from ToolTip import *

import sys
import os

from PIL import Image, ImageTk
from glob import glob


class flightImagePanel(tk.Frame):
    image = 0 #this is needed to store the image\
    pathToolTip = 0
    defaultImagePath = 0
    imageDirLabel = 0
    imageSuffix = 0
    imageName = ""
    imageDir = ""
    frameTitle = 0
    imageMaxHeight = 600.0
    firstButton = 0
    secondButton = 0
    def __init__(self,parent,defaultImagePath,frameTitle,suffix=".png"):

        tk.Frame.__init__(self,parent,bg='#F0F0F0',bd=1,relief='sunken')
        
        self.imageSuffix = suffix
        self.defaultImagePath = defaultImagePath
        
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
        
        
        #if(self.FB != 0)
        #    FB.config(parent=self)
        
    
    def findNewImage(self,imageID):
        self.imageName = imageID
    
        path = self.imageDir + self.imageName + self.imageSuffix
        self.setImage(path)
            
        
    def setImage(self,path):
        if(not os.path.exists(path)):
            print("Failed to set image at path: %s " %(path))
            path = self.defaultImagePath
            print("Image not found, using default image")
        print("Setting image at path: %s " %(path))
            
        image = Image.open(path)
        imSize= image.size
        if(imSize[1] > self.imageMaxHeight):
            ratio = imSize[1] / self.imageMaxHeight
            print("Image too tall, changing max size to %f, image ratio %f" %(self.imageMaxHeight,1/ratio))
            imSize = (int(round(imSize[0] / ratio)),int(self.imageMaxHeight))
        
        image = image.resize(imSize, Image.ANTIALIAS) #TODO: RESIZE THIS
        photo = ImageTk.PhotoImage(image)
        #try:
        self.image = photo
        self.imageCanvas.create_image(1,1,image=self.image,anchor='nw')
        self.imageCanvas.config(width=imSize[0],height=imSize[1])
        self.update()
        
        fullPath = path.replace("\\","/")
        lastIndex = fullPath.rindex('/')
        sLastIndex = fullPath.rindex('/',0,lastIndex-1)
        dispPath = fullPath[lastIndex+1:]
        #dispPath = dispPath[sLastIndex:len(dispPath)]
        
        self.imageDirLabel.config(state='normal',width=len(dispPath))
        self.imageDirLabel.delete(1.0, 'end')
        self.imageDirLabel.insert('insert',dispPath)
        self.imageDirLabel.config(state='disable')
        #self.imageCanvas.pack_forget()
        
        
        createToolTip(self.imageDirLabel,fullPath)
    
    def setDir(self,dirName):
        self.imageDir = dirName
        createToolTip(self.firstButton,dirName)
        
    def setupFirstButton(self,text="",func=0):
        self.firstButton = tk.Button(self,text=text,command = func,width=len(text))
        self.firstButton.grid(row=3,column=0)
        
    def setupSecondButton(self,text="",func=0):
        self.secondButton = tk.Button(self,text=text,command = func,width=len(text))
        self.secondButton.grid(row=4,column=0) 
        
    def getDirectory(self):
        return self.imageDir

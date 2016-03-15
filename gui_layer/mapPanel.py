import Tkinter as tk
import tkFileDialog as filedialog

import sys
import os

from PIL import Image, ImageTk
from glob import glob

class mapPanel(tk.Frame):
    image = 0 #this is needed to store the image
    imageFilePath = ""
    imageNameLabel = 0
    imageCanvas = 0
    defaultImagePath = 0
    maxWidth = 500.0
    maxHeight = 270.0
    def __init__(self,parent,imagePath):
        tk.Frame.__init__(self,parent,bg='#F0F0F0',bd=1,relief='sunken')
        self.imageNameLabel = tk.Text(self,height=1,state='disable',bg='#F0F0F0',bd=0,wrap='char',width=20)
        self.imageNameLabel.grid(row=1,column = 0,sticky = 'W')
        
        self.imageCanvas = tk.Canvas(self,bg='#F0F0F0')
        self.imageCanvas.grid(row=0,column = 0,sticky = 'W')
        
        self.setImage(imagePath)
        
        
        
    def setImage(self,path):
    #TODO, add check to see if this image is already loaded, save time re-loading
        if(path == self.imageFilePath):
            return
        if(not os.path.isfile(path)):
            path = self.defaultImagePath
            print("Map not found, loading default image")
        try:       
            self.image = Image.open(path)
        except(IOError):
            print("Error loading image")
            return
            
        print("Setting map image at path: %s " %(path))
        self.imageFilePath = path
        
        imSize = self.image.size
        print("tiff size prerotate")
        print(imSize)
        if(self.image.size[0] < self.image.size[1]):
            self.image = self.image.rotate(90)
            imSize = [imSize[1], imSize[0]]
        #imSize = self.image.size
        print("tiff size precheck")
        print(imSize)
        imSize = self.checkSize(imSize)
        print("tiff size postcheck")
        print(imSize)
        
        #image = image.resize(self.IMSize, Image.ANTIALIAS) #TODO: RESIZE THIS
        self.image = self.image.resize(imSize, Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)
        #try:
        self.imageCanvas.create_image(1,1,image=self.image,anchor='nw')
        self.update()
        

        dispPath = path.replace("\\","/")
        lastIndex = dispPath.rindex('/')
        sLastIndex = dispPath.rindex('/',0,lastIndex-1)
        dispPath = dispPath[sLastIndex:len(dispPath)]
        
        self.imageNameLabel.config(state='normal')
        self.imageNameLabel.delete(1.0, 'end')
        self.imageNameLabel.insert('insert',dispPath)
        self.imageNameLabel.config(state='disable')
        
        
        self.config(width=imSize[0], height=imSize[1])
        #self.imageCanvas.pack_forget()
        
        
    def getFilePath(self):
        return self.imageFilePath
        
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
        
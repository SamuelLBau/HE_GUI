import Tkinter as tk
import tkFileDialog as filedialog

import sys
import os

from PIL import Image, ImageTk
from glob import glob

class mapPanel(tk.Frame):
    image = 0 #this is needed to store the image
    imageNameLabel = 0
    defaultImagePath = 0
    IMSize = 190, 270
    def __init__(self,parent,imagePath):
        tk.Frame.__init__(self,parent,bg='#F0F0F0',bd=1,relief='sunken')
        self.defaultImagePath = imagePath
        self.imageNameLabel = tk.Text(self,height=1,state='disable',bg='#F0F0F0',bd=0,wrap='char',width=20)
        self.imageNameLabel.grid(row=1,column = 0,sticky = 'W')
        
        self.imageCanvas = tk.Canvas(self,bg='#F0F0F0')
        self.imageCanvas.grid(row=0,column = 0,sticky = 'W')
        
        self.setImage(imagePath)
        
        
        
    def setImage(self,path):
        if(not os.path.exists(path)):
            path = self.defaultImagePath
            print("Map not found, loading default image")
        print("Setting map image at path: %s " %(path))
        
        self.image = 0        
        self.image = Image.open(path)
        #image = image.resize(self.IMSize, Image.ANTIALIAS) #TODO: RESIZE THIS
        self.image = self.image.resize(self.IMSize, Image.ANTIALIAS)
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
        #self.imageCanvas.pack_forget()
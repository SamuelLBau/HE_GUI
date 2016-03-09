import Tkinter as tk
import os
import sys


from PIL import Image, ImageTk
import scipy
from scipy import ndimage
import matplotlib.pyplot as plt


class panZoomFrame(tk.Frame):
    maxHeight = 800
    maxWidth = 1000
    mainCanvas = 0
    imagePath = ""
    rotateCWButton = 0
    rotateCCWButton = 0
    zoomInButton = 0
    zoomOutButton = 0
    panUpButton = 0
    panDownButton = 0
    panLeftButton=0
    panRightButton=0
    resetButton = 0
    def __init__(self,master,imagePath):
        tk.Frame.__init__(self,master,bg='#F0F0F0')
        self.imagePath = imagePath
        
        
        self.setupWidgets()
        self.placeWidgets()
        
        
    def setupWidgets(self):
        self.mainCanvas = tk.Canvas(self)
        
        self.rotateCWButton = tk.Button(self,text="Rotate CW",command=self.rotateCW)
        self.rotateCCWButton = tk.Button(self,text="Rotate CCW",command=self.rotateCCW)
        
        self.zoomInButton = tk.Button(self,text="Zoom in",command=self.zoomIn)
        self.zoomOutButton = tk.Button(self,text="Zoom out",command=self.zoomOut)
        
        self.panUpButton = tk.Button(self,text="Pan Up",command=self.panUp)
        self.panDownButton = tk.Button(self,text="Pan Down",command=self.panDown)
        self.panLeftButton = tk.Button(self,text="Pan Left",command=self.panLeft)
        self.panRightButton = tk.Button(self,text="Pan Right",command=self.panRight)
        
        self.resetButton = tk.Button(self,text="Reset",command=self.resetImage)
        
    def placeWidgets(self):
        #See notebook for designplan
        self.mainCanvas.grid(row=0,column=0,columnspan = 20,sticky='wens')
        
        self.rotateCWButton.grid(row=1,column=1,sticky='we')
        self.rotateCCWButton.grid(row=1,column=3,sticky='we')
        
        self.zoomInButton.grid(row=1,column=0,sticky='we')
        self.zoomOutButton.grid(row=3,column=0,sticky='we')
        
        self.panUpButton.grid(row=1,column=2,sticky='we')
        self.panDownButton.grid(row=3,column=2,sticky='we')
        self.panLeftButton.grid(row=2,column=1,sticky='we')
        self.panRightButton.grid(row=2,column=3,sticky='we')
        
        self.resetButton.grid(row=2,column=2,sticky='we')
        
    def resetImage(self):
        print("TODO: implement everything")
        
    def rotateCW(self):
        print("TODO: implement everything")
         
    def rotateCCW(self):
        print("TODO: implement everything")

    def zoomIn(self):
        print("TODO: implement everything")
        
    def zoomOut(self):
        print("TODO: implement everything")
        
    def panUp(self):
        print("TODO: implement everything")
        
    def panDown(self):
        print("TODO: implement everything")    
        
    def panLeft(self):
        print("TODO: implement everything")
        
    def panRight(self):
        print("TODO: implement everything")
        
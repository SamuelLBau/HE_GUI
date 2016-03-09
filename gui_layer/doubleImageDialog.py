#!/usr/bin/env python
import Tkinter as tk
import os
import sys

from panZoomFrame import panZoomFrame



class doubleImageDialog(tk.Toplevel):
    visImagePath = ""
    irImagePath = ""
    firstImageFrame = 0     #Currently will just be frames that hold
    secondImageFrame = 0
    
    
    def __init__(self,visImagePath,irImagePath,master=None):
        self.visImagePath = visImagePath
        self.irImagePath = irImagePath
    
    
        tk.Toplevel.__init__(self,bg='#F0F0F0')
        
        self.placeFrames()
        
        
        
    def placeFrames(self):
        
        self.firstImageFrame = panZoomFrame(self,self.visImagePath)
        self.secondImageFrame = panZoomFrame(self,self.irImagePath)
        
        
        self.firstImageFrame.grid(row=0,column=0)
        self.secondImageFrame.grid(row=0,column=1)
        
        

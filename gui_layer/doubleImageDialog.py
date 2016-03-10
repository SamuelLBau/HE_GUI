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
    
    linkImages = False
    
    
    def __init__(self,visImagePath,irImagePath,master=None):
        self.visImagePath = visImagePath
        self.irImagePath = irImagePath
    
    
        tk.Toplevel.__init__(self,bg='#F0F0F0')
        
        self.placeFrames()
        
        
        
    def placeFrames(self):
        
        self.firstImageFrame = panZoomFrame(self,self.visImagePath,self.frame1Updated)
        self.secondImageFrame = panZoomFrame(self,self.irImagePath,self.frame2Updated)
        
        self.firstImageFrame.grid(row=0,column=0)
        self.secondImageFrame.grid(row=0,column=1)
        
    def frame1Updated(self,value):
    
        #Value is a string representation of what frame1did
        if(value == 'link-images'):
            self.linkImages = not self.linkImages
            print(self.linkImages)
            self.firstImageFrame.changeLinked(value=self.linkImages,update=False)
            self.secondImageFrame.changeLinked(value=self.linkImages,update=False)
            
        if(self.linkImages == False):
            return
        #Only reaches here if images should be linked
        if(value == 'reset'):
            self.secondImageFrame.resetImage(update=False)
        elif(value == 'rotate-cw'):
            self.secondImageFrame.rotateCW(update=False)
        elif(value == 'rotate-ccw'):
            self.secondImageFrame.rotateCCW(update=False)
        elif(value == 'zoom-in'):
            self.secondImageFrame.zoomIn(update=False)
        elif(value == 'zoom-out'):
            self.secondImageFrame.zoomOut(update=False)
        elif(value == 'pan-up'):
            self.secondImageFrame.panUp(update=False)
        elif(value == 'pan-down'):
            self.secondImageFrame.panDown(update=False)
        elif(value == 'pan-left'):
            self.secondImageFrame.panLeft(update=False)
        elif(value == 'pan-right'):
            self.secondImageFrame.panRight(update=False)
            
    def frame2Updated(self,value):
        #Value is a string representation of what frame1did
        if(value == 'link-images'):
            self.linkImages = not self.linkImages
            print(self.linkImages)
            self.firstImageFrame.changeLinked(value=self.linkImages,update=False)
            self.secondImageFrame.changeLinked(value=self.linkImages,update=False)
            
        if(self.linkImages == False):
            return
        #Only reaches here if images should be linked
        if(value == 'reset'):
            self.firstImageFrame.resetImage(update=False)
        elif(value == 'rotate-cw'):
            self.firstImageFrame.rotateCW(update=False)
        elif(value == 'rotate-ccw'):
            self.firstImageFrame.rotateCCW(update=False)
        elif(value == 'zoom-in'):
            self.firstImageFrame.zoomIn(update=False)
        elif(value == 'zoom-out'):
            self.firstImageFrame.zoomOut(update=False)
        elif(value == 'pan-up'):
            self.firstImageFrame.panUp(update=False)
        elif(value == 'pan-down'):
            self.firstImageFrame.panDown(update=False)
        elif(value == 'pan-left'):
            self.firstImageFrame.panLeft(update=False)
        elif(value == 'pan-right'):
            self.firstImageFrame.panRight(update=False)
        
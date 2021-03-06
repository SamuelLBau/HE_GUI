import Tkinter as tk
import sys
import os
from glob import glob

from ToolTip import *


#import MetaFileReader

class fileSelectorFrame(tk.Frame):
    selectBox = 0
    frameTitle = 0
    newFileSelected = 0
    newMetaFileButton = 0
    newMetaFileFunc = 0
    activeID = 0
    
    def __init__(self,parent,newFileSelectedFunc,selectMetaFileFunc):
        tk.Frame.__init__(self,parent,bg='#F0F0F0',bd=1,relief='sunken')
        self.newFileSelected = newFileSelectedFunc
        self.initWidgets()
        self.newMetaFileFunc = selectMetaFileFunc
        self.loadNewImages([])
        
        
        
    def initWidgets(self):
        self.grid_rowconfigure(index=1,weight=1)
        self.frameTitle = tk.Text(self,height=1,state='disable',bg='#F0F0F0',bd=0,wrap='char',width=20)
        self.frameTitle.config(state='normal')
        self.frameTitle.delete(1.0, 'end')
        self.frameTitle.insert('insert','Image List')
        self.frameTitle.config(state='disable')
        self.frameTitle.grid(row=0,column=0)
        
        self.newMetaFileButton = tk.Button(self,text="Select Meta File",command=self.internalNewMetaFileFunc)
        self.newMetaFileButton.grid(row=2,column=0,sticky='n')
        
        self.selectBox = tk.Listbox(self)
        self.selectBox.grid_rowconfigure(2,weight=1)
        self.selectBox.grid(row=1,column=0,sticky='wens')
        self.selectBox.config(selectmode='single')
        self.selectBox.bind('<<ListboxSelect>>', self.updateSelection)
        
        #These are flipped because up on the listbox goes down in index
        self.selectBox.bind("<Up>",self.selectDown)
        self.selectBox.bind("<Down>",self.selectUp)
        
    
    def internalNewMetaFileFunc(self):
        #for some reason it would not link unless I used this intermediate function
        self.newMetaFileFunc()
        
        
    def selectUp(self,event):
    #ERRORCHECK
        snum = self.selectBox.curselection()[0] +1
        if snum < self.selectBox.size():
            self.selectBox.select_clear(snum-1)
            self.selectBox.select_set(snum)
            self.updateSelection()
            
    def setMetaFile(self,dirName):
        self.meta_file = dirName
        createToolTip(self.newMetaFileButton,self.meta_file)
        
        
    def selectDown(self,event):
        #ERRORCHECK
        snum = self.selectBox.curselection()[0] -1
        if snum >= 0 and snum < self.selectBox.size():
            self.selectBox.select_clear(snum+1)
            self.selectBox.select_set(snum)
            self.updateSelection()
            
            
    def loadNewImages(self,imageList):
        self.clearList()
        
        i=0
        for s in imageList:
            self.selectBox.insert(i,s)
            i=i+1
            
        if( i > 0): #at least one image in group
            self.selectBox.select_set(0)
            self.updateSelection()

    def clearList(self):
        self.selectBox.delete(0,"end")
          
    def updateSelection(self,event=None):
        imageID = self.selectBox.curselection()
        imageID = self.selectBox.get(imageID)
        self.activeID = imageID
        print("Current selection is %s" % (imageID))
        self.newFileSelected(imageID)
        
    def getFilePath(self):
        return self.meta_file
    
    def getActiveID(self):
        return self.activeID
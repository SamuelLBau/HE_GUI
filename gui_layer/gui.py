#!/usr/bin/env python
import Tkinter as tk
import os
import sys

from mainFrame import mainFrame

class Application(tk.Toplevel):
    mainFrameI = 0
    
    menubar = 0
    profileMenu = 0
    sourceMenu = 0
    actionMenu = 0
    
    def __init__(self,parent=None):
        tk.Toplevel.__init__(self,parent,bg='#F0F0F0',bd=1,relief='sunken')
        self.mainFrameI = mainFrame(self)
        
        
        self.mainFrameI.grid(row=0,column=0)
        
        self.placeAdditionalWidgets()
    
    def placeAdditionalWidgets(self):
        self.menuBar = tk.Menu(self)
        
        
        self.profileMenu = tk.Menu(self.menuBar,tearoff=0)
        self.profileMenu.add_command(label="Save current Profile",command=self.saveProfile)
        self.profileMenu.add_command(label="Load a profile",command=self.loadProfile)
        self.menuBar.add_cascade(label="Profiles",menu=self.profileMenu)
        
        self.sourceMenu = tk.Menu(self.menuBar,tearoff=0)
        self.sourceMenu.add_command(label="Select data dir.",command=self.mainFrameI.selectRootDir)
        self.sourceMenu.add_command(label="Set Visible dir.",command=self.mainFrameI.selectNewVisImageDir)
        self.sourceMenu.add_command(label="Set IR dir.",command=self.mainFrameI.selectNewIRImageDir)
        self.sourceMenu.add_command(label="Set meta file",command=self.mainFrameI.selectNewMetaFile)
        self.sourceMenu.add_command(label="Set tiff file",command=self.mainFrameI.selectNewTiffFile)
        self.menuBar.add_cascade(label="Sources",menu=self.sourceMenu)
        
        self.actionMenu = tk.Menu(self.menuBar,tearoff=0)
        self.actionMenu.add_command(label="Export current images",command=self.mainFrameI.exportDisplayedData)
        self.actionMenu.add_command(label="View Enlarged images",command=self.mainFrameI.prepEnlargeImages)
        self.actionMenu.add_command(label="Change temp. range",command=self.mainFrameI.createTempRangeDialog)
        
        self.menuBar.add_cascade(label="Actions",menu=self.actionMenu)
        
        self.config(menu=self.menuBar)
        
        
    def saveProfile(self):
        self.mainFrameI.saveProfile()
        
    def loadProfile(self):
        self.mainFrameI.loadProfile()
        
        
        
    def temp(self):   
        print("TODO: Add stuff")
    
    
    
root = tk.Tk()
root.withdraw()
top = Application(root)
top.protocol("WM_DELETE_WINDOW", root.destroy)
top.title('Harpy Eagle GUI')
root.mainloop()

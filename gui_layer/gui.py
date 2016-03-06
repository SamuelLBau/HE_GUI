#!/usr/bin/env python
import Tkinter as tk
from PIL import Image, ImageTk
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'metaReaders'))

from mainFrame import mainFrame
from flightImagePanel import flightImagePanel
from mapPanel import mapPanel
from metaDataPanel import metaDataPanel
from fileSelectorFrame import fileSelectorFrame


from logParser import *
from MetaFileReader import MetaFileReader
from HEdataObject import HEdataObject

from simpleDialogs import *
from tempRangeDialog import temperatureDialog

class Application(tk.Toplevel):
    mainFrameI = 0
    
    menubar = 0
    profileMenu = 0
    
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

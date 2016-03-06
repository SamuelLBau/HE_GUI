#This panel displays the metadata for the image currently being displayed

import Tkinter as tk
import tkFileDialog as filedialog
import tkSimpleDialog as simpledialog
from ToolTip import *

from HEdataObject import HEdataObject


class metaDataPanel(tk.Frame):
    frameTitle = 0
    textObject = 0     #This is the text object
    meta_file = 0
    frameTitleText = 'Meta-Data Display'
    metaFileFormat = [] #This is the value held in each column
    textList = []                    #This is each text line
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,bg='#F0F0F0',bd=1,relief='sunken')
         
        self.initWidgets()
        #self.createDataLines()
        
        
        
    def initWidgets(self):
        self.frameTitle = tk.Text(self,height=1,state='disable',bg='#F0F0F0',bd=0,wrap='char')
        self.frameTitle.config(state='normal',width = len(self.frameTitleText))
        self.frameTitle.delete(1.0, 'end')
        self.frameTitle.insert('insert',self.frameTitleText)
        self.frameTitle.config(state='disable')
        
        self.frameTitle.grid(row=0,column=0)
        
        self.textObject = tk.Text(self,bg='#F0F0F0',state='disable',height=1,width=60)
        self.textObject.grid(row=1,column=0,sticky="wens")
        

        
    def loadData(self,data):
        self.textObject.config(state='normal',height=len(data))
        self.textObject.delete(1.0, 'end')
        length = len(data)
        i = 0
        while i < length:
            #print(data[i])
            self.textObject.insert('insert',data[i]+'\n')
            i=i+1
        self.textList = data
        self.textObject.config(state='disable')
    
    
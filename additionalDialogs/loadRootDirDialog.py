import Tkinter as tk
import os
import sys

from simpleDialogs import *
#This dialog is used to select a root directory, instead of independantly selecting them
class loadRootDirDialog(tk.Toplevel):
    irDirName = ""
    visDirName=""
    IRlogFileName=""
    VISlogFileName=""
    
    rootDirPath = "NULL"
    irDirPath = "NULL"      #These actually store path values
    visDirPath = "NULL"
    IRlogFilePath = "NULL"
    VISlogFilePath = "NULL"
    tiffFilePath = "NULL"

    updateLogFile = 0       #these are function pointers
    updateIRDir = 0
    updateVISDir = 0
    updateTiffFile = 0
    rootDirPath = 0
    
    rootText = 0 #Just says Root Path :
    VISlogText = 0
    IRlogText = 0  #Just says log file Path: 
    irText = 0
    visText = 0
    tiffText = 0
    
    rootDirText = 0         #These actually hold data
    rootDirButton = 0
    IRlogPathText = 0
    IRlogPathButton = 0 # Used to select new log file
    VISlogPathText = 0
    VISlogPathButton = 0
    irDirText = 0
    irDirButton = 0
    visDirText = 0
    visDirButton = 0
    tiffPathText = 0    #Will probably be empty on loadup
    tiffPathButton = 0
    
    submitButton = 0
    cancleButton = 0
   
    
    def __init__(self,master=None,UDL=0,UDIR=0,UDVIS=0,UDTIFF=0,irDirName="",visDirName="",IRlogFileName="",VISlogFileName=""):
        #Initialize, then try loading directory in here
        tk.Toplevel.__init__(self,bg='#F0F0F0')
        self.title("Data Directory Selector")
        
        self.updateLogFile = UDL
        self.updateIRDir = UDIR
        self.updateVISDir = UDVIS
        self.updateTiffFile = UDTIFF
        
        self.IRlogFileName = IRlogFileName
        self.VISlogFileName = VISlogFileName
        self.irDirName = irDirName
        self.visDirName = visDirName
        
        self.initWidgets()
        self.setRootDir()
        
        
        
    def initWidgets(self):
        self.rootText = tk.Text(self,width=15,bg='#F0F0F0',height=1,bd=0)
        self.IRlogText = tk.Text(self,width=15,bg='#F0F0F0',height=1,bd=0)
        self.VISlogText = tk.Text(self,width=15,bg='#F0F0F0',height=1,bd=0)
        self.irText = tk.Text(self,width=15,bg='#F0F0F0',height=1,bd=0)
        self.visText = tk.Text(self,width=15,bg='#F0F0F0',height=1,bd=0)
        self.tiffText = tk.Text(self,width=15,bg='#F0F0F0',height=1,bd=0)
        
        self.rootDirText = tk.Text(self,width=15,bg='#F0F0F0',height=1,bd=0)
        self.IRlogFileText = tk.Text(self,width=15,bg='#F0F0F0',height=1,bd=0)
        self.VISlogFileText = tk.Text(self,width=15,bg='#F0F0F0',height=1,bd=0)
        self.irDirText = tk.Text(self,width=15,bg='#F0F0F0',height=1,bd=0)
        self.visDirText = tk.Text(self,width=15,bg='#F0F0F0',height=1,bd=0)
        self.tiffPathText = tk.Text(self,width=15,bg='#F0F0F0',height=1,bd=0)
        
        self.rootDirButton = tk.Button(self,text="Select root dir",command=self.setRootDir)
        self.IRlogPathButton = tk.Button(self,text="Select log file",command=self.setIRLogPath)
        self.VISlogPathButton = tk.Button(self,text="Select log file",command=self.setVISLogPath)
        self.irDirButton = tk.Button(self,text="Select thermal dir",command=self.setIrDir)
        self.visDirButton = tk.Button(self,text="Select visible dir",command=self.setVisDir)
        self.tiffPathButton = tk.Button(self,text="Select tiff file",command=self.setTiffPath)
        
        self.submitButton = tk.Button(self,text="Done",command=self.done)
        self.cancleButton = tk.Button(self,text="Cancle",command=self.quit)
        
        self.rootText.grid(row=0,column=0,sticky='w')
        self.IRlogText.grid(row=1,column=0,sticky='w')
        self.VISlogText.grid(row=2,column=0,sticky='w')
        self.irText.grid(row=3,column=0,sticky='w')
        self.visText.grid(row=4,column=0,sticky='w')
        self.tiffText.grid(row=5,column=0,sticky='w')
        
        self.rootDirText.grid(row=0,column=1,sticky='w')
        self.IRlogFileText.grid(row=1,column=1,sticky='w')
        self.VISlogFileText.grid(row=2,column=1,sticky='w')
        self.irDirText.grid(row=3,column=1,sticky='w')
        self.visDirText.grid(row=4,column=1,sticky='w')
        self.tiffPathText.grid(row=5,column=1,sticky='w')
        
        self.rootDirButton.grid(row=0,column=2,sticky='we')
        self.IRlogPathButton.grid(row=1,column=2,sticky='we')
        self.VISlogPathButton.grid(row=2,column=2,sticky='we')
        self.irDirButton.grid(row=3,column=2,sticky='we')
        self.visDirButton.grid(row=4,column=2,sticky='we')
        self.tiffPathButton.grid(row=5,column=2,sticky='we')
        
        self.submitButton.grid(row=6,column=0)
        self.cancleButton.grid(row=6,column=2)
        
        self.initTextValues()
        
        
        
    def initTextValues(self):
        self.changeText(self.rootText,"Root directory: ")
        self.changeText(self.IRlogText,"IRLog file Path: ")
        self.changeText(self.VISlogText,"VISLog file Path: ")
        self.changeText(self.irText,"Thermal image dir.: ")
        self.changeText(self.visText,"Visible image dir.: ")
        self.changeText(self.tiffText,"Tiff file path: ")
        
        
    def setRootDir(self,path=""):
        if(path == ""):
            path = getDir()+'/'
        if(path ==""):
            path = "NULL"
            
        if(not os.path.isdir(path) or path == "NULL"):
            #ERRORCHECK
            self.rootDirPath = "NULL"
            self.changeText(self.rootDirText,"NULL")
            return
        else:
            self.rootDirPath = path
            self.changeText(self.rootDirText,path)
            
        #logFilePath = path + self.logFileName
        #print(self.logFileName)
        irDirPath = path+self.irDirName
        visDirPath = path+self.visDirName
        irLogFilePath = irDirPath + self.IRlogFileName
        visLogFilePath = visDirPath + self.VISlogFileName
        tiffFilePath = "NULL"
        
        self.setIRLogPath(irLogFilePath)
        self.setVISLogPath(visLogFilePath)
        self.setIrDir(irDirPath)
        self.setVisDir(visDirPath)
        self.setTiffPath(tiffFilePath) #Commented because I want it to just be empty on load
        
    def setIRLogPath(self,path=""):
        if(path == ""):
            path = getFile() 
        if(path ==""):
            path = "NULL"
        #TODO LOGGER
        #print("NOTE: IR log path = %s" %(path))
        if(not os.path.isfile(path) or path == "NULL"):
            #ERRORCHECK
            self.IRlogFilePath = "NULL"
            self.changeText(self.IRlogFileText,"NULL")
            return
        else:
            self.IRlogFilePath = path
            self.changeText(self.IRlogFileText,path)
                 
    def setVISLogPath(self,path=""):
        if(path == ""):
            path = getFile()
        if(path ==""):
            path = "NULL"
        #TODO LOGGER
        #print("NOTE: VISlog path = %s" %(path))
        if(not os.path.isfile(path) or path == "NULL"):
            #ERRORCHECK
            self.VISlogFilePath = "NULL"
            self.changeText(self.VISlogFileText,"NULL")
            return
        else:
            self.VISlogFilePath = path
            self.changeText(self.VISlogFileText,path)
                 
    def setIrDir(self,path=""):
        if(path == ""):
            path = getDir()
        if(path ==""):
            path = "NULL"
            
        if(not os.path.isdir(path) or path == "NULL"):
            #ERRORCHECK
            self.irDirPath = "NULL"
            self.changeText(self.irDirText,"NULL")
            return
        else:
            self.irDirPath = path
            self.changeText(self.irDirText,path)
            
    def setVisDir(self,path=""):
        if(path == ""):
            path = getDir()
        if(path ==""):
            path = "NULL"
            
        if(not os.path.isdir(path) or path == "NULL"):
            #ERRORCHECK
            self.visDirPath = "NULL"
            self.changeText(self.visDirText,"NULL")
            return
        else:
            self.visDirPath = path
            self.changeText(self.visDirText,path)
            
    def setTiffPath(self,path=""):
        if(path == ""):
            path = getFile()
        if(path ==""):
            path = "NULL"
            
        if(not os.path.isfile(path) or path == "NULL"):
            #ERRORCHECK
            self.tiffFilePath = "NULL"
            self.changeText(self.tiffPathText,"NULL")
            return
        else:
            self.tiffFilePath = path
            self.changeText(self.tiffPathText,path)
            
            
    def done(self):
        #Send values to functions, then quit
        if(self.IRlogFilePath != "NULL"):
            self.updateLogFile(self.IRlogFilePath,source="IR")
        if(self.VISlogFilePath != "NULL"):
            self.updateLogFile(self.VISlogFilePath,source="VIS")
        if(self.irDirPath != "NULL"):
            self.updateIRDir(self.irDirPath)
        if(self.visDirPath != "NULL"):
            self.updateVISDir(self.visDirPath)
        if(self.tiffFilePath != "NULL"):
            self.updateTiffFile(self.tiffFilePath)
        self.quit()
    def quit(self):
        #Destroy this
        self.destroy()
        
    def changeText(self,textObject,value):
        invalidMessage = "Valid directory / File not found"
        #if text is NULL, set color red, otherwise color black
        if(value == "NULL"):
            textObject.config(state='normal',width=len(invalidMessage),fg='red')
            textObject.delete(1.0, 'end')
            textObject.insert('insert',invalidMessage)
            textObject.config(state='disable')
        else:
            textObject.config(state='normal',width=len(value),fg='black')
            textObject.delete(1.0, 'end')
            textObject.insert('insert',value)
            textObject.config(state='disable')
        
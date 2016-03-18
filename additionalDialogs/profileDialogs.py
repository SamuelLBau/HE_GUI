import Tkinter as tk
import os
import sys

from ToolTip import *

sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'metaReaders'))
from access_meta_file import *



#Note, the file format must be same here as it is in load Profile dialog,
#Also check read_meta_file to ensure compatibility
class saveProfileDialog(tk.Toplevel):
    errorText = 0
    profileDetailsText = 0
    saveNameText = 0
    profileListText = 0
    nameTB = 0
    profileText = "" #Will just be placed directly after nameTB
    existingProfilesListBox = 0 #Will hold names of existing profile names
    saveButton = 0 #Add Are you sure you want to overwrite button
    profileObjectList = [] #each line to be saved in new profile
    initGridRow = 0
    
    dirPath = 0
    
    stringList = []
    def formatStrings(self,tags,values):
        self.stringList = []
        length = len(tags)
        if( length > len(values)):
            length = len(values)
           #Ensures no out of bounds occur 
        i=0
        while i < length:
            self.stringList.append(tags[i] +"| " + values[i])
            i=i+1
        #TODO LOGGER    
        #print("PRINTING STRINGLIST")
        #print(self.stringList)
     
        
    def __init__(self,dirPath,tags,values):
        print("CREATING SAVEPROFILE")
        tk.Toplevel.__init__(self,bg='#F0F0F0')
        self.title("Save Profile")
        self.dirPath = dirPath
        self.tagList = tags
        self.values = values
        
        self.formatStrings(tags,values)
        
        self.initWidgets()
        self.populateTexts()
        self.populateListbox(dirPath)
        self.createProfileDetails()
        
    def initWidgets(self):
        self.errorText = tk.Text(self,height=2,state='disable',bg='#F0F0F0',fg='red',bd=0,width=70,wrap='word',)
        
        self.saveNameText = tk.Text(self,height=1,state='disable',bg='#F0F0F0',bd=0,width=len("Profile name: "))
        self.nameTB = tk.Entry(self,width=15)
        self.profileText = tk.Text(self,height=1,bg='#F0F0F0',bd=0,width=len(".profile"))
        self.saveButton = tk.Button(self,text="Save profile",command=self.trySaveProfile)
        
        self.profileListText = tk.Text(self,height=1,bg='#F0F0F0',bd=0,width=len("Existing profiles: "))
        self.existingProfilesListBox = tk.Listbox(self,height=3)
        
        
        self.profileDetailsText = tk.Text(self,height=1,state='disable',bg='#F0F0F0',bd=0,width=len("Profile details: "))
        
        
        self.errorText.grid(row=0,column=0,columnspan=9,sticky='w')
        self.saveNameText.grid(row=1,column=0,sticky='e')
        self.nameTB.grid(row=1,column=1,sticky='e')
        self.profileText.grid(row=1,column=2,sticky="w")
        self.saveButton.grid(row=1,column=3)
        
        self.profileListText.grid(row=2,column=0)
        self.existingProfilesListBox.grid(row=2,column=1,columnspan=2)
        
        self.profileDetailsText.grid(row=3,column=0,sticky='w')
        
        self.initGridRow = 4
     
    def populateListbox(self,dirPath):
        existingFileList = os.listdir(dirPath)
        for s in existingFileList:
            end = len(s.split('.'))-1
            if(s.split('.')[end] == "profile"):
                self.existingProfilesListBox.insert('end',s)
        
        
    def populateTexts(self):
        self.saveNameText.config(state='normal')
        self.saveNameText.delete(1.0, 'end')
        self.saveNameText.insert('insert',"Profile name: ")
        self.saveNameText.config(state='disable')
        
        self.profileListText.config(state='normal')
        self.profileListText.delete(1.0, 'end')
        self.profileListText.insert('insert',"Existing profiles: ")
        self.profileListText.config(state='disable')
        
        self.profileText.config(state='normal')
        self.profileText.delete(1.0, 'end')
        self.profileText.insert('insert',".profile")
        self.profileText.config(state='disable')
        
        self.profileDetailsText.config(state='normal')
        self.profileDetailsText.delete(1.0, 'end')
        self.profileDetailsText.insert('insert',"Profile details: ")
        self.profileDetailsText.config(state='disable')
        
    def createProfileDetails(self=None):
    #This function creates the text lines with the details of the new profile
        textWidth = 150
        
        row = self.initGridRow
        length = len(self.stringList)
        
        i=0
        while i < length:
            width= textWidth
            if(len(self.stringList[i]) < width):
                width = len(self.stringList[i])
            newText = tk.Text(self,height=1,state='disable',bg='#F0F0F0',bd=0,width=width)
            newText.grid(row=row,column=0,sticky='w',columnspan=8)
            row=row+1
            
                
            newText.config(state='normal')
            newText.delete(1.0, 'end')
            newText.insert('insert',self.stringList[i])
            newText.config(state='disable')
            createToolTip(newText,self.stringList[i])
            i=i+1
        
    def trySaveProfile(self=None):
        fileName = self.nameTB.get()+".profile"
        string = self.nameTB.get().replace("_","").replace(".","")
        if(not str.isalnum(string)):
            self.setError("Name must be made up of letters, numbers and underscores")
            return
            
        if(os.path.isfile(self.dirPath +fileName)):
            self.setError("I currently can't allow you to overwrite profiles, please delete any profiles with this same name")
            return
            
        if(not os.path.isdir(self.dirPath)):
            self.setError("There was an error and the directory is not correctly defined, please exit this window")
            return
        self.setError() #This will clear the errorList
        write_list_meta_file(self.dirPath+fileName,self.stringList)
        self.destroy()
        
    def setError(self,errorString=""):
        if errorString != "":
            self.errorText.config(state='normal')
            self.errorText.delete(1.0, 'end')
            self.errorText.insert('insert',errorString)
            self.errorText.config(state='disable')
            
        else:
            self.errorText.config(state='normal')
            self.errorText.delete(1.0, 'end')
            self.errorText.config(state='disable')
            
            
    
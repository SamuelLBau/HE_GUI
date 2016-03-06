import sys
import numpy as np
import os
import fileinput

from HEdataObject import HEdataObject



class MetaFileReader():
    npArray = 0
    columnIDs = ["imageID","Altitude","Gps","Speed"]
    def __init__(self,filePath = ""):
    
        if(os.path.exists(filePath)):
            self.setNewMetaFile(filePath)
        
    def setNewMetaFile(self,filePath):
        print("New meta file: %s" %(filePath))
        if(not os.path.exists(filePath)):
            print("Log file not found, no valid data imported")
            return
            
            
        self.npArray = np.genfromtxt(filePath, delimiter='|', names=self.columnIDs,dtype=None)
        print("Importing data from metafile : %s" %(filePath))
        #self.npIDColumn = self.npArray["imageID"]
        #print(self.npArray)
        
        self.getColumnIDS()

        
        
    def getImageRow(self,imageID):
        #Iindex = self.npArray.where(imageID)
        #print("numpyindex = ")
        #print(index)
        column = self.getColumn("imageID")
        #print(imageID)
        index = np.where(column==imageID)
        #print("Index = %d" %(index))
        #print("Index[0] = %d" %(index[0]))
        #print("Index[0][0] = %d" %(index[0][0]))
        if(len(index) == 0): #Change this to return empty stuff
            index = 0
        else:
            index = index[0][0] #finds first instance and returns it
        
        #print("Index[0][0] = %d" %(index))
        return self.getRowIndex(index) 
        
        
    def getRowIndex(self,index):
        if(len(self.npArray) > index):
            return self.npArray[index]
        else:
            return 0 #TODO: Change to return empty stuff
            
            
    def getColumn(self,columnID):
        return self.npArray[columnID]
        
    def getColumnIDS(self):
        #ERRORCHECK
        stringList = self.getRowIndex(0)
        self.columnIDs = ["imageID"]
        length = len(stringList)
        i=1
        while i < length:
            string = stringList[i]
            firstBracketIndex = string.find('{')
            self.columnIDs.append(string[0:firstBracketIndex])
            i=i+1

        
import numpy as np
from HEdataObject import HEdataObject

keepLOGStructure = True

def logLineParser(npLine):
    numEntries = len(npLine)
    dataString = "ID"
    dataValue = 0
    dataObject = HEdataObject(npLine[0]) # Object has its entry ID as name
    print("dataObject")
    print(dataObject.printArray())
    i=1
    while i<numEntries:
        curString = npLine[i]
        curString = curString.replace(" ","")
        stringList = curString.split(',')
        numSubEntries = len(stringList)
        j=0
        while j < numSubEntries: 
            curSubString = stringList[j]
            FBI = curSubString.find('{')
            if(FBI != -1): #Can't be more than 1 open brace between columns
                newLayer = curSubString[0:FBI].split('=')[0]
                dataString = dataString + '.'+newLayer
                curSubString = curSubString[FBI:]
            
            splitString = curSubString.split('=')
            splitString[0] = dataString+'.'+splitString[0].replace("}","").replace("{","")
            splitString[1] = splitString[1].replace("}","")
            dataObject.updateDict(key=splitString[0],value=splitString[1])
            #print("dataString = %s" %(splitString[0]))
            #print(splitString[1])
            
            CBI = curSubString.find('}')
            while (CBI != -1): #This loop effectively closes braces
                dot = dataString.rfind('.')
                curSubString = curSubString[CBI+1:]
                CBI = curSubString.find('}')
                if(dot == -1):
                    dataString == "ID"
                else:
                    dataString = dataString[0:dot]
                    
            j =j+1
        #close while j < numSubEntries:         
                #There is a curly brace in here
        if(dataString != "ID"):
            print("ERROR IN PARSING, UNMATCHED BRACES")
        i=i+1
    #close while i<numEntries:
    return dataObject
    
def logLineParserString(npRow):
    numEntries = len(npRow)
    outString = ""
    
    i=0
    while i < numEntries:
        curString = npRow[i]
        outString+= curString + "|"
        i = i+1
        
    if(len(outString) >0):
        outString = outString[0:len(outString)-1]
        
    return outString
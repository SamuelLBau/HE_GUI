#This will use the log parser and HEObject to read/ parse each line, and convert it to a CSV format
#Will also add a field that converts the time (image ID) to a format that can easily be used to compare
#When an image was captured (to match each thermal image with a visible image)


#This will likely read in two log files (IR and VIS), and output two separate CSVs
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'metaReaders'))

import numpy as np
import fileinput

from HEdataObject import HEdataObject
from logFileReader import logFileReader
from logParser import *


def log2CSV(irLogPath,visLogPath,irCSVPath,visCSVPath,overwrite=False):
    print("Inside log2CSV")
    print("irLogPath: %s" %(irLogPath))
    print("visLogPath: %s" %(visLogPath))
    print("irCSVPath: %s" %(irCSVPath))
    print("visCSVPath: %s" %(visCSVPath))
    #TODO LOGGER
    #print("Entering log2CSV")
    continueConversion = checkFiles(irLogPath,visLogPath,irCSVPath,visCSVPath)
    #This requires that the names of the files be pre-determined
        
    if(not continueConversion):
        #TODO LOGGER
        print("NOTE: Skipping log2CSV")
        return -1
        
        
    #Generates the numpy arrays, currently just stores as strings
    [irNumpy,irColumnIDs,irDataTypes] = loadLog(irLogPath)
    [visNumpy,visColumnIDs,visDataTypes] = loadLog(visLogPath)
    
    #This is each id association, can make ir CSV by
    #ir pairs is the closest visImage for each ir image
    #visPairs is the closest irImage for each vis image
    irPairs = associateIDs(irNumpy,visNumpy)
    visPairs = associateIDs(visNumpy,irNumpy)
    
    writeData(irCSVPath,irNumpy,irPairs,irColumnIDs,irDataTypes)
    writeData(visCSVPath,visNumpy,visPairs,visColumnIDs,visDataTypes)
    #Next should be the write logic
    #for length idColumn
    # write(irPair[i][0]+','+ irPair[i][1] + irNumpy[i][EACHITEMAFTER2])
    
    
def writeData(saveFile,dataNumpy,dataPair,columnIDs,dataTypes):
    
    s = saveFile.split('.')
    length2 = len(s)
        
    
    lengthcolumnIDs = len(columnIDs)
    lengthDataTypes = len(dataTypes)
    
    columnIDs.insert(1,"matchedID")
    dataTypes.insert(1,"string")
    
    #This segment writes first two rows
    file = open(saveFile,'w')
    i = 0
    
    #Consider r
    while i < len(columnIDs): #-1 is necessary because I inserted the matchedID value
        writeString = columnIDs[i]
        if(i != len(columnIDs)-1):
            writeString = writeString+','
        file.write(writeString)
        i=i+1
    file.write('\n')
    
    i = 0
    while i < len(dataTypes): #-1 is necessary because I inserted the string value
        writeString = dataTypes[i]
        if(i != len(dataTypes)-1):
            writeString = writeString+','
        file.write(writeString)
        i=i+1
    file.write('\n')

    matrixHeight = len(dataNumpy[:,0])
    matrixWidth = lengthcolumnIDs #-1 is necessary because I inserted the matchedID value
    
    i = 0
    while i < matrixHeight:
        j = 1
        file.write("%s,%s,"%(dataPair[i][0],dataPair[i][1]))
        while j < matrixWidth:
            file.write("%s"%(dataNumpy[i,j]))
            if(j != matrixWidth-1):
                file.write(',')
            j=j+1
        file.write('\n')
        i=i+1

    file.close()
   
def checkFiles(irLogPath,visLogPath,irCSVPath,visCSVPath):
    continueConversion = True
    print("irLogPath %s"%(irLogPath))
    print("visLogPath %s"%(visLogPath))
    print("irCSVPath %s"%(irCSVPath))
    print("visCSVPath %s"%(visCSVPath))
    if(not os.path.isfile(irLogPath)):
        #TODO LOGGER
        print("WARNING: IR LOG file not found")
        continueConversion = False
    if(not os.path.isfile(visLogPath)):
        #TODO LOGGER
        print("WARNING: VISIBLE LOG file not found")
        continueConversion = False
    if(os.path.exists(irCSVPath)):
        #TODO LOGGER
        print("NOTE: IR CSV already exists, overwritting")
        #continueConversion = False
    if(os.path.exists(visCSVPath)):
        #TODO LOGGER
        print("NOTE: VISIBLE CSV file already exists,overwritting")
        #continueConversion = False 

    return continueConversion
def associateIDs(numpyA, numpyB):
    #numpyA and numpyB are both numpy matrices
    #print("returns an array with same length of A, with ID of each nearest item in numpyB")
    outPairList = []
    aColumn = numpyA[:,0]
    bColumn = numpyB[:,0]
    Alength = len(numpyA)
    Blength = len(numpyB)
    
    bIndex = 0
    
    i = 0
    while (i < Alength): #i is the thermal image index, should match for each one
        if(bIndex != Blength - 1):
            while (timeBetween(aColumn[i],bColumn[bIndex]) > timeBetween(aColumn[i],bColumn[bIndex+1])):
                bIndex = bIndex+1
                if(bIndex == Blength - 1):
                    break
        #print("Time A %s, Time B %s" %(aColumn[i],bColumn[bIndex]))
        #print("Pair %d, %d" %(timeBetween(aColumn[i],bColumn[bIndex]),timeBetween(aColumn[i],bColumn[bIndex+1])))    
        outPairList.append([aColumn[i],bColumn[bIndex]])
    
        i=i+1
    return outPairList
def loadLog(logPath):
    #Returns numpy object
    outNP = 0
    LFR = logFileReader(filePath=logPath)
    #Note: These caolumn IDs are just the term before the first bracket, ex: Altitude, Speed etc., not each inner term
    imageIDText = LFR.getColumnIDs()[0]
    
    IDList = LFR.getColumn(imageIDText) #Assume first column is the ID / timestamp,
    columnIDs = []
    dataTypes = []
    
    numEntries = len(IDList)
    
    #This if block gets the field names, then sorts it
    #Current order, 
    tupleList = []
    if (numEntries > 0):
        row = LFR.getImageRow(IDList[0])
        curData = logLineParser(row,structured=False)
        curDict = curData.getFullDict()
        for keys,values in curDict.items():
            columnIDs.append(keys)
            dataTypes.append(getDataType(values))
            tupleList.append((keys,"|S20"))
                  
        outNP = np.array((tuple(curData.getDictAsList())))
            
    numCols = len(columnIDs)
    i=0
    
    i = 1
    while i < numEntries:
        #This loops for every row in the log file
        row = LFR.getImageRow(IDList[i])
        curData = logLineParser(row,structured=False) #Type is HE object
        curData = tuple(curData.getDictAsList()) #Converted to a list
        outNP = np.vstack([outNP,curData])
        
        #curData = logLineParser(curData,structured=False)
        
        
        i=i+1
    return [outNP, columnIDs,dataTypes]
  
def getDataType(value):
    val = 0
    try:
        val = float(value)
        return "float"
    except ValueError:
        val = 0
    
    #defaults to string
    return "string"
    
def castAs(value,type):
    if(type == "float"):
        return float(value)
    if(type == "string"):
        return str(value)

def timeBetween(timeA,timeB):
    #Returns absolute value of time between
    val = time2int(timeA) - time2int(timeB)
    if(val < 0):
        val = -val
    return val
        
def time2int(value):
    #Assumes format: yyyyMMdd_HHmmss_sss
    #print("TODO: Convert string to an integer")
    year = long(value[0:4])
    month = long(value[4:6])
    day = long(value[6:8])
    hour = long(value[9:11])
    minute = long(value[11:13])
    second = long(value[13:15])
    millisecond = long(value[16:19])
    #print("Value: %s"%(value))
    
    
    
    outVal = year
    outVal = outVal * 12 + month
    outVal = outVal * 30 + day
    outVal = outVal * 24 + hour
    outVal = outVal * 60 + minute
    outVal = outVal * 60 + second
    outVal = outVal * 1000 + millisecond
    
    #if(millisecond == 61 or millisecond == 966 or millisecond == 899):
        #print("Value: %s"%(value))
        #print("SYear = %s"%(value[0:4]))
        #print("Smonth = %s"%(value[4:6]))
        #print("Sday = %s"%(value[6:8]))
        #print("Shour = %s"%(value[9:11]))
        #print("Sminute = %s"%(value[11:13]))
        #print("Ssecond = %s"%(value[13:15]))
        #print("Smillisecond = %s"%(value[16:19]))
        
        
        
        
        
        
        #print("Value: %s"%(value))
        #print("year: %d"%(year))
        #print("month: %d"%(month))
        #print("day: %d"%(day))
        #print("hour: %d"%(hour))
        #print("minute: %d"%(minute))
        #print("second: %d"%(second))
        #print("millisecond: %d"%(millisecond))
        #print("Outval = %d" %(outVal))
        #input("Pausing to read")
    
    return outVal
    
    

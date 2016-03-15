from logFileReader import logFileReader
from HEdataObject import HEdataObject
from logParser import *



filePath = "C:\Users\Work\Documents\Files\Projects\HarpyEagle\HE_GUI\metaReaders\log.txt"


LFR = logFileReader(filePath)


columnIDs = LFR.getColumnIDs()  #returns the IDs of each column as a list, assumes first column is imageID, 
#subsequent ID's are the first term following each | delimeter (Altitude{.....} ->Altitude)
print("Printing column IDs")
print(columnIDs)

imageList = LFR.getColumn("imageID")
#Returns a list representing each imageID (each item in first column)
print("Printing image list")
print(imageList)
curItem = imageList[0]
print("Printing curItem")
print(curItem)  #This is just the first imageID on list


#This gets the entire row with the matching imageID,
#This is why each rowID must be unique (which it will be if visible/IR
#Data is stored in separate files
row = LFR.getImageRow(curItem)
print("Printing row")
print(row)

#This is a HEdataObject
#For the most part is is just a dictionary
#With a few supplementary functions
#if structured is true, it holds structure of logfile
#If false it is easier to access,but requires all fields to be unique 
curData = logLineParser(row,structured=False)

#This produces a list of strings to present to structure / data of the object
printArray = curData.printArray()
print("Printing curData printArray")
print(printArray)

#This returns the given element, currently does not account for cases when an element is not present
groundSpeed = curData.getElem('groundSpeed')

longitude = curData.getElem('longitude')

fullDictionary = curData.getFullDict()
print("Printing curData elements")
print("groundSpeed = %s" %(groundSpeed))
print("longitude = %s" %(longitude))
print(fullDictionary)

for keys,values in fullDictionary.items():
    print("Key [%s] value [%s]" %(keys,values))
    
#Similar to above, but this version holds the json structure of the log file
#Element-wise access is handled differently
structCurData = logLineParser(row,structured=True)
printArray = structCurData.printArray()
print("Printing structCurData printArray")
print(printArray)


structFullDictionary = structCurData.getFullDict()

#Note in this case the path to the field must be included
structGroundSpeed = structCurData.getElem('Speed.groundSpeed')

structLatitude = structCurData.getElem('Gps.mPosition.latitude')
structLongitude = structCurData.getElem('Gps.mPosition.longitude')

structFullDictionary = structCurData.getFullDict()
print("Printing structured elements")
print("structGroundSpeed = %s" %(structGroundSpeed))
print("latitude = %s" %(structLatitude))
print("longitude = %s" %(structLongitude))
print(structFullDictionary)

from collections import OrderedDict

class HEdataObject():
    #This is general,  and maintains structure of LOG file
    dataDictionary = OrderedDict([])
    structured = False
    def __init__(self,name="",structured=False):
        self.structured = structured
        if(name != ""):
            self.dataDictionary = OrderedDict([])
            self.dataDictionary['ID'] = name
        
    def updateDict(self,key,value):
    #to go deeper use format Gps.mPosition.latitude
        key=key.split('.')
        if(self.structured):
            string = key[1]
            del key[0]
            #print("Entering updateDict key = %s value = %s, len(key) = %d" %(key,value,len(key)))
            self.dataDictionary[string] = self.updateSubDict(self.dataDictionary,key,value)
        else:
            string = key[len(key)-1]
            key = [string]
            self.dataDictionary[string] = value
        
       # print("Printing dataDictionary")
        #print(self.dataDictionary)
      
    def clearDict(self):
        del self.dataDictionary
        self.dataDictionary = OrderedDict([])
    
    def removeElem(self,key):
        del self.dataDictionary[key]
        
    def updateSubDict(self,dictionary,key,value):
        #print("Entering sub dict")
        #print(key)
        if(len(key) == 1):
            #print("Adding {%s : %s}" %(key[0] ,value))
            dictionary[key[0]] = value
           # print(dictionary)
            return
        else:
            if(key[0] in dictionary):
                newDict = dictionary[key[0]]
            else:
                newDict = {}
                dictionary[key[0]] = newDict
                #print("Setting ID %s" %(key[0]))
            string = key[0]
            del key[0]
            #print("Printing newDict before")
            #print(newDict)
            self.updateSubDict(newDict,key,value)
            #print("Printing newDict after")
            #print(newDict)
            return newDict
            
            
    def printArray(self):
        #This returns an array of strings to be printed simply
        tabList = ""
        printArray = []
        dictionary = self.dataDictionary
        #print("Printing full dictionary")
        #print(self.dataDictionary)
        return self.printValue(dictionary,tabList,printArray)

        
    def printValue(self,dictionary,tabList,printArray):
        if("ID" in dictionary):
            printArray.append("%s%s : %s" %(tabList,"ID",dictionary["ID"]))
        #tabList = tabList + '\t'
        for keys,values in dictionary.items():
            #print("PrintArray keys=%s,values=%s" %(keys,values))
            if type(values) == dict:
                printArray.append("%s%s :" %(tabList,keys))
                printArray = self.printValue(values,tabList+'\t',printArray)
            else:
                if(keys != "ID" and values != ""):
                    printArray.append("%s%s : %s" %(tabList,keys,values))
        
        return printArray
    def getElem(self,element):
        if(self.structured):
            curDict = self.dataDictionary
            element = element.split('.')
            while len(element) > 1:
                curDict = curDict[element[0]]
                del element[0]
            return curDict[element[0]]
        else:
            return self.dataDictionary[element]
            
    def getFullDict(self):
        return self.dataDictionary
    
    def getDictAsList(self):
        
        outList = []
        
        for keys,values in self.dataDictionary.items():
            outList.append(values)
        return outList
        
            
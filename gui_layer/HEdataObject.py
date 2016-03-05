class HEdataObject():
    #This is general,  and maintains structure of LOG file
    dataDictionary = {}
    def __init__(self,name=""):
        if(name != ""):
            self.dataDictionary['ID'] = name
        
    def updateDict(self,key,value):
    #to go deeper use format Gps.mPosition.latitude
        key=key.split('.')
        string = key[1]
        del key[0]
       # print("Entering updateDict key = %s value = %s" %(key,value))
        self.dataDictionary[string] = self.updateSubDict(self.dataDictionary,key,value)
       # print("Printing dataDictionary")
        #print(self.dataDictionary)
      
    def clearDict(self):
        del self.dataDictionary
        self.dataDictionary = {'Name': 0}
    
    def removeElem(self,key):
        del self.dataDictionary[key]
        
    def updateSubDict(self,dictionary,key,value):
        #print("Entering sub dict")
        #print(key)
        if(len(key) == 1):
            #print("Adding {%s : %s}" %(key[0] ,value))
            dictionary[key[0]] = value
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
            if type(values) == dict:
                printArray.append("%s%s :" %(tabList,keys))
                printArray = self.printValue(values,tabList+'\t',printArray)
            else:
                if(keys != "ID" and values != ""):
                    printArray.append("%s%s : %s" %(tabList,keys,values))
        
        return printArray
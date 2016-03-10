#!/usr/bin/env python
import Tkinter as tk
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'metaReaders'))




class temperatureDialog(tk.Toplevel):
    invalidTemp = -600
    lowTempTV = 0
    highTempTV = 0
    
    lowTempText = 0
    highTempText = 0
    
    unitsTextValue = u"\u2103"
    unitsText1 = 0
    unitsText2 = 0
    
    lowTempTB = 0
    highTempTB = 0
    
    lowTempError = 0
    highTempError = 0
    
    submitButton = 0
    cancelButton = 0
    updateTempFunc = 0
    
    def __init__(self,master=None,updateFunc=0):
        self.updateTempFunc = updateFunc
        tk.Toplevel.__init__(self,bg='#F0F0F0')
        
        
        self.unitsText1 = tk.Text(self,width=15,bg='#F0F0F0',height=1,bd=0)
        self.unitsText2 = tk.Text(self,width=15,bg='#F0F0F0',height=1,bd=0)
        
        self.lowTempTV = tk.StringVar()
        self.lowTempTV.trace("w", lambda name, index, mode,temp=self.lowTempTV.get(): self.changeLowTemp())
        
        self.highTempTV = tk.StringVar()
        self.highTempTV.trace("w", lambda name, index, mode,temp=self.highTempTV.get(): self.changeHighTemp())
        
        self.lowTempText = tk.Text(self,width=15,bg='#F0F0F0',height=1,bd=0)
        self.highTempText = tk.Text(self,width=15,bg='#F0F0F0',height=1,bd=0)
        
        self.lowTempText.config(state='normal',width=len("Low temperature"))
        self.lowTempText.delete(1.0, 'end')
        self.lowTempText.insert('insert',"Low temperature")
        self.lowTempText.config(state='disable')
        
        self.highTempText.config(state='normal',width=len("High temperature"))
        self.highTempText.delete(1.0, 'end')
        self.highTempText.insert('insert',"High temperature")
        self.highTempText.config(state='disable')
        
        self.unitsText1.config(state='normal',width=len(self.unitsTextValue))
        self.unitsText1.delete(1.0, 'end')
        self.unitsText1.insert('insert',self.unitsTextValue)
        self.unitsText1.config(state='disable')
        
        self.unitsText2.config(state='normal',width=len(self.unitsTextValue))
        self.unitsText2.delete(1.0, 'end')
        self.unitsText2.insert('insert',self.unitsTextValue)
        self.unitsText2.config(state='disable')
        
        
        
        self.lowTempTB = tk.Entry(self,width=8,textvariable=self.lowTempTV)
        self.highTempTB = tk.Entry(self,width=8,textvariable=self.highTempTV)
        
        self.lowTempError = tk.Text(self,width=15,bg='#F0F0F0',fg='#F0F0F0',height=1,bd=0)
        self.highTempError = tk.Text(self,width=15,bg='#F0F0F0',fg='#F0F0F0',height=1,bd=0)
        
        self.lowTempError.config(state='normal',width=len("Value must be integer"))
        self.lowTempError.delete(1.0, 'end')
        self.lowTempError.insert('insert',"Value must be integer")
        self.lowTempError.config(state='disable')
        
        self.highTempError.config(state='normal',width=len("Value must be integer"))
        self.highTempError.delete(1.0, 'end')
        self.highTempError.insert('insert',"Value must be integer")
        self.highTempError.config(state='disable')
        
        self.submitButton = tk.Button(self,text="Enter",command=self.submitNumbers)
        self.cancelButton = tk.Button(self,text="Cancel",command=self.cancle)
        
        
        self.lowTempText.grid(row=0,column=0)
        self.highTempText.grid(row=0,column=1)
        
        self.lowTempTB.grid(row=1,column=0)
        #self.unitsText1.grid(row=1,column=1)
        self.highTempTB.grid(row=1,column=1)
        #self.unitsText2.grid(row=1,column=3)
        
        self.lowTempError.grid(row=2,column=0)
        self.highTempError.grid(row=2,column=1)
        
        self.submitButton.grid(row=3,column=0)
        self.cancelButton.grid(row=3,column=1)
    
    def submitNumbers(self):
        lowTemp= self.checkTemp(self.lowTempTV.get())
        highTemp= self.checkTemp(self.highTempTV.get())
        
        if(lowTemp == self.invalidTemp or highTemp == self.invalidTemp):
            return
        
        if(lowTemp > highTemp):
            temp = lowTemp
            lowTemp = highTemp
            highTemp = temp
            
        self.updateTempFunc([lowTemp,highTemp])

        self.cancle()
        
            
        
    
    def cancle(self):
        self.destroy()
        
    def changeLowTemp(self=None):
        temp = self.checkTemp(self.lowTempTV.get())
        if temp == self.invalidTemp:
            self.lowTempError.config(fg='red')       
        else:
            self.lowTempError.config(fg='#F0F0F0')
        
        
    def changeHighTemp(self=None):
        temp = self.checkTemp(self.highTempTV.get())
        if temp == self.invalidTemp:
            self.highTempError.config(fg='red')       
        else:
            self.highTempError.config(fg='#F0F0F0')
            
    def checkTemp(self,temp):
        try:
            temp = int(temp)
        except ValueError:
            temp = self.invalidTemp
            
        return temp
import os
import glob
import Tkinter as tk
import tkFileDialog

def getDir(initialDir=""):
    root = tk.Tk()
    root.withdraw()
    if(initialDir != ""):
        file_path = tkFileDialog.askdirectory(initialdir=initialDir)
    else:
        file_path = tkFileDialog.askdirectory()
    root.destroy()

    return file_path
    
    
dirName = getDir()+ '/'
print(dirName)

extension = input("Input a filetype (ex .png): ")
currentSuffix = input("Input a suffix to remove(ex _ir): ")
list = glob.glob(dirName+ '*' + currentSuffix+extension)
suffix = input("Input a file suffix to replace with (ex: _IR) :")
for s in list:
    print(s)
    newName = s.replace(currentSuffix+extension,"")+suffix+extension
    print(newName)
    os.rename(s,newName)
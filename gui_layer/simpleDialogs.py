#!/usr/bin/env python
import Tkinter as tk
import tkFileDialog

from profileDialogs import saveProfileDialog

def getDir(initialDir=""):
    root = tk.Tk()
    root.withdraw()
    if(initialDir != ""):
        file_path = tkFileDialog.askdirectory(initialdir=initialDir)
    else:
        file_path = tkFileDialog.askdirectory()
    root.destroy()

    return file_path

    
def getFile(initialDir=""):
    root = tk.Tk()
    root.withdraw()
    if(initialDir != ""):
        file_path = tkFileDialog.askopenfilename(initialdir=initialDir)
    else:
        file_path = tkFileDialog.askopenfilename()
    root.destroy()

    return file_path
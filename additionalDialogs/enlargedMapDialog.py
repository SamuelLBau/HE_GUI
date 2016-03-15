import Tkinter as tk
import os
import sys

#from mapFrame import mapFrame
from QGISmapFrame import QGISmapFrame


class enlargedMapDialog(tk.Toplevel):
    maxWidth = 1000.0
    maxHeight = 600.0
    mapFrame = 0
    def __init__(self,master=None,tiffImagePath="",pointList=[],curPoint=[0,0]):
        tk.Toplevel.__init__(self,bg='#F0F0F0')
        self.mapFrame = QGISmapFrame(self,tiffImagePath,pointList,curPoint)
        self.title("Enlarge map of the area")
        self.mapFrame.grid()
        
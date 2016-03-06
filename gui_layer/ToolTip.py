from Tkinter import *

class ToolTip(object):
#Note: SB did not write this, this is copied directly from
#http://www.voidspace.org.uk/python/weblog/arch_d7_2006_07_01.shtml#e387

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        #print(type(self.widget))    
        #print self.widget.bbox(0)
        #x, y, cx, cy = self.widget.bbox(1)
        #I was getting Nonetype from widget.bbox, so I disabled the tooltip's ability to follow cursor
        x = self.widget.winfo_rootx()-130# +27 + x #This is hardcoded, should change to be half of TT length
        y = self.widget.winfo_rooty() +27# + y + cy
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle",
                       "style", tw._w,
                       "help", "noActivates")
        except TclError:
            pass
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
            
    def destroyTip(self):
        self.tipwindow.destroy()
        self.tipwindow = None

def createToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
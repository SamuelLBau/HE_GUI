#!/usr/bin/env python
import Tkinter as tk
import os
import sys

from PIL import Image, ImageTk



class doubleImageDialog(tk.Toplevel):
    visImagePath = ""
    irImagePath = ""
    firstImageFrame = 0     #Currently will just be frames that hold
    secondImageFrame = 0
    
    linkImages = False
    prevImageFunc = 0
    nextImageFunc = 0
    
    def __init__(self,visImagePath,irImagePath,master=None,PIC=0,NIC=0):
        self.prevImageFunc = PIC
        self.nextImageFunc = NIC
        self.visImagePath = visImagePath
        self.irImagePath = irImagePath
    
        tk.Toplevel.__init__(self,bg='#F0F0F0')
        self.title("Enlarged Image Viewer")
        self.placeFrames()
        
        
        
    def placeFrames(self):
        
        self.firstImageFrame = panZoomFrame(self,self.visImagePath,self.frame1Updated,PIC=self.prevImageFunc,NIC=self.nextImageFunc)
        self.secondImageFrame = panZoomFrame(self,self.irImagePath,self.frame2Updated)
        
        self.firstImageFrame.grid(row=0,column=0)
        self.secondImageFrame.grid(row=0,column=1)
        
    def frame1Updated(self,value):
    
        #Value is a string representation of what frame1did
        if(value == 'link-images'):
            self.linkImages = not self.linkImages
            #TODO LOGGER
            #print(self.linkImages)
            self.firstImageFrame.changeLinked(value=self.linkImages,update=False)
            self.secondImageFrame.changeLinked(value=self.linkImages,update=False)
            
        if(self.linkImages == False):
            return
        #Only reaches here if images should be linked
        if(value == 'reset'):
            self.secondImageFrame.resetImage(update=False)
        elif(value == 'rotate-cw'):
            self.secondImageFrame.rotateCW(update=False)
        elif(value == 'rotate-ccw'):
            self.secondImageFrame.rotateCCW(update=False)
        elif(value == 'zoom-in'):
            self.secondImageFrame.zoomIn(update=False)
        elif(value == 'zoom-out'):
            self.secondImageFrame.zoomOut(update=False)
        elif(value == 'pan-up'):
            self.secondImageFrame.panUp(update=False)
        elif(value == 'pan-down'):
            self.secondImageFrame.panDown(update=False)
        elif(value == 'pan-left'):
            self.secondImageFrame.panLeft(update=False)
        elif(value == 'pan-right'):
            self.secondImageFrame.panRight(update=False)
            
    def frame2Updated(self,value):
        #Value is a string representation of what frame1did
        if(value == 'link-images'):
            self.linkImages = not self.linkImages
            #TODO LOGGER
            #print(self.linkImages)
            self.firstImageFrame.changeLinked(value=self.linkImages,update=False)
            self.secondImageFrame.changeLinked(value=self.linkImages,update=False)
            
        if(self.linkImages == False):
            return
        #Only reaches here if images should be linked
        if(value == 'reset'):
            self.firstImageFrame.resetImage(update=False)
        elif(value == 'rotate-cw'):
            self.firstImageFrame.rotateCW(update=False)
        elif(value == 'rotate-ccw'):
            self.firstImageFrame.rotateCCW(update=False)
        elif(value == 'zoom-in'):
            self.firstImageFrame.zoomIn(update=False)
        elif(value == 'zoom-out'):
            self.firstImageFrame.zoomOut(update=False)
        elif(value == 'pan-up'):
            self.firstImageFrame.panUp(update=False)
        elif(value == 'pan-down'):
            self.firstImageFrame.panDown(update=False)
        elif(value == 'pan-left'):
            self.firstImageFrame.panLeft(update=False)
        elif(value == 'pan-right'):
            self.firstImageFrame.panRight(update=False)
            
            
class panZoomFrame(tk.Frame):

    #BEGIN CONFIG
    #These are used if the program can't determine size of screen
    defaultMaxHeight = 600.0
    defaultMaxWidth = 600.0
    #These are the offsets, adjust them to change the maximum size of the enlarged images
    #self.maxWidth = (root.winfo_screenwidth() * self.maxWidthOffset)
    #self.maxHeight = root.winfo_screenheight()- self.maxHeightOffset
    maxWidthOffset = .4
    maxHeightOffset = 150
    
    
    #END CONFIG

    #Use temp variable before se.f.photoImage
    imageOriginalSize = 0
    imageOriginalCenter = 0
    originalRotation = 0
    originalImage = 0
    
    photoImage = 0
    zoomFactor = 1      #This is for calculations
    imageCenter = 0     #This is for calculations
    imageRotation = 0   #This is for calculations
    imageSize = 0       #This is for calculations, not visual
    
    visImageSize = 0
    
    defaultMaxHeight = 600.0
    defaultMaxWidth = 600.0
    zoomFactorValue = 1.5   #How much does each click zoom 
    panFactorValue = .5     #How much does a pan offset image
    
    image = 0
    mainCanvas = 0
    imagePath = ""
    
    imagesLinkedButton = 0
    rotateCWButton = 0
    rotateCCWButton = 0
    zoomInButton = 0
    zoomOutButton = 0
    panUpButton = 0
    panDownButton = 0
    panLeftButton=0
    panRightButton=0
    resetButton = 0
    prevImageButton = 0
    nextImageButton = 0
    
    updateTopFrameFunc = 0
    prevItemFunc = 0
    nextItemFunc = 0
    parent = 0
    def __init__(self,master,imagePath,updateFunc=0,PIC=0,NIC=0):
        self.parent = master
        self.prevItemFunc = PIC
        self.nextItemFunc = NIC
        tk.Frame.__init__(self,master,bg='#F0F0F0')
        self.imagePath = imagePath
        self.updateTopFrameFunc = updateFunc
        
        self.getMaxSizes()
        
        self.setupWidgets()
        self.placeWidgets()
        
        self.loadImage()
        self.displayImage()
        
    def loadImage(self):
    #Load image should just load the image into memory, it will not resize it,
    #resizing and checks will be done by display
        path = self.imagePath
        if(not os.path.exists(path)):
            #TODO LOGGER
            print("WARNING: Enlarged image dialog, failed to set image at path: %s " %(path))
            path = self.defaultImagePath
            #TODO LOGGER
            #print("NOTE: Image not found, using default image")
        #TODO LOGGER
        #print("Setting image at path: %s " %(path))
        
        self.imagePath = path       
        self.originalImage = Image.open(self.imagePath)
        #self.image = self.originalImage
        
        imSize = self.originalImage.size #[width, height]
        
 
        #self.originalImage = self.originalImage.resize(imSize, Image.ANTIALIAS)
        #self.originalImage = ImageTk.PhotoImage(file=self.imagePath)
        self.image = self.originalImage
        
        #imSize = self.image.size #[width, height]
        
        self.zoomFactor = 1
        self.imageCenter = [imSize[0]/2, imSize[1] / 2]
        
        self.imageOriginalSize = imSize
        self.imageOriginalCenter = self.imageCenter
        
        self.imageSize = imSize
        self.imageRotation = 0
        
        
    def displayImage(self):
        #Rotate disabled
#-------#Begin, given imageCenter,imageZoom, imageRotation
        
        if(self.zoomFactor < 1):
            self.zoomFactor = 1
            
        self.imageRotation = self.imageRotation % 360 #TODO: Need to check this
        
        image = self.originalImage
        #image = image.rotate(self.imageRotation)
        imSize = [image.size[0]/self.zoomFactor, image.size[1]/self.zoomFactor]
        self.imageSize = imSize
        #print("self.imageSize")
        #print(self.imageSize)
#-------#Check Bounds, size, this should just prepare to crop image
            #Changes center if necessary
        edgeBounds = self.checkBounds()
        #print(edgeBounds)
        #Crop image and display
        
        #print("IMsize before crop")
        #print(image.size)
        image = image.crop(edgeBounds)
        #print("IMsize after crop")
        #print(image.size)
        
#-------#self.image edited directly, assume already cropped / set

        imSize = image.size
        #print("Before Check: IMsize 0 = %d, ImSize[1] = %d" %(imSize[0],imSize[1]))
        imSize = self.sizeCheck(imSize) #This check maximizes useof frame space
        #print("After Check: IMsize 0 = %d, ImSize[1] = %d" %(imSize[0],imSize[1]))
        #self.mainCanvas.create_image(1,1,image=self.image,anchor='nw')
        self.image = image.resize(imSize,Image.ANTIALIAS)
        self.mainCanvas.config(width=imSize[0],height=imSize[1])
        
        self.photoImage = ImageTk.PhotoImage(image=self.image)
        
        self.mainCanvas.create_image(1,1,image=self.photoImage,anchor='nw')
        
        
       # self.mainCanvas.create_image(1,1,image=self.image,anchor='nw')
        #print("IMsize 0 = %d, ImSize[1] = %d" %(imSize[0],imSize[1]))
        #self.mainCanvas.config(width=imSize[0],height=imSize[1])
        self.update()
        
        
        
        
    def setupWidgets(self):
        self.mainCanvas = tk.Canvas(self)
        
        self.rotateCWButton = tk.Button(self,text="Rotate CW",command=self.rotateCW)
        self.rotateCCWButton = tk.Button(self,text="Rotate CCW",command=self.rotateCCW)
        
        self.zoomInButton = tk.Button(self,text="Zoom in",command=self.zoomIn)
        self.zoomOutButton = tk.Button(self,text="Zoom out",command=self.zoomOut)
        
        self.panUpButton = tk.Button(self,text="Pan Up",command=self.panUp)
        self.panDownButton = tk.Button(self,text="Pan Down",command=self.panDown)
        self.panLeftButton = tk.Button(self,text="Pan Left",command=self.panLeft)
        self.panRightButton = tk.Button(self,text="Pan Right",command=self.panRight)
        
        self.resetButton = tk.Button(self,text="Reset",command=self.resetImage)
        
        self.imagesLinkedButton = tk.Button(self,text="Images Not Linked",command=self.changeLinked)
        
        self.prevImageButton = tk.Button(self,text="Previous image",command=self.prevImage)
        self.nextImageButton = tk.Button(self,text="Next image",command=self.nextImage)
    def placeWidgets(self):
        #See notebook for designplan
        self.mainCanvas.grid(row=0,column=0,columnspan = 20,sticky='wens')
        
        #self.rotateCWButton.grid(row=1,column=1,sticky='we')
        #self.rotateCCWButton.grid(row=1,column=3,sticky='we')
        self.imagesLinkedButton.grid(row=2,sticky='we')
        self.zoomInButton.grid(row=1,column=0,sticky='we')
        self.zoomOutButton.grid(row=3,column=0,sticky='we')
        
        self.panUpButton.grid(row=1,column=2,sticky='we')
        self.panDownButton.grid(row=3,column=2,sticky='we')
        self.panLeftButton.grid(row=2,column=1,sticky='we')
        self.panRightButton.grid(row=2,column=3,sticky='we')
        
        self.resetButton.grid(row=2,column=2,sticky='we')
        
        
        #TODO ENABLE
        if(False):
            if(self.prevItemFunc != 0):
                self.prevImageButton.grid(row=1,column=4,sticky='we')
            if(self.nextItemFunc != 0):
                self.nextImageButton.grid(row=3,column=4,sticky='we')
    def prevImage(self):
        if(self.prevItemFunc != 0):
            self.prevItemFunc(self)
    def nextImage(self):
        if(self.nextItemFunc !=0):
            self.nextItemFunc(self)
    def resetImage(self,update=True):
        self.zoomFactor = 1
        self.imageCenter = self.imageOriginalCenter
        self.imageRotation = self.originalRotation
        self.displayImage()
        if(self.updateTopFrameFunc != 0 and update):
            self.updateTopFrameFunc('reset')
    def rotateCW(self,update=True):
        print("TODO: implement everything")
        if(self.updateTopFrameFunc != 0 and update):
            self.updateTopFrameFunc('rotate-cw')
         
    def rotateCCW(self,update=True):
        print("TODO: implement everything")
        if(self.updateTopFrameFunc != 0 and update):
            self.updateTopFrameFunc('rotate-ccw')

    def zoomIn(self,update=True):
        #TODO LOGGER
        #print("Zooming in")
        #Image center does not change, only bounds do
        self.zoomFactor = self.zoomFactor * self.zoomFactorValue
        self.displayImage()
        if(self.updateTopFrameFunc != 0 and update):
            self.updateTopFrameFunc('zoom-in')
        
    def zoomOut(self,update=True):
        #TODO LOGGER
        #print("Zooming out")
        #Image center may change, if zooming out
        #Do nothing if zoom factor is already 1
        self.zoomFactor = self.zoomFactor / self.zoomFactorValue
        self.displayImage()
        if(self.updateTopFrameFunc != 0 and update):
            self.updateTopFrameFunc('zoom-out')
    def panUp(self,update=True):
        #Move image up, unless at top edge
        #TODO LOGGER
        #print("Panning up")
        newImageX = self.imageCenter[0]
        newImageY = self.imageCenter[1] - self.imageSize[1]*self.panFactorValue
        self.imageCenter = [newImageX, newImageY]
        self.displayImage()
        if(self.updateTopFrameFunc != 0 and update):
            self.updateTopFrameFunc('pan-up')
        
    def panDown(self,update=True):
        #Move image down, unless at bottom edge
        #TODO LOGGER
        #print("Panning down")
        newImageX = self.imageCenter[0]
        newImageY = self.imageCenter[1] + self.imageSize[1]*self.panFactorValue
        self.imageCenter = [newImageX, newImageY]
        self.displayImage()
        if(self.updateTopFrameFunc != 0 and update):
            self.updateTopFrameFunc('pan-down')
        
    def panLeft(self,update=True):
        #Move image left, unless at left edge
        #TODO LOGGER
        #print("Panning left")
        newImageX = self.imageCenter[0] - self.imageSize[0]*self.panFactorValue
        newImageY = self.imageCenter[1]
        self.imageCenter = [newImageX, newImageY] 
        self.displayImage()
        if(self.updateTopFrameFunc != 0 and update):
            self.updateTopFrameFunc('pan-left')
        
    def panRight(self,update=True):
        #Move image right, unless at right edge
        #TODO LOGGER
        #print("Panning right")
        newImageX = self.imageCenter[0] + self.imageSize[0]*self.panFactorValue
        newImageY = self.imageCenter[1]
        self.imageCenter = [newImageX, newImageY] 
        self.displayImage()
        if(self.updateTopFrameFunc != 0 and update):
            self.updateTopFrameFunc('pan-right')
    def changeLinked(self,value=None,update=True):
        if(update):
            self.updateTopFrameFunc('link-images')
        
        if(value != None):
            if(value == True):
                self.imagesLinkedButton.config(text="Images Linked")
            else:
                self.imagesLinkedButton.config(text="Images Not Linked")
    
    def sizeCheck(self,imSize):
        newWidth = imSize[0]
        newHeight = imSize[1]
    
        if(imSize[0] > self.maxWidth):
            ratio = imSize[0] / self.maxWidth
            newWidth = self.maxWidth
            newHeight = imSize[1] / ratio
            
        if(imSize[1] > self.maxHeight):
            ratio = imSize[1] / self.maxHeight
            newHeight = self.maxHeight
            newWidth = imSize[0] / ratio
            
        imSize = [newWidth, newHeight]    
        widthRatio = float(imSize[0]) / self.maxWidth
        heightRatio = float(imSize[1]) / self.maxHeight
        
        #These are already maxed out at 1,
        #These calculations should not be able to make them bigger
        #Than the max values
        newWidth = imSize[0]
        newHeight = imSize[1]
        if(heightRatio > widthRatio):
            newWidth = imSize[0] / heightRatio
            newHeight = imSize[1] / heightRatio
        else:
            newWidth = imSize[0] / widthRatio
            newHeight = imSize[1] / widthRatio
        #TODO LOGGER 
        #print("New width: %f"%(newWidth))
        #print("New height: %f"%(newHeight))
        return [int(newWidth), int(newHeight)]
        
    def checkBounds(self):
        #TODO: This needs to move imageCenter
        #This will ensure the final image is not place out of bounds
        #These are in relation to the original image
        #print("Image Center Before boundCheck")
        #print(self.imageCenter)
        #print("self.imageSize Before boundCheck")
        #print(self.imageSize)
        leftEdge = self.imageCenter[0]-self.imageSize[0]/2
        rightEdge = self.imageCenter[0]+self.imageSize[0]/2
        
        bottomEdge = self.imageCenter[1]-self.imageSize[1]/2
        topEdge = self.imageCenter[1]+self.imageSize[1] /2
        
         # Due to zoom factor minimum being 1, no additional checks
         #Should be needed to ensure the second edge is pushed out of bounds
        imageCenterY = self.imageCenter[1]
        imageCenterX = self.imageCenter[0]
         
        if(bottomEdge < 0):
            imageCenterY =self.imageCenter[1] - bottomEdge
            #topEdge = topEdge + bottomEdge # Due to zoom factor minimum being 1, this shouldn't be issue
            #bottomEdge = 0
        self.imageCenter = [imageCenterX, imageCenterY] 
        #print("ImageCenter [%d,%d] " %(self.imageCenter[0],self.imageCenter[1])) 
        if(topEdge > self.imageOriginalSize[1]):
            imageCenterY =self.imageCenter[1] -(topEdge - self.imageOriginalSize[1])
            #bottomEdge = bottomEdge -(topEdge - self.imageOriginalSize[1])
            #topEdge = self.imageOriginalSize[1]
        self.imageCenter = [imageCenterX, imageCenterY] 
        #print("ImageCenter [%d,%d] " %(self.imageCenter[0],self.imageCenter[1]))    
        if(leftEdge < 0):
            imageCenterX = self.imageCenter[0] - leftEdge
            #rightEdge = rightEdge + leftEdge # Due to zoom factor minimum being 1, this shouldn't be issue
            #leftEdge = 0
        self.imageCenter = [imageCenterX, imageCenterY] 
        #print("ImageCenter [%d,%d] " %(self.imageCenter[0],self.imageCenter[1])) 
        if(rightEdge > self.imageOriginalSize[0]):
            imageCenterX = self.imageCenter[0] -(rightEdge - self.imageOriginalSize[0])
            #leftEdge = leftEdge -(rightEdge - self.imageOriginalSize[0])
            #rightEdge = self.imageOriginalSize[0]
        self.imageCenter = [imageCenterX, imageCenterY] 
        #print("ImageCenter [%d,%d] " %(self.imageCenter[0],self.imageCenter[1])) 
        self.imageCenter = [imageCenterX, imageCenterY]   
            #This order set by not on URL
            #http://stackoverflow.com/questions/20361444/cropping-an-image-with-python-pillow
            
        leftEdge = self.imageCenter[0]-self.imageSize[0]/2
        rightEdge = self.imageCenter[0]+self.imageSize[0]/2
        
        bottomEdge = self.imageCenter[1]-self.imageSize[1]/2
        topEdge = self.imageCenter[1]+self.imageSize[1] /2    
        #print("Image Center After boundCheck")
        #print(self.imageCenter)
        #print("self.imageSize After boundCheck")
        #print(self.imageSize)
        return [int(leftEdge), int(bottomEdge), int(rightEdge), int(topEdge)]

    def checkImage():
        #This function checks all bounds and sizes, the panzoom, etc. functions should only try changing values
        edgeBounds = self.checkBounds()
        #print("Image Size:")
        #print(self.image.size)
        self.image = self.originalImage.crop(edgeBounds)
        #print("Image Size:")
        #print(self.image.size)
        #print("EdgeBounds")
        #print(edgeBounds)
    def getMaxSizes(self):
        try:
            root = tk.Tk()
            self.maxWidth = (root.winfo_screenwidth() * self.maxWidthOffset)
            self.maxHeight = root.winfo_screenheight()- self.maxHeightOffset
            #TODO LOGGER
            print("NOTE: Setting maxWidth to %f"%(self.maxWidth))
            print("NOTE: Setting maxHeight to %f"%(self.maxHeight))
            root.destroy()
        except:
            #TODO LOGGER
            print("NOTE: Could not load screen sizes")
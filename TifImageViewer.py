import wx
import cv2
import numpy as np
import os

class ImageViewerFrame(wx.Frame):
    def __init__(self,parent, title):
        super(ImageViewerFrame,self).__init__(None,title=title)
        
        self.panel = myPanel(None,self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel, 1, wx.EXPAND|wx.ALL, 2)
        self.SetSizer(self.sizer)
        self.CreateStatusBar()
        self.SetStatusText("Made for Delmic")
        self.createMenuBar()
        self.Show()

        self.Bind(wx.EVT_SIZE, self.onResize)
        
        

    def createMenuBar(self):
        """
        A menu bar for our frame
        """
        
        fileMenu = wx.Menu()
        openItem = fileMenu.Append(-1,"&Open...\tCtrl-J",
                                   "Open a new image file")
        fileMenu.AppendSeparator()
        
        exitItem = fileMenu.Append(wx.ID_EXIT)

        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu,"&File")
        menuBar.Append(helpMenu,"&Help")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU,self.onExit,exitItem)
        self.Bind(wx.EVT_MENU,self.onAbout,aboutItem)
        self.Bind(wx.EVT_MENU,self.onOpenFile,openItem)
        

    def onExit(self,event):
        self.Close(True)

    def onAbout(self,event):
        
        wx.MessageBox("About"+"\n\nImage Viewer developed by Mounir AFIFI for Delmic"
                      +"\n\nPython version: 2.7.12"+
                      "\n\nDate: Feb 08, 2018")

    def onOpenFile(self,event):
        wildcard = "All files (*.*) | *.*|(*.jpg)|*.jpg|(*.png)|*.png|(*.tif)|*.tif|(*.tiff)|*.tiff"
        openFileDialog = wx.FileDialog(self, "Open", "", "", 
                                       wildcard, 
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        modal = openFileDialog.ShowModal()
        if modal == wx.ID_OK:
            self.panel.Destroy()
            self.panel = myPanel(openFileDialog.GetPath(),self)
            
        
        openFileDialog.Destroy()

    def onResize(self, event):
                
        try:
            f = self.panel.filename
            self.panel.Hide()
            self.panel = myPanel(f,self)
        except Exception,e:
            print(str(e))
    
    

class myPanel(wx.Panel):
    def __init__(self,filename,frame):
        super(myPanel,self).__init__(frame)
        
        self.filename = filename
        frame_width,frame_height = frame.GetSize()
        self.SetSize((frame_width,frame_height))
        if(self.filename is not None):
            try:
                extension = self.filename.split('.')[-1]
                #we bypass the issue of TIF images by converting the image
                #to a temporary jpg file
                if(extension.lower() in ['tiff','tif']):
                    im = cv2.imread(self.filename).astype(np.uint8)
                    cv2.imwrite('temp.jpg', im)
                    self.filename = 'temp.jpg'
                
                self.image = wx.Image(self.filename,wx.BITMAP_TYPE_ANY)
                
                image_width,image_height = get_new_image_size(self.image.GetSize(),frame.GetSize())
                self.image.Rescale(image_width,image_height)
                
                self.image_control = wx.StaticBitmap(self, wx.ID_ANY, 
                                             wx.Bitmap(self.image))
                
            
            except Exception,e:
                print(str(e))
        
def get_new_image_size(image_size,frame_size):
    image_width,image_height = image_size
    frame_width,frame_height = frame_size
    image_ratio = image_height/float(image_width)
    if(image_ratio<1):
        image_frame_ratio = frame_width/float(image_width)
        
        if(image_height*image_frame_ratio>frame_height):
            image_height = frame_height
            
        else:
            image_height = image_height*image_frame_ratio
            
        image_width = int(image_height/image_ratio)
        
        
    else:
        image_frame_ratio = frame_height/float(image_height)
        
        if(image_width*image_frame_ratio>frame_width):
            image_width = frame_width

        else:
            image_width = image_width*image_frame_ratio
            
        image_height = int(image_width*image_ratio)
    
    return image_width,image_height
        

if __name__ == '__main__':
    app = wx.App()
    imageViewerFrame = ImageViewerFrame(None, "Delmic Image Viewer")
    app.MainLoop()

    #delete temporary image file if it exists
    try:
        os.remove('temp.jpg')
    except:
        pass
    
    

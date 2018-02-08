import wx
import cv2
import numpy as np
import os

class ImageViewer(wx.App):
    def __init__(self,redirect=False, filename=None):
        super(ImageViewer,self).__init__(redirect,filename)
        
        self.frame = myFrame(None,title="Image Viewer")
        
        self.createMenuBar()

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

        self.frame.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU,self.onExit,exitItem)
        self.Bind(wx.EVT_MENU,self.onAbout,aboutItem)
        self.Bind(wx.EVT_MENU,self.onOpenFile,openItem)
        

    def onExit(self,event):
        self.frame.Close(True)

    def onAbout(self,event):
        
        wx.MessageBox("About"+"\n\nImage Viewer developed by Mounir AFIFI for Delmic"
                      +"\n\nPython version: 2.7.12"+
                      "\n\nDate: Feb 08, 2018")

    def onOpenFile(self,event):
        wildcard = "All files (*.*) | *.*|(*.jpg)|*.jpg|(*.png)|*.png|(*.tif)|*.tif|(*.tiff)|*.tiff"
        openFileDialog = wx.FileDialog(self.frame, "Open", "", "", 
                                       wildcard, 
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        ofd = openFileDialog.ShowModal()
        if ofd == wx.ID_OK:
            self.frame.panel.Destroy()
            self.frame.panel = myPanel(openFileDialog.GetPath(),self.frame)
            
        
        openFileDialog.Destroy()

    
        
class myFrame(wx.Frame):
    def __init__(self,value,title):
        super(myFrame,self).__init__(None,title=title)
        self.panel = myPanel(None,self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND|wx.ALL, 2)
        self.SetSizer(sizer)
        self.CreateStatusBar()
        self.SetStatusText("Made for Delmic")
        
        self.Show()

        self.Bind(wx.EVT_SIZE, self.onResize)
    
    def onResize(self, event):
                
        try:
            f = self.panel.filename
            self.panel.Hide()
            self.panel = myPanel(f,self)
        except Exception,e:
            print(str(e))
        
        
        self.Refresh()
        self.Layout()
    

class myPanel(wx.Panel):
    def __init__(self,filename,frame):
        super(myPanel,self).__init__(frame)
        self.sizer = wx.GridBagSizer(5,5)
        self.filename = filename
        frame_width,frame_height = frame.GetSize()
        self.SetSize((frame_width,frame_height))
        if(self.filename!=None):
            try:
                extension = self.filename.split('.')[-1]
                
                if(extension in ['tiff','tif','TIF','TIFF']):
                    im = cv2.imread(self.filename).astype(np.uint8)
                    cv2.imwrite('temp.jpg', im)
                    self.filename = 'temp.jpg'
                
                self.image = wx.Image(self.filename,wx.BITMAP_TYPE_ANY)
                
                image_width,image_height = self.image.GetSize()
                image_ratio = image_height/float(image_width)
                if(image_ratio<1):
                    image_frame_ratio = frame_width/float(image_width)
                    
                    if(image_height*image_frame_ratio>frame_height):
                        image_height = frame_height
                        
                    else:
                        image_height = image_height*image_frame_ratio
                        
                    image_width = int(image_height/image_ratio)
                    self.image.Rescale(image_width,image_height)
                    
                else:
                    image_frame_ratio = frame_height/float(image_height)
                    
                    if(image_width*image_frame_ratio>frame_width):
                        image_width = frame_width

                    else:
                        image_width = image_width*image_frame_ratio
                        
                    image_height = int(image_width*image_ratio)
                    self.image.Rescale(image_width,image_height)
                
                self.image_control = wx.StaticBitmap(self, wx.ID_ANY, 
                                             wx.Bitmap(self.image))
                self.sizer.Add(self.image_control,pos=(0,0),span=(5,5), flag=wx.EXPAND|wx.ALL, border=2)
                self.SetSizer(self.sizer)
                sizer = wx.BoxSizer(wx.VERTICAL)
                sizer.Add(self, 1, wx.EXPAND|wx.ALL, 2)
                frame.SetSizer(sizer)
                
            except Exception,e:
                print(str(e))
        
    
        

if __name__ == '__main__':
    imageViewer = ImageViewer()
    imageViewer.MainLoop()

    #delete temporary image file if it exists
    try:
        os.remove('temp.jpg')
    except:
        pass
    
    

import wx

class TifImageViewer(wx.App):
    def __init__(self,redirect=False, filename=None):
        super(TifImageViewer,self).__init__(redirect,filename)
        self.frame = wx.Frame(None,title="Tif Image Viewer")
        self.panel = myPanel(None,self.frame)
        #wx.InitAllImageHandlers()
        self.createMenuBar()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND|wx.ALL, 2)
        self.frame.SetSizer(sizer)
        self.frame.CreateStatusBar()
        self.frame.SetStatusText("Made for Delmic")
        print(self.frame.GetSize())
        print(self.panel.GetSize())
        self.frame.Show()

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
        #print(help(wx.MessageBox))
        wx.MessageBox("About"+"\n\nImage Viewer developed by Mounir AFIFI for Delmic"
                      +"\n\nPython version: 2.7.12"+
                      "\n\nDate: Jan 31, 2018")

    def onOpenFile(self,event):
        wildcard = "Image files (*.jpg)|*.jpg|(*.png)|*.png|(*.tif)|*.tif|(*.tiff)|*.tiff"
        openFileDialog = wx.FileDialog(self.frame, "Open", "", "", 
                                       wildcard, 
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        ofd = openFileDialog.ShowModal()
        if ofd == wx.ID_OK:
            self.panel = myPanel(openFileDialog.GetPath(),self.frame)
            
        
        openFileDialog.Destroy()
        

class myPanel(wx.Panel):
    def __init__(self,filename,frame):
        super(myPanel,self).__init__(frame)
        self.sizer = wx.GridBagSizer(5,5)
        if(filename!=None):
            try:
                
                self.image = wx.Image(filename,wx.BITMAP_TYPE_ANY)
                self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, 
                                             wx.Bitmap(self.image))
                W,H = frame.GetSize()
                self.SetSize((W,H))
                self.image.Scale(W,H)
                self.sizer.Add(self.imageCtrl,pos=(0,0),span=(5,5), flag=wx.EXPAND|wx.ALL, border=2)
                self.SetSizer(self.sizer)
                
            except Exception,e:
                print(str(e))
    
        

if __name__ == '__main__':
    imageViewer = TifImageViewer()
    imageViewer.MainLoop()
    

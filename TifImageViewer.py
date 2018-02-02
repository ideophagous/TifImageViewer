import wx

class TifImageViewer(wx.App):
    def __init__(self,redirect=False, filename=None):
        super(TifImageViewer,self).__init__(redirect,filename)
        self.frame = wx.Frame(None,title="Tif Image Viewer")
        self.panel = wx.Panel(self.frame)
        self.image = wx.Image(500,500)
        self.frame.Show()
        



if __name__ == '__main__':
    imageViewer = TifImageViewer()
    imageViewer.MainLoop()
    

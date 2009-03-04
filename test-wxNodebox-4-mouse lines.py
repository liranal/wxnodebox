#!/usr/bin/python
# -*- coding: iso-8859-1 -*- 

import wx
import math

try:
    import wx.lib.wxcairo
    import cairo
    haveCairo = True
except ImportError:
    haveCairo = False

#import NodeBox
from WxNodeBox import *
    
def run():
    fill(0.2)
    rect(10, 20, 60, 40)
    
path = []
    
class TestPanel(wx.Panel):
    def __init__(self, parent): #, log):
        self.log = None # log
        wx.Panel.__init__(self, parent, -1)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        wx.EVT_ERASE_BACKGROUND(self, self.OnEraseBackground)

        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.position = (0,0)
        self.ctx = None
        self.mousedown = False
        self.MOUSEX = 0
        self.MOUSEY = 0
        
    def OnPaint(self, evt):
        #dc = wx.PaintDC(self)
        dc = wx.BufferedPaintDC(self)
        # use PrepateDC to set position correctly
        self.PrepareDC(dc)
        # we need to clear the dc BEFORE calling PrepareDC
        #dc.BeginDrawing()
        dc.SetBackground(wx.Brush('white'))
        dc.Clear()
        self.Render(dc)
        #dc.EndDrawing()

    def OnEraseBackground(self, event):
        pass # Or None

    def OnMouseLeftDown(self, event):
        self.position = event.GetPosition()
        self.MOUSEX = self.position[0]
        self.MOUSEY = self.position[1]
        self.mousedown = True
        self.Refresh()

    def OnMouseLeftUp(self, event):
        self.position = event.GetPosition()
        self.MOUSEX = self.position[0]
        self.MOUSEY = self.position[1]
        self.mousedown = False
        self.Refresh()
        
    def OnMouseMotion(self, event):
        self.position = event.GetPosition()
        self.MOUSEX = self.position[0]
        self.MOUSEY = self.position[1]
        self.Refresh()

    def Render(self, dc):
        # Draw some stuff on the plain dc
        sz = self.GetSize()
        # now draw something with cairo
        #NodeBox.createGraphContext(dc)
        #if self.ctx == None:
        ctx = Context()
        ctx.createGraphContext(dc)
        #self.ctx = ctx
        #else:
        #    ctx = self.ctx
        
        from math import pi
        
        global path
        
        ctx.nofill()
        ctx.stroke(0)
        ctx.rect(0,0,40,40)

        ctx.autoclosepath(False)
    
        if self.mousedown:
            pt = Point(self.MOUSEX, self.MOUSEY)
            path.append(pt)
        
        if len(path) > 0:
            first = True
            for pt in path:
                if first:
                    ctx.beginpath(pt.x, pt.y)
                    first = False
                else:
                    ctx.lineto(pt.x, pt.y)
            ctx.endpath()
        
class Frame(wx.Frame):
    """Frame class that displays an image."""

    def __init__(self, image, parent=None, id=-1,
                 pos=wx.DefaultPosition, title='Hello, wxPython!'):
        """Create a Frame instance and display image."""
        #temp = image.ConvertToBitmap()
        #size = temp.GetWidth(), temp.GetHeight()
        size = 600, 500
        wx.Frame.__init__(self, parent, id, title, pos, size)
        panel = TestPanel(self)
        #panel = wx.Panel(self)
        #self.bmp = wx.StaticBitmap(parent=panel, bitmap=temp)
        self.SetClientSize(size)

class App(wx.App):
    """Application class."""

    def OnInit(self):
        #image = wx.Image('wxPython.jpg', wx.BITMAP_TYPE_JPEG)
        #self.frame = Frame(image)
        self.frame = Frame(None)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

def main():
    app = App()
    app.MainLoop()

if __name__ == '__main__':
    main()
    
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

from SceneData import *

def run():
    fill(0.2)
    rect(10, 20, 60, 40)
    
    
class TestPanel(wx.Panel):
    def __init__(self, parent): #, log):
        self.log = None # log
        wx.Panel.__init__(self, parent, -1)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        wx.EVT_ERASE_BACKGROUND(self, self.OnEraseBackground)

        self.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnMouseRightUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseRightDown)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.position = (0,0)
        self.mouseleftdown = False
        self.mouserightdown = False
        
        self.game = GameManager()
        self.game.initialize_world( "SceneData\\Level0.png")
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(40) # 1000 = 1 seconde
        
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
        self.mouseleftdown = True
        self.game.graphics.update_actor( self.MOUSEX, self.MOUSEY)

    def OnMouseLeftUp(self, event):
        self.position = event.GetPosition()
        self.MOUSEX = self.position[0]
        self.MOUSEY = self.position[1]
        self.mouseleftdown = False
        
    def OnMouseRightDown(self, event):
        self.position = event.GetPosition()
        self.MOUSEX = self.position[0]
        self.MOUSEY = self.position[1]
        self.mouserightdown = True
        self.game.graphics.update_actor_gunfire( self.MOUSEX, self.MOUSEY)

    def OnMouseRightUp(self, event):
        self.position = event.GetPosition()
        self.MOUSEX = self.position[0]
        self.MOUSEY = self.position[1]
        self.mouserightdown = False
        
    def OnMouseMotion(self, event):
        self.position = event.GetPosition()
        self.MOUSEX = self.position[0]
        self.MOUSEY = self.position[1]
        if self.mouseleftdown == True:
            self.game.graphics.update_actor( self.MOUSEX, self.MOUSEY)
        if self.mouserightdown == True:
            self.game.graphics.update_actor_gunfire( self.MOUSEX, self.MOUSEY)
        
    def Render(self, dc):
        # Draw some stuff on the plain dc
        self.game.draw_scene( dc)
        
    def OnTimer(self, event):
        #self.panel.SetBackgroundColour(wx.RED)
        #position = randrange(0, self.col_num-1, 1)
        #self.panel.SetBackgroundColour(self.colors[position])
        self.game.physics.turn()
        self.Refresh()
        
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
    
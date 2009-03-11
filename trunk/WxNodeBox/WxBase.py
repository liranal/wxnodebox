#!/usr/bin/python
# -*- coding: iso-8859-1 -*- 

import wx

class WxBase(wx.Panel):
    def __init__(self, parent, log):
        """ initialize all interaction components: mouse, refresh rate, keyboard
        """
        #self.log = None # log
        wx.Panel.__init__(self, parent, log)

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

    def test(self):
        a = 0
        return
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
from NodeBox import *
    
def run():
    fill(0.2)
    rect(10, 20, 60, 40)
    
    
class TestPanel(wx.Panel):
    def __init__(self, parent): #, log):
        self.log = None # log
        wx.Panel.__init__(self, parent, -1)

        self.Bind(wx.EVT_PAINT, self.OnPaint)


    def OnPaint(self, evt):
        #dc = wx.PaintDC(self)
        dc = wx.BufferedPaintDC(self)
        dc.SetBackground(wx.Brush('white'))
        dc.Clear()
        
        self.Render(dc)


    def Render(self, dc):
        # Draw some stuff on the plain dc
        sz = self.GetSize()
        # now draw something with cairo
        #NodeBox.createGraphContext(dc)
        ctx = Context()
        ctx.createGraphContext(dc)
        
        #fill(0.5,0.5,0.5)
        ctx.fill(1,0,0)
        ctx.rect(10,10,100,100,0.5)
        ctx.fill(0,0,1)
        ctx.rect(120,10,100,100,1)
        ctx.fill(0,1,0)
        ctx.oval(230,10,100,100)
        ctx.fill(0.5,0.5,0)
        ctx.oval(340,10,50,100)
        ctx.oval(390,10,50,100)
        ctx.fill(1,0,0)
        ctx.line(450,10,550,110)
        ctx.rect(560,10,100,100,0)

        ctx.nofill()
        ctx.stroke(1,0,0)
        ctx.rect(10,120,100,100,0.5)
        ctx.stroke(0,0,1)
        ctx.rect(120,120,100,100,1)
        ctx.stroke(0,1,0)
        ctx.strokewidth(3)
        ctx.oval(230,120,100,100)
        ctx.stroke(0.5,0.5,0)
        ctx.oval(340,120,50,100)
        ctx.oval(390,120,50,100)
        ctx.stroke(1,0,0)
        ctx.strokewidth(10)
        ctx.line(450,120,550,220)
        ctx.rect(560,120,100,100,0)
        
        ctx.fill(0.2, 0.2, 0.2)
        ctx.arrow(110, 280, 100)
        ctx.nofill()
        ctx.arrow(120, 280, -100)
        ctx.fill(0.1, 0.4, 0.6)
        ctx.arrow(230, 330, -100, ctx.FORTYFIVE)
        ctx.nofill()
        ctx.arrow(440, 230, 100, ctx.FORTYFIVE)
        ctx.stroke(0,1,0)
        ctx.strokewidth(1)
        ctx.star( 500, 280, 5, 50, 10)
        ctx.strokewidth(3)
        ctx.star( 610, 280, 6, 50, 40)
        
        points = [(10, 10), (90, 90), (350, 200)]
        for x, y in points:
            ctx.oval(x-2, y-2, 4, 4)
        ctx.nofill()
        ctx.stroke(0.2)
        ctx.autoclosepath(False)    
        path = ctx.findpath(points)
        ctx.drawpath(path)   
        
        ctx.nofill()
        ctx.stroke(1,0,0)
        ctx.strokewidth(1)
        ctx.rect(10,340,100,100,1)
        ctx.image("nodeboxicon.png", 10, 340, 100, 100, 0)
        #ctx.image("nodeboxicon.png", 250, 350, 100, 100)
        #ctx = wx.lib.wxcairo.ContextFromDC(dc)
        #node = NodeBox.Box()
        #node.rect(0, 10, 100, 100)
        #ctx.rectangle(0, 10, 100, 100)
        #ctx.stroke()
        
        ctx.stroke(0.2)
        ctx.beginpath(10, 10)
        ctx.lineto(40, 10)
        ctx.endpath()
        
        ctx.stroke(0)
        ctx.rect(30,60,80,80)
        ctx.translate(100,100)
        ctx.rect(20,40,80,80)
        ctx.translate(100,100)
        ctx.rect(20,40,80,80)
        #ctx.rotate(40)
        #ctx.rect(-20, -20, 40, 40)
        #ctx.rotate(10)
        #ctx.rect(30, 120, 40, 40)
        #ctx.rotate(10)
        #ctx.rect(30, 180, 40, 40)
        #ctx.rotate(10)
        #ctx.rect(30, 240, 40, 40)
        return
        
        #dc.SetPen(wx.Pen("navy", 1))
        #x = y = 0
        #while x < sz.width * 2 or y < sz.height * 2:
            #x += 20
            #y += 20
            #dc.DrawLine(x, 0, 0, y)
        
        ## now draw something with cairo
        #ctx = wx.lib.wxcairo.ContextFromDC(dc)
        #ctx.set_line_width(15)
        #ctx.move_to(125, 25)
        #ctx.line_to(225, 225)
        #ctx.rel_line_to(-200, 0)
        #ctx.close_path()
        #ctx.set_source_rgba(0, 0, 0.5, 1)
        #ctx.stroke()

        ## and something else...
        #ctx.arc(200, 200, 80, 0, math.pi*2)
        #ctx.set_source_rgba(0, 1, 1, 0.5)
        #ctx.fill_preserve()
        #ctx.set_source_rgb(1, 0.5, 0)
        #ctx.stroke()

        ## here's a gradient pattern
        #ptn = cairo.RadialGradient(315, 70, 25,
                                   #302, 70, 128)
        #ptn.add_color_stop_rgba(0, 1,1,1,1)
        #ptn.add_color_stop_rgba(1, 0,0,0,1)
        #ctx.set_source(ptn)
        #ctx.arc(328, 96, 75, 0, math.pi*2)
        #ctx.fill()

        ## Draw some text
        #face = wx.lib.wxcairo.FontFaceFromFont(
            #wx.FFont(10, wx.SWISS, wx.FONTFLAG_BOLD))
        #ctx.set_font_face(face)
        #ctx.set_font_size(60)
        #ctx.move_to(360, 180)
        #ctx.set_source_rgb(0, 0, 0)
        #ctx.show_text("Hello")

        ## Text as a path, with fill and stroke
        #ctx.move_to(400, 220)
        #ctx.text_path("World")
        #ctx.set_source_rgb(0.39, 0.07, 0.78)
        #ctx.fill_preserve()
        #ctx.set_source_rgb(0,0,0)
        #ctx.set_line_width(2)
        #ctx.stroke()

        ## Show iterating and modifying a (text) path
        #ctx.new_path()
        #ctx.move_to(0, 0)
        #ctx.set_source_rgb(0.3, 0.3, 0.3)
        #ctx.set_font_size(30)
        #text = "This path was warped..."
        #ctx.text_path(text)
        #tw, th = ctx.text_extents(text)[2:4]
        #self.warpPath(ctx, tw, th, 360,300)
        #ctx.fill()

        ## Drawing a bitmap.  Note that we can easily load a PNG file
        ## into a surface, but I wanted to show how to convert from a
        ## wx.Bitmap here instead.
        ##img = cairo.ImageSurface.create_from_png(opj('bitmaps/toucan.png'))
        #bmp = wx.Bitmap('bitmaps/toucan.png')
        #img = wx.lib.wxcairo.ImageSurfaceFromBitmap(bmp)
        #ctx.set_source_surface(img, 70, 230)
        #ctx.paint()

        ##bmp = wx.lib.wxcairo.BitmapFromImageSurface(img)
        ##dc.DrawBitmap(bmp, 280, 300)
        
        
    def warpPath(self, ctx, tw, th, dx, dy):
        def f(x, y):
            xn = x - tw/2
            yn = y+ xn ** 3 / ((tw/2)**3) * 70
            return xn+dx, yn+dy

        path = ctx.copy_path()
        ctx.new_path()
        for type, points in path:
            if type == cairo.PATH_MOVE_TO:
                x, y = f(*points)
                ctx.move_to(x, y)

            elif type == cairo.PATH_LINE_TO:
                x, y = f(*points)
                ctx.line_to(x, y)

            elif type == cairo.PATH_CURVE_TO:
                x1, y1, x2, y2, x3, y3 = points
                x1, y1 = f(x1, y1)
                x2, y2 = f(x2, y2)
                x3, y3 = f(x3, y3)
                ctx.curve_to(x1, y1, x2, y2, x3, y3)

            elif type == cairo.PATH_CLOSE_PATH:
                ctx.close_path()

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
    
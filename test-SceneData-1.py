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
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.position = (0,0)
        self.mousedown = False
        
        self.game = GameManager()
        self.game.initialize_world( "SceneData\\Level0.png")
        
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

    #def OnMouseLeftDown(self, event):
        ## récupération de la position souris relative à la fenêtre
        #self.position = event.GetPosition()
        ## calcul la nouvelle position de l'acteur
        ##rel_posx = self.Size.x
        #self.game.graphics.update_actor( self.position[0], self.position[1])
        #self.Refresh()
        
    def OnMouseLeftDown(self, event):
        self.position = event.GetPosition()
        self.MOUSEX = self.position[0]
        self.MOUSEY = self.position[1]
        self.mousedown = True
        self.game.graphics.update_actor( self.MOUSEX, self.MOUSEY)
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
        if self.mousedown == True:
            self.game.graphics.update_actor( self.MOUSEX, self.MOUSEY)
        self.Refresh()
        
    def Render(self, dc):
        # Draw some stuff on the plain dc
        sz = self.GetSize()
        # now draw something with cairo
        #NodeBox.createGraphContext(dc)
        ctx = Context()
        ctx.createGraphContext(dc)
        #self.ctx = ctx
        ctx.size(sz.x, sz.y)
        self.game.graphics.draw( ctx)
        
        return
        ###ctx.rotate(40)
        ###ctx.rect(30, 60, 40, 40)
        ##ctx.cairoContext.translate( 30 + 40/2., 60 + 40/2.)
        ##ctx.cairoContext.rotate( -40 * pi /180.)
        ##ctx.cairoContext.rectangle( -40/2., -40/2., 40, 40)
        ##ctx.cairoContext.stroke()
        
        #ctx.fill(0.5,0.5,0)
        #ctx.rect(self.position[0], self.position[1], 40,40)

        #ctx.rotate(40)
        #ctx.rect(30, 60, 40, 40)
        #ctx.rotate(10)
        #ctx.rect(30, 120, 40, 40)
        #ctx.rotate(10)
        #ctx.rect(30, 180, 40, 40)
        #ctx.rotate(10)
        #ctx.rect(30, 240, 40, 40)
        
        #ctx.reset()
        #ctx.rotate(40)
        #ctx.rect(130, 60, 40, 40, 0.5)
        #ctx.rotate(10)
        #ctx.rect(130, 120, 40, 40, 0.5)
        #ctx.rotate(10)
        #ctx.rect(130, 180, 40, 40, 0.5)
        #ctx.rotate(10)
        #ctx.rect(130, 240, 40, 40, 0.5)

        ##size=14
        ##ctx.cairoContext.set_font_size( size)
        ##ctx.cairoContext.save()
        ##ctx.cairoContext.translate(100+size*3/4.,100-size/4.)
        ###ctx.cairoContext.move_to(100+size*3/4.,100-size/4.)
        ##ctx.cairoContext.rotate( - 90. * pi / 180. )
        ##ctx.cairoContext.translate(0-size*3/4., 1.+size/4.)
        ##ctx.cairoContext.show_text("one")
        ##ctx.cairoContext.stroke()
        ##ctx.cairoContext.restore()

        ###ctx.cairoContext.set_font_size( size)
        ###ctx.cairoContext.save()
        ###ctx.cairoContext.translate(100.,100.+1)
        ####ctx.cairoContext.move_to(100,100)
        ####ctx.cairoContext.rotate( - 90. * pi / 180. )
        ####ctx.cairoContext.translate(0-size*3/4., 1.+size/4.)
        ###ctx.cairoContext.show_text("one")
        ###ctx.cairoContext.restore()
        
        ###ctx.cairoContext.identity_matrix()
        ###ctx.cairoContext.rectangle(100,100,100,100)
        ###ctx.cairoContext.stroke()

        ##ctx.cairoContext.save()
        ##ctx.cairoContext.translate(100.,100.+1)
        ##ctx.cairoContext.show_text("one")
        ##ctx.cairoContext.restore()

        ###self.cairoContext.translate(14/2.+x,-14/2.+y)
            
            ###self.cairoContext.translate( x , y)
            ###self.cairoContext.rotate( - self._transform.radians)
            ###size = 5. #10.
            ###self.cairoContext.translate( x + size/2., y + size/2.)
            ###self.cairoContext.rotate( - self._transform.radians)
            ###self.cairoContext.translate( - size/2., - size/2.)
        
        #ctx.reset()
        #ctx.fontsize(14)
        #ctx.rotate(90)
        #ctx.text("one", 30, 380)
        #ctx.text("two", 45, 380)
        #ctx.reset()
        #ctx.text("one", 30, 380)
        #ctx.rect(30, 380, 14, 14)
        #ctx.text("three", 70, 380)
        
        #ctx.fill( 0.2)
        ## doesn't work
        ##ctx.skew( 10.0)
        #ctx.rect( 220, 10, 40, 40)
        
        #return

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
    
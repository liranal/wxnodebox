
import wx
import array

import Image
import ImageDraw


def julia2():
    #SIZE = 128
    SIZE = 512
    image = Image.new("L", (SIZE, SIZE))
    d = ImageDraw.Draw(image)

    c = 0.5 + 0.2j
    for x in range(SIZE):
        for y in range(SIZE):
            re = (x * 2.0 / SIZE) - 1.0
            im = (y * 2.0 / SIZE) - 1.0

            z=re+im*1j
            for i in range(128):
                if abs(z) > 4.0:
                    break
                z = z * z + c
            if abs(z) > 4.0:
                d.point((x, y), 128)
            else:
                d.point((x, y), 0)
            #d.point((x, y), i * 2)
    return image

    #image.save(r"c:\julia.png", "PNG")

def julia():
    SIZE = 512
    image = Image.new("L", (SIZE, SIZE))
    d = ImageDraw.Draw(image)

    c = 0.32 + 0.043j
    for x in range(SIZE):
        for y in range(SIZE):
            re = (x * 3.0 / SIZE) - 1.5
            im = (y * 3.0 / SIZE) - 1.5

            z=re+im*1j
            for i in range(10):
                if abs(z) > 4.0:
                    break
                z = z * z + c
            if abs(z) > 4.0:
                d.point((x, y), 255)
            else:
                d.point((x, y), 0)
            #d.point((x, y), i * 2)
    return image
    
    
    
    
class MathFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title)
        p1 = TestPanel(self, title)

        self.sizer = wx.BoxSizer()
        self.sizer.Add(p1, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        size = wx.DisplaySize()
        size = ( size[0]-100, size[1]-100)
        size = ( 700, 700)
        self.SetSize(size)

        self.Center()
        self.Show(True)

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.width, self.height = 120,120

        self.MakeImageRGB(self.width, self.height)
        #self.MakeBitmapRGB(self.width, self.height)
        #self.MakeBitmapRGBA(self.width, self.height)
        #self.MakeBitmapRGBpA(self.width, self.height)

    def GetRGB(self, x, y, bpp):
        # calculate some colour values for this sample based on x,y position
        r = g = b = 0
        if y < self.height/3:                           r = 255
        if y >= self.height/3 and y <= 2*self.height/3: g = 255
        if y > 2*self.height/3:                         b = 255

        if bpp == 4:
            a = int(x * 255.0 / self.width)
            return r, g, b, a
        else:
            return r, g, b

        
    def MakeImageRGB(self, width, height):
        # build PIL image
        pilImage = julia()
        image = wx.EmptyImage(pilImage.size[0],pilImage.size[1])
        image.SetData(pilImage.convert("RGB").tostring())
        image.SetAlphaData(pilImage.convert("RGBA").tostring()[3::4])
        # use the wx.Image or convert it to wx.Bitmap
        self.rgbBmp = wx.BitmapFromImage(image)

    def MakeBitmapRGB(self, width, height):
        # Make a bitmap using an array of RGB bytes
        bpp = 3  # bytes per pixel
        bytes = array.array('B', [0] * width*height*bpp)

        for y in xrange(height):
            for x in xrange(width):
                offset = y*width*bpp + x*bpp
                r,g,b = self.GetRGB(x, y, bpp)
                bytes[offset + 0] = r
                bytes[offset + 1] = g
                bytes[offset + 2] = b

        self.rgbBmp = wx.BitmapFromBuffer(width, height, bytes)



    def MakeBitmapRGBA(self, width, height):
        # Make a bitmap using an array of RGBA bytes
        bpp = 4  # bytes per pixel
        bytes = array.array('B', [0] * width*height*bpp)

        for y in xrange(height):
            for x in xrange(width):
                offset = y*width*bpp + x*bpp
                r,g,b,a = self.GetRGB(x, y, bpp)
                bytes[offset + 0] = r
                bytes[offset + 1] = g
                bytes[offset + 2] = b
                bytes[offset + 3] = a

        self.rgbaBmp = wx.BitmapFromBufferRGBA(width, height, bytes)


    def MakeBitmapRGBpA(self, width, height):
        # Make a bitmap using an array of RGB bytes plus a separate
        # buffer for the alpha channel
        bpp = 3  # bytes per pixel
        bytes = array.array('B', [0] * width*height*bpp)

        for y in xrange(height):
            for x in xrange(width):
                offset = y*width*bpp + x*bpp
                r,g,b = self.GetRGB(x, y, bpp)
                bytes[offset + 0] = r
                bytes[offset + 1] = g
                bytes[offset + 2] = b

        # just use an alpha buffer with a constant alpha value for all
        # pixels for this example, it could just as easily have
        # varying alpha values like the other sample.
        alpha = array.array('B', [128]*width*height)
        self.rgbaBmp2 = wx.BitmapFromBuffer(width, height, bytes, alpha)


    def DrawBitmapAndMessage(self, dc, bmp, msg, x_, y_):
        x, y = x_, y_

        # draw some text to help show the alpha
        dc.SetFont(self.GetFont())
        while y < y_ + self.height + 2*dc.GetCharHeight():
            dc.DrawText(msg, x,y)
            y += dc.GetCharHeight() + 5

        # draw the bitmap over the text
        dc.DrawBitmap(bmp, x+15,y_+15, True)


    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        self.DrawBitmapAndMessage(dc, self.rgbBmp,  "No alpha channel in this image", 30,35)
        #self.DrawBitmapAndMessage(dc, self.rgbaBmp, "This image has some alpha", 325,35)
        #self.DrawBitmapAndMessage(dc, self.rgbaBmp2,"This one made with RGB+A", 180,220)





#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>BitmapFromBuffer</center></h2>

Two new wx.Bitmap factory functions allow you to create a wx.Bitmap
directly from a data buffer.  The the buffer can be any Python object
that implements the buffer interface, or is convertable to a buffer,
such as a string or an array.  The new functions are: <ul>

<li><b>wx.BitmapFromBuffer</b>(width, height, dataBuffer, alphaBuffer=None):
Creates the bitmap from a buffer of RGB bytes, optionally with a separate
buffer of alpha bytes.

<li><b>wx.BitmapFromBufferRGBA</b>(width, height, dataBuffer): Creates
the bitmap from a buffer containing RGBA bytes.

</ul>



</body></html>
"""

import sys,os


if __name__ == '__main__':
    app = wx.App(0)
    MathFrame(None, -1, 'File Hunter')
    app.MainLoop()
    #run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])


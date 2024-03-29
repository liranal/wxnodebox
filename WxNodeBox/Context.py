#!/usr/bin/python
# -*- coding: iso-8859-1 -*- 

import wx

import cairo

from BezierPath import *
from Point import *
from Transform import *


class Context():
    '''
    The Box class is an abstraction to hold a Cairo surface, context and all
    methods to access and manipulate it (the Nodebox language is
    implemented here).
    '''

    inch = 72
    cm = 28.3465
    mm = 2.8346

    RGB = "rgb"
    HSB = "hsb"

    CENTER = "center"
    CORNER = "corner"
    CORNERS = "corners"

    DEFAULT_WIDTH = 200
    DEFAULT_HEIGHT = 200


    NORMAL = "1"
    FORTYFIVE = "2"
    
    #self.cairoContext = None
    #self._ctx
    def __init__(self):
        self.cairoContext = None
        self.RGB = "rgb"
        self.HSB = "hsb"
        self.CMYK = "cmyk"    
        self._colormode = self.RGB
        self._fillState = 1
        self._lineWidth = 1
        
        self._autoclosepath = True
        self._transform = Transform()
        self._fontsize = 10
        #self._color = Color()
    
    def size(self, width, height):
        self.width = width
        self.height = height
    
    def rect2(self, x, y, width, height, roundness=0.0, draw=True):
        if roundness == 0:
            p = BezierPath()
            p.rect(x, y, width, height)
        else:
            curve = min(width*roundness, height*roundness)
            p = self.BezierPath(**kwargs)
            p.moveto(x, y+curve)
            p.curveto(x, y, x, y, x+curve, y)
            p.lineto(x+width-curve, y)
            p.curveto(x+width, y, x+width, y, x+width, y+curve)
            p.lineto(x+width, y+height-curve)
            p.curveto(x+width, y+height, x+width, y+height, x+width-curve, y+height)
            p.lineto(x+curve, y+height)
            p.curveto(x, y+height, x, y+height, x, y+height-curve)
            p.closepath()
            
    def createGraphContext( self, wxPaintDCObject):
        self.cairoContext = wx.lib.wxcairo.ContextFromDC(wxPaintDCObject)
        return self.cairoContext

    def getGraphContext( self):
        return self.cairoContext

    # version 0.00
    def rect( self, x, y, width, height, roundness=0.0, draw=True):
        '''Draws a rectangle with top left corner at (x,y)

        The roundness variable sets rounded corners.
        '''
        # straight corners
        if roundness == 0.0:
            self.cairoContext.save ()
            if self._transform.mode == CENTER:
                self.cairoContext.translate( x + width/2., y + height/2.)
                self.cairoContext.rotate( - self._transform.radians)
                x0 = -width/2.
                y0 = -height/2.
            else:
                x0 = x
                y0 = y
            self.cairoContext.rectangle( x0, y0, width, height)
            self.cairoContext.set_line_width( self._lineWidth)
            if self._fillState == 1:
                self.cairoContext.fill()
            self.cairoContext.restore ()
        else:
            self.cairoContext.save ()
            if self._transform.mode == CENTER:
                self.cairoContext.translate( x + width/2., y + height/2.)
                self.cairoContext.rotate( - self._transform.radians)
                x0 = -width/2.
                y0 = -height/2.
            else:
                x0 = x
                y0 = y
            radius = roundness * 50
            x1=x0+width
            y1=y0+height
            #if (!rect_width || !rect_height)
            #    return
            if width/2<radius:
                if height/2<radius:
                    self.cairoContext.move_to  (x0, (y0 + y1)/2)
                    self.cairoContext.curve_to (x0 ,y0, x0, y0, (x0 + x1)/2, y0)
                    self.cairoContext.curve_to (x1, y0, x1, y0, x1, (y0 + y1)/2)
                    self.cairoContext.curve_to (x1, y1, x1, y1, (x1 + x0)/2, y1)
                    self.cairoContext.curve_to (x0, y1, x0, y1, x0, (y0 + y1)/2)
                else:
                    self.cairoContext.move_to  (x0, y0 + radius)
                    self.cairoContext.curve_to (x0 ,y0, x0, y0, (x0 + x1)/2, y0)
                    self.cairoContext.curve_to (x1, y0, x1, y0, x1, y0 + radius)
                    self.cairoContext.line_to (x1 , y1 - radius)
                    self.cairoContext.curve_to (x1, y1, x1, y1, (x1 + x0)/2, y1)
                    self.cairoContext.curve_to (x0, y1, x0, y1, x0, y1- radius)
            else:
                if height/2<radius:
                    self.cairoContext.move_to  (x0, (y0 + y1)/2)
                    self.cairoContext.curve_to (x0 , y0, x0 , y0, x0 + radius, y0)
                    self.cairoContext.line_to (x1 - radius, y0)
                    self.cairoContext.curve_to (x1, y0, x1, y0, x1, (y0 + y1)/2)
                    self.cairoContext.curve_to (x1, y1, x1, y1, x1 - radius, y1)
                    self.cairoContext.line_to (x0 + radius, y1)
                    self.cairoContext.curve_to (x0, y1, x0, y1, x0, (y0 + y1)/2)
                else:
                    self.cairoContext.move_to  (x0, y0 + radius)
                    self.cairoContext.curve_to (x0 , y0, x0 , y0, x0 + radius, y0)
                    self.cairoContext.line_to (x1 - radius, y0)
                    self.cairoContext.curve_to (x1, y0, x1, y0, x1, y0 + radius)
                    self.cairoContext.line_to (x1 , y1 - radius)
                    self.cairoContext.curve_to (x1, y1, x1, y1, x1 - radius, y1)
                    self.cairoContext.line_to (x0 + radius, y1)
                    self.cairoContext.curve_to (x0, y1, x0, y1, x0, y1- radius)
            # xxxxxxxxx
            self.cairoContext.close_path ()
            self.cairoContext.set_line_width( self._lineWidth)
            if self._fillState == 1:
                self.cairoContext.fill_preserve ()
            self.cairoContext.restore ()
        
        if draw == True:
            self.cairoContext.stroke()
    
    # version 0.00
    def stroke( self, color0, color1, color2, a=1):
        ''' Sets a stroke color, applying it to new paths.
        '''

    def stroke(self, *args):
        ''' Sets a stroke color, applying it to new paths.
        '''
        params = len(args)
        a=1
        if params == 1:
            color0 = args[0]
            color1 = args[0]
            color2 = args[0]
        if params == 2:
            color0 = args[0]
            color1 = args[0]
            color2 = args[0]
            a = args[1]
        elif params == 3:
            color0 = args[0]
            color1 = args[1]
            color2 = args[2]
        elif params == 4:
            color0 = args[0]
            color1 = args[1]
            color2 = args[2]
            a = args[3]
        if self._colormode == self.RGB:
            self.cairoContext.set_source_rgba( color0, color1, color2, a)
        elif self._colormode == self.HSB:
            rgb = util.hsl_to_rgb(color0, color1, color2)
            self.cairoContext.set_source_rgba( rgb[0], rgb[1], rgb[2], a)
        #self.cairoContext.stroke()
        #if len(args) > 0:
        #    self._strokecolor = self.Color(*args)
        #return self._strokecolor
        
    def colormode( self, mode, range=1.0):
        if mode == self.RGB:
            self._colormode = self.RGB
        elif mode == self.HSB:
            self._colormode = self.HSB
        elif mode == self.CMYK:
            self._colormode = self.CMYK
        else:
            self._colormode = self.RGB
      
    #def fill( self, gray, a=1):
    #    '''Sets a fill color, applying it to new paths.'''
    #    self._fillState = 1
    #    self.cairoContext.set_source_rgba( gray, gray, gray, a)
    #def fill( self, gray, a=1):
    #def fill( self, color0, color1, color2, a=1):
    def fill( self, color0=-1, color1=1, color2=-1, a=1):
        '''Sets a fill color, applying it to new paths.'''
        self._fillState = 1
        if color2 == -1:
            # def fill( self, gray, a=1):
            gray = color0
            self.cairoContext.set_source_rgba( gray, gray, gray, color1)
        elif self._colormode == self.RGB:
            self.cairoContext.set_source_rgba( color0, color1, color2, a)
        elif self._colormode == self.HSB:
            rgb = util.hsl_to_rgb(color0, color1, color2)
            self.cairoContext.set_source_rgba( rgb[0], rgb[1], rgb[2], a)
        #self.opt.fillapply = True
        #self.opt.fillcolor = self.color(*args)
        #return self.opt.fillcolor
    
    def nofill( self):
        '''nofill
        '''
        self._fillState = 0
        
    def oval( self, x, y, width, height, draw=True):
        '''Draws an ellipse starting from (x,y)'''
        from math import pi
        self.cairoContext.save ()
        self.cairoContext.translate ( x + width / 2., y + height / 2.);
        self.cairoContext.scale ( width / 2., height / 2.);
        self.cairoContext.arc ( 0., 0., 1., 0., 2 * pi);
        if self._fillState == 1:
            self.cairoContext.fill()
        self.cairoContext.restore();
        self.cairoContext.set_line_width( self._lineWidth)
        if draw == True:
            self.cairoContext.stroke()

    def circle(self, x, y, diameter):
        self.oval(x, y, diameter, diameter)

    def line( self, x1, y1, x2, y2, draw=True):
        '''Draws a line from (x1,y1) to (x2,y2)'''
        self.cairoContext.save ()
        self.cairoContext.move_to( x1, y1)
        self.cairoContext.line_to( x2, y2)
        self.cairoContext.set_line_width( self._lineWidth)
        if draw == True:
            self.cairoContext.stroke()
        self.cairoContext.restore();
        #self.beginpath()
        #self.moveto(x1,y1)
        #self.lineto(x2,y2)
        #self.endpath()

    def strokewidth( self, width):
        self._lineWidth = width

    def arrow( self, x, y, width, type=NORMAL, draw=True):
        '''Draws an arrow.

        Arrows can be two types: NORMAL or FORTYFIVE.
        Taken from Nodebox.
        '''
        if type == self.NORMAL:
            head = width * .4
            tail = width * .2
            self.beginpath()
            self.moveto(x, y)
            self.lineto(x-head, y+head)
            self.lineto(x-head, y+tail)
            self.lineto(x-width, y+tail)
            self.lineto(x-width, y-tail)
            self.lineto(x-head, y-tail)
            self.lineto(x-head, y-head)
            self.lineto(x, y)
            self.endpath( draw)
        elif type == self.FORTYFIVE:
            head = .3
            tail = 1 + head
            self.beginpath()
            self.moveto(x, y)
            self.lineto(x, y+width*(1-head))
            self.lineto(x-width*head, y+width)
            self.lineto(x-width*head, y+width*tail*.4)
            self.lineto(x-width*tail*.6, y+width)
            self.lineto(x-width, y+width*tail*.6)
            self.lineto(x-width*tail*.4, y+width*head)
            self.lineto(x-width, y+width*head)
            self.lineto(x-width*(1-head), y)
            self.lineto(x, y)
            self.endpath( draw)
        else:
            raise NameError("arrow: available types for arrow() are NORMAL and FORTYFIVE\n")

    def star(self, x, y, points=20, outer=100, inner=50, draw=True):
        '''Draws a star.
        Taken from Nodebox.
        
	Draws a star to the screen. The first two parameters set the location, 
        measured from the star's center. There are three optional parameters 
        that set the number of points, the outer radius and the inner radius 
        (the fill radius).        
        '''
        startx = x
        starty = y
        from math import sin, cos, pi
        self.beginpath()
        self.moveto(startx, starty + outer)

        for i in range(1, int(2 * points)):
            angle = i * pi / points
            x = sin(angle)
            y = cos(angle)
            if i % 2:
                radius = inner
            else:
                radius = outer
            x = startx + radius * x
            y = starty + radius * y
            self.lineto(x,y)

        self.endpath( draw)

        
    # ----- PATH -----
    # Path functions taken from Nodebox and modified

    def beginpath(self, x=None, y=None):
        # create a BezierPath instance
        ## FIXME: This is fishy
        self._path = BezierPath((x,y))
        self._path.closed = False

        # if we have arguments, do a moveto too
        if x is not None and y is not None:
            self._path.moveto(x,y)

    def moveto(self, x, y):
        if self._path is None:
            ## self.beginpath()
            raise ShoebotError, "No current path. Use beginpath() first."
        self._path.moveto(x,y)

    def lineto(self, x, y):
        if self._path is None:
            raise ShoebotError, "No current path. Use beginpath() first."
        self._path.lineto(x, y)

    def curveto(self, x1, y1, x2, y2, x3, y3):
        if self._path is None:
            raise ShoebotError, "No current path. Use beginpath() first."
        self._path.curveto(x1, y1, x2, y2, x3, y3)

    def closepath(self):
        if self._path is None:
            raise ShoebotError, "No current path. Use beginpath() first."
        if not self._path.closed:
            self._path.closepath()
            self._path.closed = True

    def endpath(self, draw=True):
        if self._path is None:
            raise ShoebotError, "No current path. Use beginpath() first."
        if self._autoclosepath:
            self._path.closepath()
        p = self._path
        if draw == True:
            self.drawpath(p)
        self._path = None
        return p

    def autoclosepath(self, close=True):
        self._autoclosepath = close
    
    def findpath(self, points, curvature=1.0):
        """Constructs a path between the given list of points.
        
        Interpolates the list of points and determines
        a smooth bezier path betweem them.
        
        The curvature parameter offers some control on
        how separate segments are stitched together:
        from straight angles to smooth curves.
        Curvature is only useful if the path has more than  three points.
        """
        ''' (NOT IMPLEMENTED) Builds a path from a list of point coordinates.
        Curvature: 0=straight lines 1=smooth curves
        '''
        #raise NotImplementedError("findpath() isn't implemented yet (sorry)")
        #import bezier
        #path = bezier.findpath(points, curvature=curvature)
        #path.ctx = self
        #path.inheritFromContext()
        #return path
        
        # The list of points consists of Point objects,
        # but it shouldn't crash on something straightforward
        # as someone supplying a list of (x,y)-tuples.
        
        from types import TupleType
        for i, pt in enumerate(points):
            if type(pt) == TupleType:
                points[i] = Point(pt[0], pt[1])
        
        if len(points) == 0: return None
        if len(points) == 1:
            path = BezierPath(None)
            path.moveto(points[0].x, points[0].y)
            return path
        if len(points) == 2:
            path = BezierPath(None)
            path.moveto(points[0].x, points[0].y)
            path.lineto(points[1].x, points[1].y)
            return path
                  
        # Zero curvature means straight lines.
        
        curvature = max(0, min(1, curvature))
        if curvature == 0:
            path = BezierPath(None)
            path.moveto(points[0].x, points[0].y)
            for i in range(len(points)): 
                path.lineto(points[i].x, points[i].y)
            return path
            
        curvature = 4 + (1.0-curvature)*40
        
        dx = {0: 0, len(points)-1: 0}
        dy = {0: 0, len(points)-1: 0}
        bi = {1: -0.25}
        ax = {1: (points[2].x-points[0].x-dx[0]) / 4}
        ay = {1: (points[2].y-points[0].y-dy[0]) / 4}
        
        for i in range(2, len(points)-1):
            bi[i] = -1 / (curvature + bi[i-1])
            ax[i] = -(points[i+1].x-points[i-1].x-ax[i-1]) * bi[i]
            ay[i] = -(points[i+1].y-points[i-1].y-ay[i-1]) * bi[i]
            
        r = range(1, len(points)-1)
        r.reverse()
        for i in r:
            dx[i] = ax[i] + dx[i+1] * bi[i]
            dy[i] = ay[i] + dy[i+1] * bi[i]
    
        path = BezierPath(None)
        path.moveto(points[0].x, points[0].y)
        for i in range(len(points)-1):
            path.curveto(points[i].x + dx[i], 
                         points[i].y + dy[i],
                         points[i+1].x - dx[i+1], 
                         points[i+1].y - dy[i+1],
                         points[i+1].x,
                         points[i+1].y)
        
        return path
    
    def drawpath(self,path):
        if not isinstance(path, BezierPath):
            raise ShoebotError, "drawpath(): Input is not a valid BezierPath object"
        self.cairoContext.save ()
        for element in path.data:
            if not isinstance(element,PathElement):
                raise ShoebotError("drawpath(): Path is not properly constructed (expecting a path element, got " + element + ")")

            cmd = element[0]

            if cmd == MOVETO:
                x = element.x
                y = element.y
                self.cairoContext.move_to(x, y)
            elif cmd == LINETO:
                x = element.x
                y = element.y
                self.cairoContext.line_to(x, y)
            elif cmd == CURVETO:
                c1x = element.c1x
                c1y = element.c1y
                c2x = element.c2x
                c2y = element.c2y
                x = element.x
                y = element.y
                self.cairoContext.curve_to(c1x, c1y, c2x, c2y, x, y)
            elif cmd == CLOSE:
                self.cairoContext.close_path()
            else:
                raise ShoebotError("PathElement(): error parsing path element command (got '%s')" % (cmd))
        ## TODO
        ## if path has state attributes, set the context to those, saving
        ## before and replacing them afterwards with the old values
        ## else, just go on
        # if path.stateattrs:
        #     for attr in path.stateattrs:
        #         self.context....

        self.cairoContext.set_line_width( self._lineWidth)
        if self._fillState == 1:
            self.cairoContext.fill()
        #self.cairoContext.restore();
        #self.cairoContext.restore();
        #if draw == True:
        self.cairoContext.stroke()
        self.cairoContext.restore()
        
    #### Transform and utility
    # ----- Transform and utility -----

    # TODO
    def beginclip(self,x,y,w,h):
        self.save()
        self.context.rectangle(x, y, w, h)
        self.context.clip()

    # TODO
    def endclip(self):
        self.restore()
        
    def translate(self, x, y):
        self._transform.translate( x, y)
        
    def rotate(self, degrees=0, radians=0):
        self._transform.rotate( degrees, radians)

    # TODO - to check
    def scale(self, x=1, y=None):
        if x == 0 or y == 0:
            print "Warning: Invalid matrix provided to scale(), values of 0 not allowed. Ignoring."
            pass
        elif y is None:
            self.context.scale(x,x)
        else:
            self.context.scale(x,y)
        
    def reset(self):
        #self.context.identity_matrix()
        self._transform.reset()

    # TODO - doesn't work
    def skew(self, x=1, y=None):
        if x in (-1,1):
            print "Warning: Invalid value provided to scale(), values of -1, or -1 not allowed. Setting value to 0."
            x = 0
        if y in (-1,1):
            print "Warning: Invalid value provided to scale(), values of -1, or -1 not allowed. Setting value to 0."
            y = 0
        elif y is None:
            y = x
            mtrx = cairo.Matrix (xx=1.0, yx=y, xy=x, yy=1.0, x0=0.0, y0=0.0)
            self.cairoContext.transform(mtrx)
        else:
            mtrx = cairo.Matrix (xx=1.0, yx=y, xy=x, yy=1.0, x0=0.0, y0=0.0)
            self.cairoContext.transform(mtrx)
    
    # TODO - to check
    def push(self):
        #self.push_group()
        self.cairoContext.save()

    # TODO - to check
    def pop(self):
        #self.pop_group()
        self.cairoContext.restore()
            
    # ----- UTILITY -----
    
    # TODO - to check
    def random(self,v1=None, v2=None):
        # ipsis verbis from Nodebox
        import random
        if v1 is not None and v2 is None:
            if isinstance(v1, float):
                return random.random() * v1
            else:
                return int(random.random() * v1)
        elif v1 != None and v2 != None:
            if isinstance(v1, float) or isinstance(v2, float):
                start = min(v1, v2)
                end = max(v1, v2)
                return start + random.random() * (end-start)
            else:
                start = min(v1, v2)
                end = max(v1, v2) + 1
                return int(start + random.random() * (end-start))
        else: # No values means 0.0 -> 1.0
            return random.random()

    from random import choice
    
    # TODO - to check
    def grid(self, cols, rows, colSize=1, rowSize=1, shuffled = False):
        """Returns an iterator that contains coordinate tuples.
        The grid can be used to quickly create grid-like structures.
        A common way to use them is:
            for x, y in grid(10,10,12,12):
                rect(x,y, 10,10)
        """
        # Taken ipsis verbis from Nodebox

        rowRange = range(int(rows))
        colRange = range(int(cols))
        if (shuffled):
            shuffle(rowRange)
            shuffle(colRange)
        for y in rowRange:
            for x in colRange:
                yield (x*colSize,y*rowSize)
        
    # ----- TEXT -----
    
    def textmetrics(self, txt, width=None):
        '''Returns the width and height of a string of text as a tuple
        (according to current font settings).
        '''
        # for now only returns width and height (as per Nodebox behaviour)
        # but maybe we could use the other data from cairo
        x_bearing, y_bearing, textwidth, textheight, x_advance, y_advance = self.cairoContext.text_extents(txt)
        return textwidth, textheight
    
    def textwidth(self, txt, width=None):
        '''Returns the width of a string of text according to the current
        font settings.
        '''
        return textmetrics(txt)[0]

    def textheight(self, txt, width=None):
        '''Returns the height of a string of text according to the current
        font settings.
        '''
        return textmetrics(txt)[1]
    
    def lineheight(self, height=None):
        '''
        NOT IMPLEMENTED
        '''
        # default: 1.2
        # sets leading
        raise NotImplementedError("lineheight() isn't implemented yet")

    def align(self, align="LEFT"):
        '''
        NOT IMPLEMENTED
        '''
        # sets alignment to LEFT, RIGHT, CENTER or JUSTIFY
        raise NotImplementedError("align() isn't implemented in Shoebot yet")
    
    def font(self, fontpath=None, fontsize=None):
        '''Set the font to be used with new text instances.

        Accepts TrueType and OpenType files. Depends on FreeType being
        installed.'''
        if fontpath is not None:
            face = util.create_cairo_font_face_for_file(fontpath, 0)
            self.cairoContext.set_font_face(face)
        else:
            self.cairoContext.get_font_face()
        if fontsize is not None:
            self.fontsize(fontsize)
    
    def fontsize(self, fontsize=None):
        if fontsize is not None:
            self._fontsize = fontsize
            self.cairoContext.set_font_size( fontsize)
        else:
            #return self.cairoContext.get_font_size()
            return self._fontsize

    def text(self, txt, x, y, width=None, height=1000000, outline=False):
        '''
        Draws a string of text according to current font settings.
        '''
        # TODO: Check for malformed requests (x,y,txt is a common mistake)
        self.cairoContext.save()
        if width is not None:
            pass
        if outline is True:
            self.textpath(txt, x, y, width, height)
        else:
            ##original
            #self.cairoContext.move_to(x,y+1.)
            #self.cairoContext.show_text(txt)

            ##with transformation
            length = len(txt)
            self.cairoContext.save()
            xcoeff = 4.
            # ce coeff reste � analyser
            ycoeff = 2.
            self.cairoContext.translate(x+self._fontsize*length/xcoeff,y-self._fontsize/ycoeff)
            #ctx.cairoContext.move_to(100+size*3/4.,100-size/4.)
            self.cairoContext.rotate( - self._transform.radians)
            self.cairoContext.translate(0-self._fontsize*length/xcoeff, 1.+self._fontsize/ycoeff)
            self.cairoContext.show_text( txt)
            
            #self.cairoContext.translate(0-14/2.,1.+14/2.)
            #self.cairoContext.rotate( - self._transform.radians)
            #self.cairoContext.translate(14/2.+x,-14/2.+y)
            #self.cairoContext.translate( x , y)
            #self.cairoContext.rotate( - self._transform.radians)
            #size = 5. #10.
            #self.cairoContext.translate( x + size/2., y + size/2.)
            #self.cairoContext.rotate( - self._transform.radians)
            #self.cairoContext.translate( - size/2., - size/2.)
            #self.cairoContext.show_text(txt)
            self.cairoContext.set_line_width( self._lineWidth)
            if self._fillState == 1:
                self.cairoContext.fill()
            self.cairoContext.stroke()
                
        self.cairoContext.restore()
        
    # TODO
    def textpath(self, txt, x, y, width=None, height=1000000, draw=True):
        '''
        Draws an outlined path of the input text
        '''
        ## FIXME: This should be handled by BezierPath
        self.save()
        self.context.move_to(x,y)
        self.context.text_path(txt)
        self.restore()
        #return self._path
        
    # ----- IMAGE -----

    ## TODO Lit uniquement les fichiers png
    def image(self, path, x, y, width=None, height=None, alpha=1.0, data=None):
        '''
        TODO:
        width and height ought to be for scaling, not clipping
        Use gdk.pixbuf to load an image buffer and convert it to a cairo surface
        using PIL
        '''
        imagesurface = cairo.ImageSurface.create_from_png(path)
        if width == None:
            width = imagesurface.get_width()
        if height == None:
            height = imagesurface.get_height()
        self.cairoContext.save()
        self.cairoContext.translate( x, y)
        self.cairoContext.scale( 0.5, 0.5)
        #self.cairoContext.scale( 1.0/width, 1.0/height)
        self.cairoContext.set_source_rgba(1.0, 0.0, 1.0, 1.0)
        self.cairoContext.set_source_surface( imagesurface, 0, 0)
        self.cairoContext.paint()
        self.cairoContext.restore()
        #self.cairoContext.set_source_surface (imagesurface, x, y)
        #self.cairoContext.rectangle( x, y, width, height)
        #self.cairoContext.scale( 1.0/width, 1.0/height)
        #self.cairoContext.fill()

    def image2(self, path, x, y, width=None, height=None, alpha=1.0, data=None):
        '''
        TODO:
        width and height ought to be for scaling, not clipping
        Use gdk.pixbuf to load an image buffer and convert it to a cairo surface
        using PIL
        '''
        imagesurface = cairo.ImageSurface.create_from_png(path)
        if width == None:
            width = imagesurface.get_width()
        if height == None:
            height = imagesurface.get_height()
        self.cairoContext.set_source_surface (imagesurface, x, y)
        self.cairoContext.rectangle( x, y, width, height)
        self.cairoContext.scale( 1.0/width, 1.0/height)
        self.cairoContext.fill()

    ## TODO Lit uniquement les fichiers png
    def imagesize(self, path):
        '''
        TODO:
        width and height ought to be for scaling, not clipping
        Use gdk.pixbuf to load an image buffer and convert it to a cairo surface
        using PIL
        '''
        imagesurface = cairo.ImageSurface.create_from_png(path)
        return imagesurface.get_width(), imagesurface.get_height()


#!/usr/bin/python
# -*- coding: iso-8859-1 -*- 

from PathElement import *

class BezierPath():
    """
    Shoebot implementation of Nodebox's BezierPath wrapper.
    While Nodebox relies on Cocoa/QT for its data structures,
    this is more of an "agnostic" implementation that won't
    require any other back-ends to work with paths.
    """
    
    ## def __init__(self, ctx, path=None):
    def __init__(self, path=None):
        if path is None:
            self.data = []
        elif isinstance(path, (tuple,list)):
            self.data = []
            self.extend(path)
        elif isinstance(path, BezierPath):
            self.data = path.data
            ##util._copy_attrs(path, self, self.stateAttributes)
        elif isinstance(path, basestring):
            # SVG path goes here
            # - check if SVG datastring is valid
            # - parse it
            pass
        else:
            raise ShoebotError, "Don't know what to do with %s." % path
        self.closed = False

    # testing string output
    #def __str__(self):
        #return self.data

    def copy(self):
        return self.__class__(self)

    ### Path methods ###

    def moveto(self, x, y):
        self.data.append(PathElement(MOVETO, x, y))

    def lineto(self, x, y):
        self.data.append(PathElement(LINETO, x, y))

    def curveto(self, c1x, c1y, c2x, c2y, x, y):
        self.data.append(PathElement(CURVETO, c1x, c1y, c2x, c2y, x, y))

    def closepath(self):
        self.data.append(PathElement(CLOSE))
        self.closed = True

    def __getitem__(self, index):
        return self.data[index]
    def __iter__(self):
        for i in range(len(self.data)):
            yield self.data[i]
    def __len__(self):
        return len(self.data)

    def extend(self, args):
        '''
        This method is still work in progress,
        don't rely on it :o)
        '''
        self.segment_cache = None

        # parsepathdata()

        ## TODO
        # Initial check, we should check for
        # - points
        # - tuples
        # - list
        # - PathElement

        # oh my, this just creates straight lines, no curves
        # this needs to be rewritten

        # check if we got [x,y] as an argument
        if isinstance(args, list) and len(args) == 2 and isinstanceargs[0]:
            # does the path have something?
            if len(self.data) == 0:
                # if not, move to [x,y]
                cmd = MOVETO
            else:
                # otherwise, draw a line to [x,y]
                cmd = LINETO
            # assign the elements to specific vars
            x = args[0]
            y = args[1]
            self.data.append(PathElement(cmd, x, y))

        elif isinstance(args,list):
            for el in pathElements:
                if isinstance(el, (list, tuple, PathElement)):
                    x, y = el
                    if len(self.data) == 0:
                        cmd = MOVETO
                    else:
                        cmd = LINETO
                    self.data.append(PathElement(cmd, x, y))
                elif isinstance(el, PathElement):
                    self.data.append(el)
                else:
                    raise ShoebotError, "Don't know how to handle %s" % el

    def append(self, el):
        '''
        Wrapper method for hiding the data var
        from public access
        '''
        # parsepathdata()
        if isinstance(el, PathElement):
            self.data.append(el)
        else:
            raise TypeError("Wrong data passed to BezierPath.append()")

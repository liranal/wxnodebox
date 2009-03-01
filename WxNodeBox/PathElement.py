#!/usr/bin/python
# -*- coding: iso-8859-1 -*- 

MOVETO = "moveto"
LINETO = "lineto"
RLINETO = "rlineto"
CURVETO = "curveto"
RCURVETO = "rcurveto"
CLOSE = "close"

class PathElement:
    '''
    Taken from Nodebox and modified
    '''
    def __init__(self, cmd, *args):
        self.cmd = cmd
        if cmd == MOVETO:
            assert len(args) == 2
            self.x, self.y = args
            self.c1x = self.c1y = self.c2x = self.c2y = None
        elif cmd == LINETO:
            assert len(args) == 2
            self.x, self.y = args
            self.c1x = self.c1y = self.c2x = self.c2y = None
        elif cmd == RLINETO:
            assert len(args) == 2
            self.x, self.y = args
            self.c1x = self.c1y = self.c2x = self.c2y = None
        elif cmd == CURVETO:
            assert len(args) == 6
            self.c1x, self.c1y, self.c2x,self.c2y, self.x, self.y = args
        elif cmd == RCURVETO:
            assert len(args) == 6
            self.c1x, self.c1y, self.c2x,self.c2y, self.x, self.y = args
        elif cmd == CLOSE:
            assert args is None or len(args) == 0
            self.x = self.y = self.c1x = self.c1y = self.c2x = self.c2y = None
        else:
            raise ShoebotError('Wrong initialiser for PathElement (got "%s")' % (cmd))

    def __getitem__(self,key):
        if self.cmd == MOVETO:
            return (MOVETO, self.x, self.y)[key]
        elif self.cmd == LINETO:
            return (LINETO, self.x, self.y)[key]
        elif self.cmd == RLINETO:
            return (RLINETO, self.x, self.y)[key]
        elif self.cmd == CURVETO:
            return (CURVETO, self.c1x, self.c1y, self.c2x, self.c2y, self.x, self.y)[key]
        elif self.cmd == RCURVETO:
            return (RCURVETO, self.c1x, self.c1y, self.c2x, self.c2y, self.x, self.y)[key]
        elif self.cmd == CLOSE:
            return (CLOSE,)[key]
        return
    def __repr__(self):
        if self.cmd == MOVETO:
            return "(MOVETO, %.6f, %.6f)" % (self.x, self.y)
        elif self.cmd == LINETO:
            return "(LINETO, %.6f, %.6f)" % (self.x, self.y)
        elif self.cmd == RLINETO:
            return "(RLINETO, %.6f, %.6f)" % (self.x, self.y)
        elif self.cmd == CURVETO:
            return "(CURVETO, %.6f, %.6f, %.6f, %.6f, %.6f, %.6f)" % (self.c1x, self.c1y, self.c2x, self.c2y, self.x, self.y)
        elif self.cmd == RCURVETO:
            return "(RCURVETO, %.6f, %.6f, %.6f, %.6f, %.6f, %.6f)" % (self.c1x, self.c1y, self.c2x, self.c2y, self.x, self.y)
        elif self.cmd == CLOSE:
            return "(CLOSE,)"
    def __eq__(self, other):
        if other is None: return False
        if self.cmd != other.cmd: return False
        return self.x == other.x and self.y == other.y \
            and self.c1x == other.c1x and self.c1y == other.c1y \
            and self.c1x == other.c1x and self.c1y == other.c1y
    def __ne__(self, other):
        return not self.__eq__(other)

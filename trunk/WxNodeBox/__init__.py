#!/usr/bin/env python
# -*- coding: iso-8859-1 -*- 

'''
Shoebot module

Copyright 2007, 2008 Ricardo Lafuente
Developed at the Piet Zwart Institute, Rotterdam

This file is part of Shoebot.

Shoebot is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Shoebot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Shoebot.  If not, see <http://www.gnu.org/licenses/>.

This file uses code from Nodebox (http://www.nodebox.net).
The relevant code parts are marked with a "Taken from Nodebox" comment.

'''

import wx
import cairo
import util
from BezierPath import *
from Context import *
from WxBase import *

VERBOSE = False
DEBUG = False
EXTENSIONS = ('.png','.svg','.ps','.pdf')

#__all__ = ()
#__all__.extend(['Context'])

# start - ORAY intervention

class ShoebotError(Exception): pass

# end   - ORAY intervention

if __name__ == "__main__":
    print '''
    This file can only be used as a Python module.
    Use the 'sbot' script for commandline use.
    '''
    import sys
    sys.exit()


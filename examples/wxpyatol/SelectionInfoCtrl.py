from wxPython.wx import *

class StatInfoCtrl (wxStaticText):
    def __init__(self, pParent, id, str, ptr, size, param):
      wxStaticText.__init__ (self, pParent, id, str, ptr, size, param)


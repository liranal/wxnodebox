from wxPython.wx import *

class CPopupMenu(wxMenu):
    def __init__ (self):#, pParent):
        wxMenu.__init__ (self) #, pParent)
        self.m_nSelectedCmd = 0
        EVT_MENU_RANGE(self, 1, 100000, self.OnMenuSelection)

    def GetSelectedID(self):
        return self.m_nSelectedCmd

    def OnMenuSelection(self, event):
        #wxPython GetId()
        self.m_nSelectedCmd = event.GetId()

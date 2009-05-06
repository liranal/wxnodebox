from wxPython.wx import *

class COptionsOperationDlg(wxWindow):
    def __init__(self, pParent):
        wxWindow.__init__ (self, pParent, -1, wxDefaultPosition, wxDefaultSize)
        #self.m_wndEditorName = wxTextCtrl (self, pParent, -1, wxDefaultPosition, wxDefaultSize)
        self.m_wndEditorName = wxTextCtrl (self, -1, '') #wxDefaultPosition, wxDefaultSize)

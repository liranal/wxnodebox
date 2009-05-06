from wxPython.wx import *

class COptionsStartupDlg(wxWindow):
    def __init__(self, pParent = None):
        wxWindow.__init__ (self, pParent, -1, wxDefaultPosition, wxDefaultSize)
        self.m_wndShowTipsChk = wxCheckBox (self, -1 , _("Show tip of day"))
        self.m_wndSingleInstChk = wxCheckBox (self, -1 , _("Allow single instance"))
        self.m_wndShowSplashChk = wxCheckBox (self, -1 , _("Show splash screen"))
        self.m_wndRestorePathsChk = wxCheckBox (self, -1 , _("Restore last path"))
        #ifdef __WXMSW__
        self.m_wndStartAtBootChk = wxCheckBox (self, -1 , _("Start at boot time"))
        #endif

        #ifdef __WXMSW__
        self.m_wndStartAtBootChk .SetDimensions(10, 10, 200, 20)
        #endif
        self.m_wndSingleInstChk  .SetDimensions(10, 30, 200, 20)
        self.m_wndShowSplashChk  .SetDimensions(10, 50, 200, 20)
        self.m_wndShowTipsChk    .SetDimensions(10, 70, 200, 20)
        self.m_wndRestorePathsChk.SetDimensions(10, 90, 200, 20)

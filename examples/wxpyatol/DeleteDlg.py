from wxPython.wx import *
from Globals import *

ID_DELETE_BTN     = 10001
ID_DELETE_ALL_BTN = 10002
ID_SKIP_BTN       = 10003
ID_SKIP_ALL_BTN   = 10004
ID_ABORT_BTN      = 10005

class CDeleteDlg(wxDialog):
    def __init__ (self, pParent = None):
        wxDialog.__init__ (self, pParent, 1, _(" "), wxDefaultPosition, wxDefaultSize, wxCAPTION)

        self.m_strInfo = ""

        self.m_wndInfoLabel = wxStaticText (self, -1, "", wxPoint(0,0))
        self.m_wndDeleteBtn = wxButton (self, ID_DELETE_BTN, _("Delete"), wxPoint(0,0))
        self.m_wndDeleteAllBtn = wxButton (self, ID_DELETE_ALL_BTN,  _("Delete all"),  wxPoint(0,0))
        self.m_wndSkipBtn = wxButton (self, ID_SKIP_BTN,      _("Skip"),    wxPoint(0,0))
        self.m_wndSkipAllBtn = wxButton (self, ID_SKIP_ALL_BTN,    _("Skip all"),  wxPoint(0,0))
        self.m_wndAbortBtn = wxButton (self, ID_ABORT_BTN,     _("Abort"),   wxPoint(0,0))

        self.m_wndInfoLabel      .SetDimensions( 10, 10, 250, 40)
        self.m_wndDeleteBtn      .SetDimensions( 10, 60, 80, 22)
        self.m_wndDeleteAllBtn   .SetDimensions( 93, 60, 80, 22)
        self.m_wndSkipBtn        .SetDimensions(176, 60, 80, 22)
        self.m_wndSkipAllBtn     .SetDimensions( 10, 85, 80, 22)
        self.m_wndAbortBtn       .SetDimensions( 93, 85, 80, 22)

        self.SetDimensions(0, 0, 270, 135)
        self.Centre()

        #//set text
        #self.m_wndInfoLabel  .SetLabel(self.m_strInfo)
        self.m_wndDeleteBtn  .SetDefault()

        #EVT_INIT_DIALOG(CDeleteDlg::OnInitDialog)
        EVT_BUTTON(self, ID_DELETE_BTN,       self.OnDelete)
        EVT_BUTTON(self, ID_DELETE_ALL_BTN,   self.OnDeleteAll)
        EVT_BUTTON(self, ID_SKIP_BTN,         self.OnSkip)
        EVT_BUTTON(self, ID_SKIP_ALL_BTN,     self.OnSkipAll)
        EVT_BUTTON(self, ID_ABORT_BTN,        self.OnAbort)

    def SetTitle (self, title):
        self.m_strInfo = title
        self.m_wndInfoLabel.SetLabel(self.m_strInfo)

    def OnDelete(self, event):
        self.EndModal(OPF_DELETE);

    def OnDeleteAll(self, event):
        #//TOFIX OPF_DEL_ALL_DIRS version
        self.EndModal(OPF_DEL_ALL_RO_FILES)

    def OnSkip(self, event):
        self.EndModal(OPF_SKIP)

    def OnSkipAll(self, event):
        self.EndModal(OPF_CPY_SKIP_ALL)

    def OnAbort(self, event):
        self.EndModal(OPF_ABORT)



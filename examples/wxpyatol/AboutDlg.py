from wxPython.wx import *
from Globals import *

class AboutDlg (wxDialog):
    def __init__(self, pParent):
        wxDialog.__init__(self, pParent, -1, _("About WxPyAtol"), wxDefaultPosition, wxSize (270, 190), wxCAPTION|wxSYSTEM_MENU)
        self.m_wndInfo = wxStaticText (self, -1, _("WxPython Atol file manager.\n\nOriginally developed by Miroslav Rajcic.\n\nAdapted by Franz Steinhaeusler 01/2004\nfor wxPython.\n\nVersion: %s") % (APP_VER_STR))
                                     #wxWindow* parent, wxWindowID id, const wxString& label, const wxPoint& pos, const wxSize& size = wxDefaultSize, long style = 0, const wxString& name = 'staticText')
        self.m_wndInfo.SetDimensions(30, 30, 250, 300)
        self.Centre()

    def OnInitDialog(self, event):
        #print 'oninit'
    #    self.SetSize(0, 0, 200, 100);
    #    self.m_wndInfo.Create(self, -1, 'Atol file manager v%s' % (APP_VER_STR),  wxPoint(0,0))
    #    m_wndInfo.SetSize(30, 30, 150, 20)
        self.Centre()



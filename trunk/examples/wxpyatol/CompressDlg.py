from wxPython.wx import *
from PluginManager import *
from WxUtil import *

#extern PluginManager g_PlugManager;

BTN_OK     = 1
BTN_CANCEL = 2

class CCompressDlg(wxDialog):
    def __init__(self, pParent = NULL):
        wxDialog.__init__ (self, pParent, -1, _("Compress file(s)"), wxDefaultPosition, wxDefaultSize, wxCAPTION|wxSYSTEM_MENU)

        self.m_wndOkBtn           = wxButton(self, BTN_OK, _("OK"), wxPoint(0,0))
        self.m_wndCancelBtn       = wxButton(self, BTN_CANCEL, _("Cancel"),wxPoint(0,0))
        self.m_wndDataEdit        = wxTextCtrl(self, -1, '',  wxPoint(0,0))
        self.m_wndArchiveLabel    = wxStaticText(self, -1, _("Archive:"),  wxPoint(0,0))
        #self.m_wndArchiversCombo  = wxComboBox(self, -1, choices=[], wxPoint(0,0), wxSize(0,0), wxCB_READONLY)
        self.m_wndArchiversCombo  = wxComboBox(self, -1, choices=[], style = wxCB_READONLY)
        self.m_wndArchiveLabel   .SetDimensions( 12, 10,  55, 22)
        self.m_wndDataEdit       .SetDimensions( 70, 10, 150, 22)
        self.m_wndOkBtn          .SetDimensions( 10, 90,  80, 22)
        self.m_wndCancelBtn      .SetDimensions( 95, 90,  80, 22)
        self.m_wndArchiversCombo .SetDimensions(140, 35,  80, 22)

        self.SetDimensions(0, 0, 230, 140)
        self.Centre()
        self.m_wndDataEdit.SetFocus()
        self.m_wndOkBtn.SetDefault()

        EVT_BUTTON(self, BTN_OK, self.OnOk)
        EVT_BUTTON(self, BTN_CANCEL, self.OnCancel)

        #//fill all supported plugin extensions in the combo
        self.strExtensions = ''
        #std::vector<wxString> lstTokenized;
        lstTokenized = []
        #print self.GetParent()
        nMax = self.GetParent().m_PluginManager.GetCount()
        for i in range (nMax):
            #//TOFIX if multiple files selected for compression, filter single file archiver extensions
            #//using g_PlugManager[i].GetArchiverCaps(strExt); eher
            #//using g_PlugManager[i].m_pfnGetArchiverCaps(strExt);
            self.strExtensions = self.GetParent().m_PluginManager.m_ArchiverList[i].m_strExtensions
            lstTokenized = Tokenize(self.strExtensions, lstTokenized, ';')
            for j in range(len(lstTokenized)):
                self.m_wndArchiversCombo.Append (lstTokenized[j])

            #//TOFIX remember and select last used archiver extension
            if nMax > 0:
                self.m_wndArchiversCombo.SetSelection(0)

    #def void CCompressDlg::OnOk(wxCommandEvent &event)
    def OnOk(self, event):
        self.EndModal(wxOK)

    def OnCancel(self, event):
    #void CCompressDlg::OnCancel(wxCommandEvent &event)
        self.EndModal(wxCANCEL)

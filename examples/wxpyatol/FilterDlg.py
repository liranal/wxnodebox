from wxPython.wx import *

BTN_OK =  1
BTN_CANCEL = 2

class CFilterDlg (wxDialog):
    def __init__ (self, pParent):
        wxDialog.__init__ (self, pParent, -1, '', wxDefaultPosition, wxDefaultSize, wxCAPTION)
        self.m_strTitle = ''
        self.m_strValue = ''
        EVT_INIT_DIALOG(self, self.OnInitDialog)
        EVT_BUTTON(self, BTN_OK,    self.OnOk)
        EVT_BUTTON(self, BTN_CANCEL,  self.OnCancel)

    #void CFilterDlg::OnInitDialog(wxInitDialogEvent &event)
    def OnInitDialog (self, event):
        #print 'oninit'
        self.SetTitle(self.m_strTitle)
        self.m_wndOkBtn = wxButton (self, BTN_OK,     _("OK"),     wxPoint(0,0))
        self.m_wndCancelBtn = wxButton (self, BTN_CANCEL, _("Cancel"), wxPoint(0,0))
        self.m_wndDataEdit = wxTextCtrl  (self, -1,  self.m_strValue,  wxPoint(0,0))

        self.m_wndDataEdit.SetDimensions(10, 10, 165, 22)
        self.m_wndOkBtn.SetDimensions(10, 40,  80, 22)
        self.m_wndCancelBtn.SetDimensions(95, 40,  80, 22)

        self.SetDimensions(0, 0, 190, 100)
        self.Centre()

        self.m_wndDataEdit.SetFocus()
        self.m_wndOkBtn.SetDefault()


    def OnOk (self, event):
        self.m_strValue = self.m_wndDataEdit.GetValue()
        self.EndModal(wxOK)

    def OnCancel (self, event):
        self.EndModal (wxCANCEL)

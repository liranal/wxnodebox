from wxPython.wx import *
from Globals import *

ID_OVERWRITE_BTN      = 10001
ID_OVERWRITE_ALL_BTN  = 10002
ID_SKIP_BTN           = 10003
ID_SKIP_ALL_BTN       = 10004
ID_RESUME_BTN         = 10005
ID_RENAME_BTN         = 10006
ID_ABORT_BTN          = 10007

class COverwriteDlg (wxDialog):
    def __init__ (self, pParent = None):
        wxDialog.__init__ (self, pParent, 1, _("Overwrite file?"), wxDefaultPosition, wxDefaultSize, wxCAPTION)

        self.m_strInfo = ""

        self.m_wndInfoLabel = wxStaticText (self, -1, "", wxPoint(0,0))
        self.m_wndOverwriteBtn = wxButton (self, ID_OVERWRITE_BTN,   _("Overwrite"), wxPoint(0,0))
        self.m_wndOverwriteAllBtn = wxButton (self, ID_OVERWRITE_ALL_BTN, _("Overwrite all"),wxPoint(0,0))
        self.m_wndSkipBtn = wxButton (self, ID_SKIP_BTN,      _("Skip"),      wxPoint(0,0))
        self.m_wndSkipAllBtn = wxButton (self, ID_SKIP_ALL_BTN,    _("Skip all"),    wxPoint(0,0))
        self.m_wndResumeBtn = wxButton (self, ID_RESUME_BTN,    _("Resume"),    wxPoint(0,0))
        self.m_wndRenameBtn = wxButton (self, ID_RENAME_BTN,    _("Rename"),    wxPoint(0,0))
        self.m_wndAbortBtn = wxButton (self, ID_ABORT_BTN,     _("Abort"),   wxPoint(0,0))
        self.m_wndInfoLabel .SetDimensions( 10, 10, 250, 40)
        self.m_wndOverwriteBtn .SetDimensions( 10, 60,  80, 22)
        self.m_wndOverwriteAllBtn.SetDimensions( 93, 60,  80, 22)
        self.m_wndSkipBtn        .SetDimensions(176, 60,  80, 22)
        self.m_wndSkipAllBtn     .SetDimensions( 10, 85,  80, 22)
        self.m_wndResumeBtn      .SetDimensions( 93, 85,  80, 22)
        self.m_wndRenameBtn      .SetDimensions(176, 85,  80, 22)
        self.m_wndAbortBtn       .SetDimensions(176,110,  80, 22)

        #//Not yet supported
        self.m_wndResumeBtn.Enable(false)

        self.SetDimensions(0, 0, 270, 165)
        self.Centre()

        #//set text
        self.m_wndInfoLabel.SetLabel(self.m_strInfo)
        self.m_wndOverwriteBtn.SetDefault()

        #EVT_INIT_DIALOG(COverwriteDlg::OnInitDialog)
        EVT_BUTTON(self, ID_OVERWRITE_BTN,     self.OnOverwrite)
        EVT_BUTTON(self, ID_OVERWRITE_ALL_BTN, self.OnOverwriteAll)
        EVT_BUTTON(self, ID_SKIP_BTN,          self.OnSkip)
        EVT_BUTTON(self, ID_SKIP_ALL_BTN,      self.OnSkipAll)
        EVT_BUTTON(self, ID_RESUME_BTN,        self.OnResume)
        EVT_BUTTON(self, ID_RENAME_BTN,        self.OnRename)
        EVT_BUTTON(self, ID_ABORT_BTN,         self.OnAbort)
        EVT_KEY_DOWN(self, self.OnKeyDown)

    #void COverwriteDlg::OnOverwrite(wxCommandEvent &event)
    def OnOverwrite(self, event):
        self.EndModal(OPF_OVERWRITE)

    def OnOverwriteAll(self, event):
        self.EndModal(OPF_OVERWRITE|OPF_CPY_OVERWRITE_ALL)

    def OnSkip(self, event):
        self.EndModal(OPF_SKIP)

    def OnSkipAll(self, event):
        self.EndModal(OPF_CPY_SKIP_ALL)

    def OnResume(self, event):
        self.EndModal(OPF_CPY_RESUME)

    def OnRename(self, event):
        self.EndModal(OPF_CPY_RENAME)

    def OnAbort(self, event):
        self.EndModal(OPF_ABORT)

    def OnKeyDown(self, event):
        '''
        /*
        nKey = event.GetKeyCode()
            if(nKey == WXK_RETURN)
            {
                wxCommandEvent dummy;

                wxMessageBox("2");

                //"press" focused child button
                switch(GetSelectedID()){
                    case ID_OVERWRITE_BTN:      OnOverwrite(dummy);      break;
                    case ID_OVERWRITE_ALL_BTN:  OnOverwriteAll(dummy);   break;
                    case ID_SKIP_BTN:           OnSkip(dummy);           break;
                    case ID_SKIP_ALL_BTN:       OnSkipAll(dummy);        break;
                    case ID_RESUME_BTN:         OnResume(dummy);         break;
                    case ID_RENAME_BTN:         OnRename(dummy);         break;
                    case ID_ABORT_BTN:          OnAbort(dummy);          break;
                }
                return;
            }

            if(nKey == WXK_TAB)
            {
                //select next item
                switch(GetSelectedID()){
                    case ID_OVERWRITE_BTN:      m_wndOverwriteAllBtn.SetFocus(); break;
                    case ID_OVERWRITE_ALL_BTN:  m_wndSkipBtn.SetFocus();         break;
                    case ID_SKIP_BTN:           m_wndSkipAllBtn.SetFocus();      break;
                    case ID_SKIP_ALL_BTN:       m_wndRenameBtn.SetFocus();       break; //TOFIX resume btn is being disabled
                    case ID_RESUME_BTN:         m_wndRenameBtn.SetFocus();       break;
                    case ID_RENAME_BTN:         m_wndAbortBtn.SetFocus();        break;
                    case ID_ABORT_BTN:          m_wndOverwriteBtn.SetFocus();    break;
                }

                Refresh();
                return;
            }
        */
        '''
        event.Skip()

    def GetSelectedID(self):
        pFocusedWnd = FindFocus()
        if(pFocusedWnd):
            return pFocusedWnd.GetId()
        return -1


from wxPython.wx import *
from Op import *
import win32api
#from OpState import *

ID_ABORT_BUTTON = 10001

class CProgressDlg(wxDialog):
    def __init__(self, pParent, id, str, pos, size, style):
        wxDialog.__init__(self, pParent, id, str, pos, size, style)
        self.m_pOp = None
        self.m_nLastCurMax = 0
        self.m_bProgressRangeSet =False
        self.m_wndProgressCurrent = wxGauge (self, 1, 100, wxDefaultPosition, wxDefaultSize, wxGA_HORIZONTAL|wxGA_SMOOTH)
        self.m_wndProgressTotal = wxGauge (self, 2, 100, wxDefaultPosition, wxDefaultSize, wxGA_HORIZONTAL|wxGA_SMOOTH)
        self.m_wndAbortBtn = wxButton (self, ID_ABORT_BUTTON, _("Abort"), wxPoint(0,0))
        self.m_wndInfoLabel = wxStaticText (self, -1, '', wxPoint(0,0))
        self.SetDimensions(0, 0, 210, 150)
        self.m_wndInfoLabel.SetDimensions( 10,  10, 180, 40)
        self.m_wndProgressCurrent.SetDimensions( 10,  50, 180, 18)
        self.m_wndProgressTotal.SetDimensions( 10,  70, 180, 18)
        self.m_wndAbortBtn.SetDimensions(140, 100,  50, 22)

        self.Centre()
        self.Refresh()
        #print '3', thread.get_ident()
        #print self

        #start operation thread
        #ifndef __GNUWIN32__
        #m_pOp->Run();
        #endif

        EVT_BUTTON(self, ID_ABORT_BUTTON,  self.OnAbort)
        EVT_BUTTON(self, 9999, self.OnUpdateProgress)
        #EVT_UPDATE_BARGRAPH(self, self.OnUpdateProgress)

        '''
        void CProgressDlg::OnInitDialog(wxInitDialogEvent &event)
            //start operation thread
            #ifndef __GNUWIN32__
                m_pOp->Run();
            #endif

        '''
        #event = wxCommandEvent ()
        #event.m_eventType = wxEVT_COMMAND_BUTTON_CLICKED
        #event.m_id  = 10001
        #event.m_isCommandEvent = True
        ##event = wxCommandEventPtr (self, event)

        #print 'a'
        #print event
        #print event.m_eventType
        #print event.m_id
        #print event.m_isCommandEvent

        #self.ProcessEvent(event)

        #print event
        #print event.m_eventType
        #print event.m_id
        #print event.m_isCommandEvent

    def OnAbort(self, event):
        #print 'Abort'
        #print event
        #print event.m_eventType
        #print event.m_id
        #print event.m_isCommandEvent

        if(self.m_pOp):
            self.m_pOp.m_Stat.Abort()

    def OnUpdateProgress(self, event):
        #print 'update'
        if(self.IsBeingDeleted()):
            return
        if(self.m_pOp):
            #when current file changes its range must be refreshed
            if(self.m_nLastCurMax != self.m_pOp.m_Stat.m_nCurBytesMax):
                self.m_bProgressRangeSet = False

            if(not self.m_bProgressRangeSet):
                self.m_bProgressRangeSet = True
                self.m_nLastCurMax = self.m_pOp.m_Stat.m_nCurBytesMax

                #print 'Range:', self.m_pOp.m_Stat.m_nCurBytesMax/10000
                #TOMAKEBETTER: is this really so: size to 16 bit=
                #self.m_wndProgressCurrent.SetRange(self.m_pOp.m_Stat.m_nCurBytesMax/10000)
                #self.m_wndProgressTotal.SetRange(self.m_pOp.m_Stat.m_nTotBytesMax/10000)
                #ifdef __WXMSW__

                #TOFIX fixes bug in wxGauge95 -> PBM_SETRANGE -> PBM_SETRANGE32
                #TOMAKEBETTER: need this: obviously it works also without this
                #r = self.m_pOp.m_Stat.m_nCurBytesMax / 10000
                r = self.m_pOp.m_Stat.m_nCurBytesMax
                #TODO
                #print "send message"
                #win32api.SendMessage((HWND) self.m_wndProgressCurrent.GetHWND(), PBM_SETRANGE32, 0, r);
                hwnd = self.m_wndProgressCurrent.GetHandle ()
                win32api.SendMessage(hwnd, 1030, 0, r)
                #1030 entspricht PBM_SETRANGE32
                #r = self.m_pOp.m_Stat.m_nTotBytesMax / 10000
                r = self.m_pOp.m_Stat.m_nTotBytesMax
                hwnd = self.m_wndProgressTotal.GetHandle ()
                win32api.SendMessage(hwnd, 1030, 0, r);
                #endif

                #child.SendMessage(WM_USER_PREPARE_TO_CLOSE, 0, 0)
                #child_ex_style = win32gui.SendMessage(self.hwndList, commctrl.LVM_GETEXTENDEDLISTVIEWSTYLE, 0, 0)
                #self.hwndList = win32gui.CreateWindow("SysListView32", None, child_style, 0, 0, 100, 100, self.hwnd, IDC_LISTBOX, self.hinst, None)
                #cb = wxComboBox(self, 500, "default value", wxPoint(90, 50), wxSize(95, -1),
                #                sampleList, wxCB_DROPDOWN)#|wxTE_PROCESS_ENTER)
                ###import win32api, win32con
                ###win32api.SendMessage(cb.GetHandle(),


            assert (self.m_pOp.m_Stat.m_nCurBytesPos <= self.m_pOp.m_Stat.m_nCurBytesMax)
            assert (self.m_pOp.m_Stat.m_nTotBytesPos <= self.m_pOp.m_Stat.m_nTotBytesMax)

            #self.m_wndProgressCurrent.SetValue(self.m_pOp.m_Stat.m_nCurBytesPos / 10000)
            self.m_wndProgressCurrent.SetValue(self.m_pOp.m_Stat.m_nCurBytesPos)
            #self.m_wndProgressCurrent.SetValue(1000)
            #self.m_wndProgressTotal.SetValue(self.m_pOp.m_Stat.m_nTotBytesPos / 10000)
            self.m_wndProgressTotal.SetValue(self.m_pOp.m_Stat.m_nTotBytesPos)

            #refresh info text
            #wxString strInfo;
            #//TOFIX adjust path length to available window size!!!
            #strSrc = self.m_pOp.m_pVfsSrc.GetDir() + '/' + self.m_pOp.m_Stat.m_strSrcFile
            strSrc = self.m_pOp.m_Stat.m_strSrcFile
            if(self.m_pOp.m_pVfsDst):
                #strDst = self.m_pOp.m_pVfsDst.GetDir() + '/' + self.m_pOp.m_Stat.m_strDstFile
                strDst = self.m_pOp.m_Stat.m_strDstFile
                strInfo = _("From: %s\nTo:   %s") % (strSrc, strDst)
            else:
                #operations like delete have no destination VFS
                strInfo = _("File: %s") % strSrc
            self.m_wndInfoLabel.SetLabel(strInfo)


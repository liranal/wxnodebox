from wxPython.wx import *
#from wxPython.lib import newevent
#UpdateBarEvent, EVT_UPDATE_BARGRAPH = newevent.NewEvent()

class OpState:
    def __init__ (self):
        self.m_bAbort = False
        self.m_pWndProgress = None
        self.m_nCurBytesPos = 0
        self.m_nCurBytesMax = 0
        self.m_nTotBytesPos = 0
        self.m_nTotBytesMax = 0
        self.m_nProcessedFilesCount = 0
        self.m_nProcessedDirsCount = 0
        #self.francesc = true

    def Abort(self):
        #TODO
        #//multithread safe
        #wxCriticalSection cs
        #cs.Enter()
        #//signalize abort
        self.m_bAbort = True
        #cs.Leave()

    def InitCurrentFiles(self, szSrc, szDest):
        if(szSrc):
        #TODO?
        #if(szSrc != ''):
            self.m_strSrcFile  = szSrc
        else:
            self.m_strSrcFile = ''

        if(szDest):
            self.m_strDstFile = szDest
        else:
            self.m_strDstFile = ''

    def InitTotalProgress(self, nTotal):
        self.m_nTotBytesMax = nTotal


    def InitCurrentProgress(self, nStartPos, nTotal):
        self.m_nCurBytesPos = nStartPos
        self.m_nCurBytesMax = nTotal

    def StepPos(self, nAmount):
        #print "step pos", nAmount, self.m_nCurBytesPos,
        self.m_nCurBytesPos += nAmount
        self.m_nTotBytesPos += nAmount

        #//ASSERT(m_nCurBytesPos <= m_nCurBytesMax);
        #//RecalcPercent();
        self.NotifyProgress()

    def SetPos(self, nAmount):
        self.m_nTotBytesPos += (nAmount - m_nCurBytesPos);
        self.m_nCurBytesPos = nAmount;

        #//ASSERT(m_nCurBytesPos <= m_nCurBytesMax);
        #//RecalcPercent();

        self.NotifyProgress();

    def NotifyProgress(self):
        #//ASSERT(NULL != m_hwndDlg && ::IsWindow(m_hwndDlg));
        #//if(::IsWindow(m_hwndDlg))
        #//  ::PostMessage(m_hwndDlg, WMU_UPDATE_PROGRESS, 0, 0);

        event = wxCommandEvent ()
        event.SetEventType (wxEVT_COMMAND_BUTTON_CLICKED)
        event.SetId (9999)
        #event.m_isCommandEvent = True

        if(self.m_pWndProgress):
            #print self.m_pWndProgress, self.m_pWndProgress.GetParent()

            #print 'proc'
            #evt = UpdateBarEvent(1, 1)
            #wxPostEvent(self.m_pWndProgress, evt)

            #if self.francesc:
            #    self.francesc = false
            #print 'proc'
                #print 'b', thread.get_ident()
                #print self.m_pWndProgress

            #Versuch
            wxPostEvent(self.m_pWndProgress, event)
            #self.m_pWndProgress.AddPendingEvent (event)
            #self.m_pWndProgress.ProcessEvent(event)

    def IsAborted(self):
        return self.m_bAbort

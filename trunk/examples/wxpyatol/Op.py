from OpManager import *
from OpState import *
import thread
#import time

#include 'wx/thread.h'
#include 'Vfs.h'
#include 'VfsSelection.h'
#include 'OpState.h'

#operation class

from wxPython.wx import *

class Op: #public wxThread
    def __init__ (self):  #wxThread(wxTHREAD_JOINABLE)
        #self.t = 0;
        self.m_pManager = None
        self.m_bError = False;
        self.m_pVfsSrc = None
        self.m_pVfsDst = None
        self.m_objSrcItems = VfsSelection()
        self.m_pManager = None
        self.m_Stat = OpState ()

        #ID_Timer = wxNewId()
        #print ID_Timer
        #self.timer = wxTimer(self, ID_Timer)
        #EVT_TIMER(self,  ID_Timer, self.OnTimer)
        #self.timer.Start(1000)
        #OpManager *m_pManager;

    #def OnTimer(self, event):
    #    self.t = self.t + 1
    #    #print 'timer'

    def Create (self):
        #TODO: insert code
        #print 'create thread'
        thread.start_new_thread(self.Run, ())
        #wait = wxBusyCursor ();

        #for i in range (100000):
            #print i

    def Run (self):
        #TODO: insert code (from import thread?)
        #run thread
        #print 'run'

        self.Entry()
        #wait = wxBusyCursor ();
        #for i in range (100000):
            #print i

        #print 'exit'
        #thread.exit()
        pass

    def RunOperation(self):
        #//create the thread
        #print 'Run Operation1'

        self.Create()
        #//starts modal progress dialog (it will start the thread)
        self.OpInit()
        #ifdef __GNUWIN32__
        #print 'Run Operation2'
        #self.Run()
        #endif

    def Entry(self):
        #print 'entry'
        #print 'a', thread.get_ident()
        self.OpExecute()
        self.OpCleanup()
        #ifdef __WXMSW__
        #//end thread
        thread.exit()
        #print 'exit'
        #endif
        self.m_pManager.OnOperationDone(self)
        return None

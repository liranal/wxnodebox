from Op import *
from VfsSelection import *
from VfsListing import *
#from OpCopy import *
#include 'OpDelete.h'
#include 'AtolApp.h'
#include 'MainFrame.h'
#include 'opcodes.h'
#include 'wx/thread.h'


class OpDelete(Op):
    def __init__ (self):
        Op.__init__ (self)
        self.m_pDlg = None
        #//flags
        self.m_nOpSettings = 0

        #TODO
        #extern wxSemaphore g_objGUISyncSemaphore;
        #extern int  g_nGuiResult;
        #extern wxString g_strTitle;


    def OpInit (self):
        ##ifndef __GNUWIN32__                  // problem with thread (dialog will not be created)
        # m_pDlg = new CProgressDlg;
        ##endif
        self.m_pDlg = self.m_pManager.m_pDlg

        #ifndef __GNUWIN32__
        #    if(m_pDlg){
        #    m_pDlg->Create(NULL, 1, _('Operation in progress ...'), wxDefaultPosition, wxDefaultSize, wxCAPTION);
        #    m_pDlg->m_pOp = this;
        #    m_pDlg->ShowModal();
        #    }
        #else
        self.m_Stat.m_pWndProgress = self.m_pManager.m_pDlg
        self.m_pDlg.m_pOp = self
        #endif

    def OpCleanup (self):
        if(self.m_pDlg):
            self.m_pDlg.Show(False)
            self.m_pDlg.Destroy()  #will delete the object
            #// #ifdef __GNUWIN32__
            #// delete m_pDlg;                   // no need to do this
            #// #endif
            self.m_pDlg = None



    def OpExecute(self):
        #//copy files from one VFS to the another
        #//Step 1: Expand selection (NOTE: we use file count for delete progress info)
        #//TOFIX pass full Stat
        self.m_pVfsSrc.ExpandSelection(self.m_objSrcItems, self.m_Stat.m_bAbort)
        self.m_Stat.m_nTotBytesMax = self.m_objSrcItems.GetTotalCount()

        #//STEP 2: delete reucrsively
        #//in case of abort
        strDir = self.m_pVfsSrc.GetDir()

        nRootCount = len (self.m_objSrcItems.m_lstRootItems)
        #print strDir, nRootCount, self.m_objSrcItems.m_lstRootItems[0].m_strName
        for i in range (nRootCount):
            #check for abort, ...
            if self.m_Stat.IsAborted():
                break

            #//delete previous temporary flags
            self.m_nOpSettings &= ~(OPF_TMP_FLAGS_MASK)

            if(not(self.m_nOpSettings & OPF_DEL_ALL_DIRS) and self.m_objSrcItems.m_lstRootItems[i].IsDir() and
                len (self.m_objSrcItems.m_lstRootItems[i].m_lstSubItems) > 0):
                #//TOFIX
                strCurPath = self.m_pVfsSrc.GetDir() + '/' + self.m_objSrcItems.m_lstRootItems[i].GetName()
                self.m_nOpSettings |= OpDeleteDirDlgThreadsafe(strCurPath)

            if(OPF_ABORT & self.m_nOpSettings):
                break

            if(OPF_SKIP & self.m_nOpSettings):
                continue

            #print "2", self.m_objSrcItems.m_lstRootItems[i]
            self.DeleteRecursive(self.m_objSrcItems.m_lstRootItems[i])

        #//restore starting dir
        self.m_pVfsSrc.SetDir(strDir)
        return True

    def DeleteRecursive(self, item):
        #print "rec", item.m_strName
        #//check for abort, ...
        if(self.m_Stat.IsAborted()):
            return;

        strItem = item.GetName();
        #print "3", strItem

        if(item.IsDir()):
            if(not item.IsDots()):
                #//store current dir position, set panels to new dir
                strSrcDir = self.m_pVfsSrc.GetDir()
                #print strSrcDir
                #//TOFIX
                strNewDir = strSrcDir + '/' + strItem
                #strNewDir = strSrcDir
                #print "4", strNewDir

                #//TOFIX verify success
                self.m_pVfsSrc.SetDir(strNewDir)

                #//delete directory contents
                nCount = len (item.m_lstSubItems)
                for i in range (nCount):
                    #//check for abort, ...
                    if(self.m_Stat.IsAborted()):
                        break

                    self.DeleteRecursive(item.m_lstSubItems[i])

                #//restore previous dir
                self.m_pVfsSrc.SetDir(strSrcDir)

                if(self.m_Stat.IsAborted()):
                    return

                #//NOTE do this before initsingle
                self.m_Stat.InitCurrentFiles(strSrcDir + strItem, NULL)
                self.m_Stat.InitCurrentProgress(0, 1)

                #//next delete directory itself
                #print "del1:", item.GetName()

                if not self.m_pVfsSrc.Delete(item.GetName(), self.m_nOpSettings):
                    #//TOFIX cumulative error collection -> message 'Some files could not be deleted' -> like deleting an current directory
                    strMsg = _("Failed to delete %s!") % strItem

                    #//TOFIX support for retry
                    if(OPF_ABORT == OpDeleteErrMessageThreadsafe(strMsg)):
                        self.m_Stat.Abort()
                        return

                #//check if user aborted inside delete
                if(self.m_nOpSettings & OPF_ABORT):
                    self.m_Stat.Abort()
                    return

                self.m_Stat.StepPos(1)
        else:
            #//NOTE do this before initsingle
            strSrcDir = self.m_pVfsSrc.GetDir();
            self.m_Stat.InitCurrentFiles(strSrcDir + '/' + strItem, NULL)
            self.m_Stat.InitCurrentProgress(0, 1)
            #print "del2:", item.GetName()
            if not self.m_pVfsSrc.Delete(item.GetName(), self.m_nOpSettings):
                #//TOFIX error handling, error dialog, abort operation?
                strMsg = _("Failed to delete %s!") % strItem

                #//TOFIX support for retry
                if(OPF_ABORT == OpDeleteErrMessageThreadsafe(strMsg)):
                    self.m_Stat.Abort()
                    return

            self.m_Stat.StepPos(1);

def OpDeleteDirDlgThreadsafe(szPath):
    #print "OpDeleteDirDlgThreadsafe"
    event = wxCommandEvent ()
    event.SetEventType (wxEVT_COMMAND_BUTTON_CLICKED)
    event.SetId (20001)

    g_strTitle = szPath

    #DECLARE_APP(AtolApp)
    pFrm = wxGetApp().GetFrame()
    if(pFrm):
        wxPostEvent(pFrm, event)

    #TODO
    #wxYield();
    #//wait for GUI to end with dialog
    #g_objGUISyncSemaphore.Wait();

    #return g_nGuiResult;
    return 0

def OpDeleteErrMessageThreadsafe(szMessage):
    #print "OpDeleteErrMessageThreadsafe"
    event = wxCommandEvent ()
    event.SetEventType (wxEVT_COMMAND_BUTTON_CLICKED)
    event.SetId (20002)

    g_strTitle = szMessage

    #DECLARE_APP(AtolApp)
    pFrm = wxGetApp().GetFrame()
    if(pFrm):
        wxPostEvent(pFrm, event)

    #wxYield();
    #g_objGUISyncSemaphore.Wait();   //wait for GUI to end with dialog

    #return g_nGuiResult;


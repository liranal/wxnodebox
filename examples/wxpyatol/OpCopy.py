from wxPython.wx import *
from Op import *
from VfsSelection import *
from VfsListing import *
from Globals import *

class OpCopy(Op):
    def __init__ (self):
        Op.__init__(self)
        #CProgressDlg  *m_pDlg;

        #virtual void OpInit();
        #virtual void OpCleanup();
        #virtual bool OpExecute();

        self.m_nOpSettings = 0  #flags
        self.m_lstDstDir = VfsListing ()
        self.m_pDlg = None

        #extern wxSemaphore g_objGUISyncSemaphore;
        #extern int  g_nGuiResult;
        #extern wxString g_strTitle;
        #extern wxString g_strResult;

    def OpInit (self):
        #problem with thread (dialog will not be created)
        #ifndef __GNUWIN32__
        #m_pDlg = new CProgressDlg;
        #endif
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

    def OpExecute (self):
        #copy files from one VFS to the another
        #//STEP 1: check if copy allowed (copy over itself is forbidden)
        if(self.m_pVfsSrc.GetType() == self.m_pVfsDst.GetType()):
            #check if copying file to itself (its own directory)
            #//TOFIX *m_pVfsDst == *m_pVfsSrc
            if(self.m_pVfsSrc.GetDir()  == self.m_pVfsDst.GetDir()):
                wxMessageBox(_("You cannot copy a file to itself!"))
                return False

            #check if copying some content into its own subdirectory (forbidden)
            strDest = self.m_pVfsDst.GetDir()

            #if destination dir is child of any dirs in the source
            nCount = len(self.m_objSrcItems.m_lstRootItems)
            #print '1', nCount, self.m_objSrcItems[0], self.m_objSrcItems.m_lstRootItems
            for i in range(nCount):
                if(self.m_objSrcItems.m_lstRootItems[i].IsDir()):
                    strSource = self.m_pVfsSrc.GetDir() + self.m_objSrcItems.m_lstRootItems[i].GetName()
                    nSrcLen   = len (strSource)
                    if(nSrcLen == StrCommonPrefixLen(strDest, strSource)):
                        wxMessageBox(_("You cannot copy directory into its own subdirectory!"))
                        return False

        #STEP 2:  expand selection recursively into subdirectories (total size calculation)
        #//TOFIX pass full Stat
        #print '2', self.m_objSrcItems
        self.m_pVfsSrc.ExpandSelection(self.m_objSrcItems, self.m_Stat.m_bAbort)
        self.m_Stat.m_nTotBytesMax = self.m_objSrcItems.GetTotalSize()
        self.m_pVfsDst.ListDir(self.m_lstDstDir, self.m_Stat.m_bAbort)

        #STEP 3:  copy (recursively)
        nRootCount = len (self.m_objSrcItems.m_lstRootItems)
        for i in range (nRootCount):
            #check for abort
            if(self.m_Stat.IsAborted()):
                break
            self.CopyRecursive(self.m_objSrcItems.m_lstRootItems[i])

        return True

    #def CopyRecursive(VfsSelectionItem &item)
    def CopyRecursive(self, item):
        #check quit flags
        if(self.m_Stat.IsAborted()):
            return

        if(item.IsDir()):
            if not item.IsDots():
                #store current dir positions
                strSrcDir = self.m_pVfsSrc.GetDir()
                strDestDir = self.m_pVfsDst.GetDir()

                #create new directory
                #set both panels to matching dirs
                #//TOFIX check success
                self.m_pVfsSrc.SetDir(strSrcDir + '/' + item.GetName())

                strDirName = item.GetName()
                #//dir might have existed before
                self.m_pVfsDst.MkDir(strDirName)

                strPathDst = strDestDir
                #//TOFIX
                strPathDst += '/'
                strPathDst += strDirName

                #//TOFIX check success
                self.m_pVfsDst.SetDir(strPathDst)
                self.m_pVfsDst.ListDir(self.m_lstDstDir, self.m_Stat.m_bAbort)

                #copy all entries to new dir
                nCount = len (item.m_lstSubItems)
                for i in range (nCount):
                    #check quit flags
                    if(self.m_Stat.IsAborted()):
                        break
                    self.CopyRecursive(item.m_lstSubItems[i])

                #restore previous dirs
                #//VERIFY
                self.m_pVfsSrc.SetDir(strSrcDir)
                #//VERIFY
                self.m_pVfsDst.SetDir(strDestDir)
                if(not self.m_Stat.IsAborted()):
                    self.m_pVfsDst.ListDir(self.m_lstDstDir, self.m_Stat.m_bAbort)

                #//TOFIX? copy directory properties to new created (time+attrib)
                #//       (this requires VFS::SetAttributes(time, attrib);
        else:
            #//NOTE: use file name only - path is known
            self.SingleFileCopy(item)

    #def SingleFileCopy(VfsSelectionItem &item)
    def SingleFileCopy(self, item):
        #//check quit flags
        if(self.m_Stat.IsAborted()):
            return False

        #//if the file already exists at destination
        strSearch = item.GetName()

        #//if item of same name exists at destination
        nItem = self.m_lstDstDir.FindItem(strSearch)
        if(-1 != nItem):
            #delete previous temporary flags
            self.m_nOpSettings &= ~(OPF_TMP_FLAGS_MASK)

            #//if the copy settings were not previously set
            if( not(self.m_nOpSettings & OPF_CPY_OVERWRITE_ALL)    and
                not(self.m_nOpSettings & OPF_CPY_SKIP_ALL)         and
                not(self.m_nOpSettings & OPF_CPY_OVERWRITE_ALL_OLDER)):
            #{
                self.m_nOpSettings |= DlgOverwriteThreadsafe(strSearch)
            #}

            #check if rename required
            if(self.m_nOpSettings & OPF_CPY_RENAME):
                while(True):
                    nRes, strSearch = self.DlgNameInputThreadsafe(_("New file name"))
                    if(wxOK == nRes):
                        nItem = self.m_lstDstDir.FindItem(strSearch)
                        if(-1 == nItem):
                            #//valid non-overwriting name
                            break

                        strMsg = _("File %s already exists!") % strSearch
                        wxMessageBox(strMsg)
                    else:
                        #//skip if canceled
                        self.m_nOpSettings |= OPF_SKIP
                        break

            if(OPF_ABORT & self.m_nOpSettings):
                #//abort requested
                self.m_Stat.Abort()
                return False

            if( (OPF_SKIP & self.m_nOpSettings) or (OPF_CPY_SKIP_ALL & self.m_nOpSettings)):
                return False

            #//TOFIX? add support for OPF_CPY_OVERWRITE_ALL_OLDER

            if ((OPF_CPY_OVERWRITE_ALL & self.m_nOpSettings) or (OPF_OVERWRITE & self.m_nOpSettings)):
                if(not self.m_pVfsDst.Delete(item.GetName(), self.m_nOpSettings)):
                    strMsg = _("Failed to overwrite %s!") % item.GetName()
                    #//TOFIX support for Retry|Cancel
                    wxMessageBox(strMsg)
                    return False
                    #//TOFIX retry/cancel/continue code

        #//check for drive free space (after we have possibly deleted file with same name)
        nFreeSpace = self.m_pVfsDst.GetDriveFreeSpace()
        if(nFreeSpace < item.m_nSize):
            strMsg = 'There is no free space on target drive\nto copy file %s.\nAborting operation!' % item.GetName()

            s = 'free:%d' % nFreeSpace
            wxMessageBox(strMsg, s)

            #TODO: hinein
            #self.m_Stat.Abort()
            #return False

        #//in case of resume start copy from some file offset
        nOffset = 0
        if(OPF_CPY_RESUME & self.m_nOpSettings):
            nOffset = item.m_nSize

        #//
        #// copy operation itself
        #//
        bRes = True

        self.m_pVfsSrc.m_pProgress = self.m_Stat
        self.m_pVfsDst.m_pProgress = self.m_Stat

        #//TOFIX check if the user here inside required operation ABORT (pass m_nOpSettings)
        #print item, strSearch, self.m_pVfsDst, nOffset
        if not self.m_pVfsSrc.Copy(item, strSearch, self.m_pVfsDst, nOffset):
            strMsg = _("Failed to copy %s!") % item.GetName()
            #//TOFIX support for Retry|Cancel
            wxMessageBox(strMsg)
            bRes = False

        return bRes

def StrCommonPrefixLen(szPath1, szPath2):
    #print "len", szPath1, szPath2
    nLen = 0
    #TODO: (also in atol)
    #nlenszPath1 = len (szPath1)
    #if(szPath1 != "" and szPath2 != ""):
    #    while (nLen < len (szPath1) and nLen < len (szPath2) and szPath1[nLen] == szPath2[nLen]):
    #        nLen += 1
    return nLen


#//use events to ask main window to do this for us in the main thread
#//TOFIX use custom event with my additional variables storing the data
def DlgOverwriteThreadsafe(strFile):
    #print "DlgOverwriteThreadsafe"
    g_strTitle = _("Overwrite %s ?") % strFile

    event = wxCommandEvent ()
    event.SetEventType (wxEVT_COMMAND_BUTTON_CLICKED)
    event.SetId (19999)
    #event.m_isCommandEvent = True

    #event.m_isCommandEvent = True
    ##wxPostEvent(self.m_pLeftPanel, event)
    ##self.m_pLeftPanel.ProcessEvent(event)
    #self.m_pLeftPanel.AddPendingEvent(event)

    #  DECLARE_APP(AtolApp)
    pFrm = wxGetApp().GetFrame()
    if(pFrm):
        wxPostEvent(pFrm, event)

    wxYield()
    #//wait for GUI to end with owerwrite dialog

    #TODO
    #g_objGUISyncSemaphore.Wait();
    return g_nGuiResult;

def DlgNameInputThreadsafe(strTitle, strValue):
    #print "DlgNameInputThreadsafe"

    event = wxCommandEvent ()
    event.SetEventType (wxEVT_COMMAND_BUTTON_CLICKED)
    event.SetId (20000)

    pFrm = wxGetApp().GetFrame()
    if(pFrm):
        wxPostEvent(pFrm, event)

    wxYield();
    #TODO
    #g_objGUISyncSemaphore.Wait();   //wait for GUI to end with owerwrite dialog
    strValue = g_strResult

    return g_nGuiResult, strValue



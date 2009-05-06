from Op import *
from VfsSelection import *
from VfsListing import *
from OpCopy import *

class OpMove(OpCopy):
    def __init__(self):
        OpCopy.__init__(self)
        self.m_bMoveDirect = False


    #extern wxSemaphore g_objGUISyncSemaphore;
    #extern int  g_nGuiResult;


    def OpExecute (self):
        #STEP 1: check if move allowed (copy over itself is forbidden)
        if(self.m_pVfsSrc.GetType() == self.m_pVfsDst.GetType()):
            #check if copying file to itself (its own directory)
            #//TOFIX *m_pVfsDst == *m_pVfsSrc
            if(self.m_pVfsSrc.GetDir()  == self.m_pVfsDst.GetDir()):
                wxMessageBox(_("You cannot move a file to itself!"))
                return False

            #check if copying some content into its own subdirectory (forbidden)
            strDest = self.m_pVfsDst.GetDir()

            #if destination dir is child of any dirs in the source
            nCount = len(self.m_objSrcItems.m_lstRootItems)
            for i in range(nCount):
                if(self.m_objSrcItems.m_lstRootItems[i].IsDir()):
                    strSource = self.m_pVfsSrc.GetDir() + self.m_objSrcItems.m_lstRootItems[i].GetName()
                    nSrcLen   = len (strSource)

                    if(nSrcLen == StrCommonPrefixLen(strDest, strSource)):
                        wxMessageBox(_("You cannot move directory into its own subdirectory!"))
                        return False

        #STEP 2:  expand selection recursively into subdirectories (total size calculation)
        #//TOFIX pass full Stat
        self.m_pVfsSrc.ExpandSelection(self.m_objSrcItems, self.m_Stat.m_bAbort)
        self.m_Stat.m_nTotBytesMax = self.m_objSrcItems.GetTotalSize()

        #STEP 3: check move type (direct or Copy()+Delete())
        self.m_bMoveDirect = false;

        if(self.m_pVfsSrc.GetType() == self.m_pVfsDst.GetType()):
            #TOFIX for lINUX check if the paths are within the same disk partition
            if(self.m_pVfsSrc.GetDir()[:3] == self.m_pVfsDst.GetDir()[:3]):
                self.m_bMoveDirect = true;

        self.m_pVfsDst.ListDir(self.m_lstDstDir, self.m_Stat.m_bAbort);

        #STEP 3:  copy (recursively)
        nRootCount = len (self.m_objSrcItems.m_lstRootItems)
        for i in range(nRootCount):
            #check for abort
            if(self.m_Stat.IsAborted()):
                break
            self.MoveRecursive(self.m_objSrcItems.m_lstRootItems[i])
        return True

    #def MoveRecursive(VfsSelectionItem &item)
    def MoveRecursive(self, item):
        #//check for abort, ...
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

                #move all entries to new dir
                nCount = len (item.m_lstSubItems)
                for i in range (nCount):
                    #check quit flags
                    if(self.m_Stat.IsAborted()):
                        break
                    self.MoveRecursive(item.m_lstSubItems[i])

                #restore previous dirs
                #//VERIFY
                self.m_pVfsSrc.SetDir(strSrcDir)
                #//VERIFY
                self.m_pVfsDst.SetDir(strDestDir)


                #IMPORTANT: check for abort before deleting original directory !!!!
                if(self.m_Stat.IsAborted()):
                    return

                self.m_pVfsDst.ListDir(self.m_lstDstDir, self.m_Stat.m_bAbort)

                #delete directory
                self.m_pVfsSrc.Delete(item.GetName(), self.m_nOpSettings)
        else:
            self.SingleFileMove(item)

    def SingleFileMove(self, item):
        #//check quit flags
        if(self.m_Stat.IsAborted()):
            return False

        bError = False

        #//if the file already exists at destination
        strSearch = item.GetName()

        strDest = self.m_pVfsDst.GetDir()
        #//TOFIX
        if not (strDest [-1] == '\\' or strDest [-1] == '/'):
            strDest += '/'

        strDest += strSearch

        if(self.m_bMoveDirect):
            nItem = self.m_lstDstDir.FindItem(strSearch)
            if(-1 != nItem):
                #delete previous temporary flags
                self.m_nOpSettings &= ~(OPF_TMP_FLAGS_MASK)

                #//TOFIX disable Resume button
                #//if the copy settings were not previously set
                if( not(self.m_nOpSettings & OPF_CPY_OVERWRITE_ALL)    and
                    not(self.m_nOpSettings & OPF_CPY_SKIP_ALL)         and
                    not(self.m_nOpSettings & OPF_CPY_OVERWRITE_ALL_OLDER)):
                #{
                    self.m_nOpSettings |= self.DlgOverwriteThreadsafe(strSearch)
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

                            wxMessageBox(_("File with that name already exists!"))
                        else:
                            #//skip if canceled
                            self.m_nOpSettings |= OPF_SKIP
                            break

                if(OPF_ABORT & self.m_nOpSettings):
                    self.m_Stat.Abort()
                    return False

                if( (OPF_SKIP & self.m_nOpSettings) or (OPF_CPY_SKIP_ALL & self.m_nOpSettings)):
                    return False

            #//TOFIX check result, check dest owerwrite, , ..
            #print "a0", bError
            bError = not self.m_pVfsSrc.Rename(self.m_pVfsSrc.GetDir() + '/' + strSearch, self.m_pVfsDst.GetDir() + '/' + strSearch);
            #print "a1", bError
        else:
            #//delete previous temporary flags
            self.m_nOpSettings &= ~(OPF_TMP_FLAGS_MASK)

            bOk = self.SingleFileCopy(item)
            #print "b", bOk

            #//on abort, do not erase original file
            if(self.m_Stat.IsAborted()):
                bOk = False
            #print "c", bOk

            if bOk:
                bOk = self.m_pVfsSrc.Delete(item.GetName(), self.m_nOpSettings);
            #print "d", bOk

            bError = not bOk;

            #//FIX: don't trigger 'Failed ...' message if that was user choice
            if( (OPF_SKIP & self.m_nOpSettings) or (OPF_CPY_SKIP_ALL & self.m_nOpSettings)):
                return False

        if(bError):
            #//TOFIX separate msg for copy and delete?
            strMsg = _("Failed to move %s!") % item.GetName()
            #//TOFIX support for Retry|Cancel
            wxMessageBox(strMsg);

        return not bError;


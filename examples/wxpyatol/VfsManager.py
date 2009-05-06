from Vfs import *
from VfsLocal import *
from VfsArchive import *
from os.path import *
#from FileListCtrl import *

class VfsManager:
    def __init__(self):
        self.m_mapStackIdx = {}
        self.m_lstStacks = []
        self.m_lstVfs = []
        self.pVfs = None

    #def InitList (FileListCtrl pList, Vfs pVfs = NULL):
    def InitList (self, pList, pVfs = None):
        #print 'init List'
        #create new Vfs stack for this list control object (if not already done)
        if self.m_mapStackIdx.get (pList, 0) == 0:
            #stack does not exist for this list, create new one
            #tVfsStack stack;
            stack=[]
            stack.append (Vfs())
            self.m_lstStacks.append (stack)
            #typedef std::vector<Vfs *> tVfsStack;

            #remember stack index
            self.m_mapStackIdx[pList] = len (self.m_lstStacks) - 1

        if (None == pVfs):
          pVfs = Vfs_Local()

        self.VfsStackPush(pList, pVfs)

        # TOFIX: remove this
        #ifdef __WXMSW__
        pList.SetDirectory ('C:\\')
        #auch moeglich
        #pList.SetDirectory ('/')
        #pList.SetDirectory ('C:\\recycled/temp')
        #pList.SetDirectory ('/recycled')
        #pList.SetDirectory ('C:\\recycled')

        #else
        #pList.SetDirectory('/');
        #endif

    #bool VfsManager::CheckForSubVfs(FileListCtrl *pList, Vfs *pVfs, VfsItem &item)
    def CheckForSubVfs(self, pList, pVfs, item):
        strFullPath = pVfs.GetDir() + '/' + item.GetName()

        #//TOFIX? simplify
        #//TOFIX? support for archives on remote Vfs (download/unpack)
        if pVfs.GetType() == VFS_LOCAL or pVfs.GetType() == VFS_NET:
            #//TOFIX support for ".enc" format
            #//suport for compressed archives
            #//TOFIX check magic numbers
            #Vfs_Archive *pArchiveVFS = new Vfs_Archive;
            pArchiveVFS = Vfs_Archive()
            if pArchiveVFS.InitArchiver (strFullPath):
                pArchiveVFS.m_strArchiveFile = strFullPath
                if not pArchiveVFS.Open():
                    wxMessageBox(_("Error in packed file!"))
                    return False

                #//switch to new Vfs
                VfsStackPush(pList, pArchiveVFS)
                return True
        elif pVfs.GetType() == VFS_ARCHIVE:
            #//check for archive in archive -> extract selected archive item into temp directory
            pArchiveVFS = Vfs_Archive ()
            if pArchiveVFS.InitArchiver(strFullPath):
                #//TOFIX separate fn -> CreateTempPath
                #//create temporary path
                #int i=0;
                i = 0
                #strDestPath = ""
                tmpPath =  PathName ()
                strDestPath = tmpPath.Path_TempDirectory() + item.GetName()
                #TOMAKEBETTER: what does this do exactly?
                while os.path.isfile(strDestPath):
                    strDestPath = "%s%d%s" % (tmpPath.Path_TempDirectory(), i, item.GetName())
                    i += 1
                    if i > 40:
                        return False

                #//TOFIX progress dialog
                pVfs.m_pProgress = 0
                #//extract file to temp under unique name
                if not pVfs.CopyToLocal(item, strDestPath):
                    return False

                #//when having archive in archive, we don't want to show
                #//true path of internal archive (unpacked in temp dir)
                #//so we set custom title
                pArchiveVFS.m_strArchiveFile  = strDestPath
                pArchiveVFS.m_strTitle = item.GetName()
                #//delete temporary archive file when Vfs closes
                pArchiveVFS.m_bDeleteFile = True

                if not pArchiveVFS.Open():
                    wxMessageBox(_("Error in packed file!"))
                    return False

                #//switch browser
                VfsStackPush(pList, pArchiveVFS);
                return True
            else:
                #//archiver not initialized - not an archive within archive
                #delete pArchiveVFS;
                pass
        return False

    #def CheckForUpVfs(FileListCtrl *pList, Vfs *pVfs)
    def CheckForUpVfs(self, pList, pVfs):
        if ((pVfs.GetType() == VFS_ARCHIVE) or (pVfs.GetType() == VFS_SITEMAN)):
            #//switch to previous VFS
            if self.VfsStackPop(pList):
                pVfs.Close()
                return True
        return False


    #def VfsStackPush(FileListCtrl *pList, Vfs *pVfs)
    def VfsStackPush(self, pList, pVfs):
        #link Vfs to the list
        #print 'vfsstackpush', pList, pVfs
        pList.m_pVfs = pVfs

        #store Vfs pointer into global and per-list stack
        self.m_lstVfs.append(pVfs)

        nPos = self.m_mapStackIdx[pList];
        #print nPos, self.m_lstStacks[nPos], type (self.m_lstStacks[nPos])
        self.m_lstStacks[nPos].append(pVfs)

    #//remove top Vfs from stack, but do not delete it (API user will have to do it)
    #bool VfsManager::VfsStackPop(FileListCtrl *pList)
    def VfsStackPop (self, pList):
        nStIdx  = self.m_mapStackIdx[pList];
        nStSize = len (m_lstStacks[nStIdx])
        #//at least one Vfs must stay in the list
        if nStSize > 1:
            #//take top/last Vfs
            pVfs = m_lstStacks[nStIdx][nStSize-1]
            #//shrink list stack
            m_lstStacks[nStIdx].pop()
            #//find and remove from global Vfs list
            for i in len (m_lstVfs):
                if m_lstVfs[i] == pVfs:
                    m_lstVfs.delete(i)

            #//link new top Vfs for list control
            #//-2 -> account for deleted Vfs
            pList.m_pVfs = self.m_lstStacks[nStIdx][nStSize-2]
            return True
        return False

    #wxString VfsManager::GetPathTitle(FileListCtrl *pList)
    def GetPathTitle (self, pList):

        nStIdx  = self.m_mapStackIdx[pList]
        nStSize = len (self.m_lstStacks[nStIdx])
        strTitle = ''
        if (nStSize > 0):
            #for i in m_lstStacks[nStIdx]:
            for i in range (nStSize):
                strTitle = strTitle + self.m_lstStacks[nStIdx][i].GetPathTitle()
                #todolinux
                #if (i < nStSize-1):
                #    strTitle = strTitle + '/'

        return strTitle;


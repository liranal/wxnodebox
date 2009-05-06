from wxPython.wx import *
import thread
from Vfs import *
from VfsListing import *
from FilterDesc import *
from VfsLocal import *

#TOFIX inherit Op class ?

'''
#if not wxThread_IsMain():
import thread
        thread.start_new_thread(self.Run, ())
        self.threads.append(CalcBarThread(self, 7, 175))
        for t in self.threads:
            t.Start()
from threading import *
class Searcher(Thread):
    def __init__(self, app, searchwindow, condition):
        Thread.__init__(self, name = 'Searcher')

'''

#class FileSearchThread(wxThread):
class FileSearchThread:
    def __init__(self):
        #search info
        self.m_objInfo = FilterDesc ()
        self.m_strDirectory = ''
        #self.m_pWnd = wxWindow ()
        self.m_pWnd = None
        #self.m_pResultLst = VfsListing ()
        self.m_pResultLst = None
        self.m_bAbort = False
        self.m_bDone = False

    def AddItem(self, item): #VfsItem &item)
        #TOFIX use mutex to synchronize
        #insert into result list
        self.m_pResultLst.Insert(item)
        #pSheet->m_nFilesFound ++;

        Ctrl = self.m_pWnd.m_wndResultList
        nPos = Ctrl.GetItemCount()
        Ctrl.InsertStringItem(nPos, item.GetTitle())
        Ctrl.SetStringItem(nPos, 1, item.GetExt())
        Ctrl.SetStringItem(nPos, 2, item.GetPath())
        Ctrl.SetStringItem(nPos, 3, item.GetSize())
        Ctrl.SetStringItem(nPos, 4, item.GetDate())
        Ctrl.SetStringItem(nPos, 5, item.GetAttr())
        #//::PostMessage(pSheet->m_hWndParent, WMU_REFRESH_INFO, 0, 0);

    def IsRunning(self):
        #TODO: correct
        return not self.m_bDone

    def Create(self):
        #TODO: correct
        thread.start_new_thread(self.Run, ())

    def Run(self):
        #TODO: correct
        self.Entry()

    def Abort(self):
        #multithread safe
        #TODO
        #cs = wxCriticalSection ()
        #cs.Enter()

        #signalize abort
        self.m_bAbort = True

        #cs.Leave()

    def Entry(self):
        #print "entry"
        self.m_bDone = False

        if(self.m_pResultLst):
            pVfs = None

            #get next directory token (multiple names separated with ;)
            strDir = ''
            nLength   = len(self.m_strDirectory)
            nStartPos = 0
            nEndPos   = 0

            while(nStartPos < nLength):
                #check abort
                if(self.m_bAbort):
                    self.m_bDone = True
                    return NULL

                #get next path token
                nEndPos = self.m_strDirectory.find(';', nStartPos)
                #print "1"
                if(nEndPos > 0):
                    #get the piece of the string
                    strDir = self.m_strDirectory[nStartPos : nEndPos-nStartPos]
                    #print "2", strDir
                    nStartPos = nEndPos + 1;
                else:
                    #get the rest of the string
                    #TODO:
                    strDir = self.m_strDirectory[nStartPos : nLength-nStartPos]
                    nStartPos = nLength
                    #print "3", strDir

                #delete previous VFS
                if(None != pVfs):
                    #delete pVfs;
                    pVfs = None

                #TOFIX move to vfsManager, support for archives?
                #use different VFS objects depending on search path type
                #if(PathIsUNC(strPath))
                #  pVFS = new Vfs_Net;
                #else
                pVfs = Vfs_Local ()

                if(None == pVfs):
                    break

                #search in this path
                if(pVfs.SetDir(strDir)):
                    #print "hi", strDir
                    list = VfsListing ()
                    pVfs.ListDir(list, self.m_bAbort)

                    #keep only items that satisfy the search terms
                    nSize = list.GetCount()
                    for i in range (nSize):
                        if(self.m_bAbort):
                            break

                        #pSheet->m_nFilesSearched ++;

                        #dots are not being part of the search result
                        if(list.GetAt(i).IsDots() == False):
                            #set item absolute path
                            #//TOFIX SetPath
                            list.GetAt(i).m_strPath = pVfs.GetDir()

                            item = list.GetAt(i)

                            #filter by search data (name, ...)
                            if(self.m_objInfo.Match(item)):
                                self.AddItem(item)

                    #now use same directory and its list to do recursive subdir processing if needed
                    if(self.m_pWnd.m_bRecursive):
                        if(self.m_bAbort):
                            break
                        self.RecursiveList(pVfs, list)

            #if(None != pVfs):
            #    delete pVfs;

        #((CFileSearchDlg *)m_pWnd)->m_wndOkBtn.SetLabel(_("Search"));
        self.m_pWnd.m_wndOkBtn.SetLabel(_("Search"))
        #//wxMessageBox('Done!');
        m_bDone = true

        #ifdef __WXMSW__
            #end thread

        #TODO: exit thread
        #self.Exit()
        # orthread.exit()

        #endif

        return NULL

#TOFIX? use VFS::ExpandList(CFileList &list, int nStart)
#void FileSearchThread::RecursiveList(Vfs *pVFS, VfsListing &lstRoot)
    def RecursiveList(self, pVFS, lstRoot):
        strDir = pVFS.GetDir()

        #for each subdir
        nSize = lstRoot.GetCountRaw()
        for i in range (nSize):
            if(self.m_bAbort):
                break

            #if subdir found
            #//TOFIX if subdir OR archive found
            if lstRoot.GetAt(i).IsDir() and not lstRoot.GetAt(i).IsDots():
                #list subdir
                #//TOFIX
                strPath = strDir + '/' + lstRoot.GetAt(i).GetName()
                if pVFS.SetDir(strPath):
                    #//TOFIX list into the temp
                    list = VfsListing ()
                    pVFS.ListDir(list, self.m_bAbort)

                    #keep only ones that satisfy the search terms
                    nSizeNew = list.GetCountRaw()
                    for j in range(nSizeNew):
                        if(self.m_bAbort):
                            break

                        #//m_nFilesSearched ++;

                        #dots are not being part of the search result
                        if(list.GetAtRaw(j).IsDots() == False):
                            #repair path
                            list.GetAtRaw(j).m_strPath = pVFS.GetDir()

                            #item VfsItem item;
                            item = list.GetAtRaw(j)

                            #filter by search data (name, ...)
                            if(self.m_objInfo.Match(item)):
                                self.AddItem(item)

                    #second pass to go deeper into recursion
                    #now use same directory and its list to do recursive subdir processing if needed
                    #//TOFIX member od CBrowser?
                    self.RecursiveList(pVFS, list)
            #// if SetDir
        #//for

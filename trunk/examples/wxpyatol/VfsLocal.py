from wxPython.wx import *
#from DirTraverser import *
from Vfs import *
from VfsItem import *
from VfsSelection import *
from Globals import *
#import time
#from   whrandom import random
import os
from MyDirTraverser import *
import win32file
import win32api
import win32con
#from stat import ST_ATIME, ST_MTIME, ST_MODE, S_IMODE
from stat import ST_MODE, S_ISREG, S_ISDIR#, S_ISLNK
from WxUtil import *

class Vfs_Local(Vfs):

    def __init__(self):
        Vfs.__init__ (self)
        self.m_strCurDir = ''
        #self.file_list = wxArrayString ()
        self.file_list = []
        self.m_nType = VFS_LOCAL
        self.m_pProgress = NULL


    def SetDir (self, szPath):
        self.m_strCurDir = szPath
        return True

    #def istDir(VfsListing &list, bool &bAbort)
    def ListDir(self, list, bAbort):

        list.Clear()
        #list = MyDirTraverser (m_strCurDir)
        MyDirTraverser (list, self.m_strCurDir)
        #print list

        #traverser = DirTraverser (list)
        #dirs = wxDir (self.m_strCurDir)
        #dirs.Traverse(traverser)
        #dirs.GetAllFiles (self.file_list)

        #optionaly append '..' item (nach vorne)
        if (self.IsRootDir() == false):
        #if 1:
            item = VfsSelectionItem ()
            item.m_strName  = '..'
            #item.m_nSize = 54
            item.m_nAttrib  = ATTR_DIR
            #item.m_nAttrib  = 0
            #ifdef __WXGTK__
            #item.m_nAttrib |= ATTR_UNIX;
            #endif
            list.Insert(item)
            #print 'root', item, item.m_strName

        return true

    def IsRootDir(self):
    #ifdef __WXMSW__
        if(len (self.m_strCurDir) <= 3):
            return true
        else:
            return false

    #else
    #    if(m_strCurDir.Len() < 2)
    #        return true;
    #endif


    def MkDir(self, szName):
        #//TOFIX permissions?
        #//TOFIX ensure that string is terminated before adding new segment
        strPath = self.m_strCurDir + '/' + szName
        #wxpython
        i = os.mkdir (strPath)
        #print i
        return i
        #return os.path.mkdir (strPath)
        #return wxMkdir(strPath)

    #bool Vfs_Local::Delete(const char *szItem, int &nOpSettings)
    def Delete(self, szItem, nOpSettings):
        #if __WXMSW__
        strPath = self.m_strCurDir
        if not (self.m_strCurDir [-1] == '\\' or self.m_strCurDir [-1] == '/'):
            strPath += '/'
        strPath +=  szItem
        #print "bei delete", strPath

        dwAttr = win32file.GetFileAttributes(strPath)
        #//TOFIX add FILE_ATTRIBUTE_SYSTEM support
        #print "0"
        if ((-1 != dwAttr) and ((dwAttr & win32con.FILE_ATTRIBUTE_READONLY) == win32con.FILE_ATTRIBUTE_READONLY)):
            #//if the style was not set, ask the user what to do
            #print "1"
            if(not (nOpSettings & OPF_DEL_ALL_RO_FILES)):
                #print "2"
                #print "delete1"
                nOpSettings |= OpDeleteFileDlgThreadsafe(strPath)
                #print "delete2"
                if ((OPF_ABORT & nOpSettings) or (OPF_SKIP & nOpSettings)):
                    return False
                    #print "delete3"
        '''
        /*
            if(m_bRecycleBin)
            {
                //NOTE: this one does not need removing the style to delete the file
                if(MoveToTrash(strPath))
                    return true;
            }
        */
        '''
        #//Hard delete (if required or recycle failed)
        if(-1 != dwAttr and dwAttr & win32con.FILE_ATTRIBUTE_READONLY):
            #//remove read-only style (so delete API won't fail)
            dwAttr &= ~(win32con.FILE_ATTRIBUTE_READONLY);
            win32file.SetFileAttributes(strPath, dwAttr);

        #//TOFIX add wipe support (global ini settings)
        if(dwAttr & win32con.FILE_ATTRIBUTE_DIRECTORY):
            #//NOTE: dir should be empty at this point
            #return (::RemoveDirectory(strPath) > 0);
            #win32file.RemoveDirectory (strPath)

            #TODO:Anzeige nachher wieder richtig (refreshen)
            #print "delete in dir"

            #TOO remove?
            #self.walktree(strPath, self.removefile, self.removedir)
            os.rmdir(strPath)
            #TODO: evaluate: really true?
            return True

            #os.removedirs(strPath)
        else:
            os.remove (strPath)
            #TODO: evaluate: really true?
            return True
        '''
        #else
            //TOFIX support deleting readonly files
            wxString strPath = m_strCurDir + '/' + szItem;
            //return ::wxRemoveFile(strPath);
            return (0 == remove(strPath));
        #endif
        '''
    #TOMAKEBETTER: remove later: we won't need it
    '''
    def walktree(self, dir, callbackfile, callbackdir):
        ####recursively descend the directory rooted at dir,
        ####calling the callback function for each regular file or directory
        #print "walkdir:"
        for f in os.listdir(dir):
            pathname = '%s/%s' % (dir, f)
            mode = os.stat(pathname)[ST_MODE]
            if S_ISDIR(mode):
                # It's a directory, recurse into it
                self.walktree(pathname, callbackfile, callbackdir)
                callbackdir(pathname)
            elif S_ISREG(mode):
                # It's a file, call the callback function
                callbackfile(pathname)
            else:
                # Unknown file type, pr int a message
                #print 'Skipping %s' % pathname
                pass

    def removefile(self,file):
        """Remove a file"""
        dwAttr = win32file.GetFileAttributes(file)
        if ((dwAttr & win32con.FILE_ATTRIBUTE_READONLY) == win32con.FILE_ATTRIBUTE_READONLY):
            #print "set read only"
            dwAttr &= ~(win32con.FILE_ATTRIBUTE_READONLY);
            win32file.SetFileAttributes(file, dwAttr);

        os.remove (file)
        #os.unlink(file)

    def removedir(self,dir):
        """Remove a directory"""
        os.rmdir(dir)
    '''
    def Rename(self, szItem, szNewItem):
        #wxpython gibt es kein MoveFile
        #ifdef __WXMSW__
        #return ::MoveFile(szItem, szNewItem);
        #print szItem, szNewItem
        #i = os.rename (szItem, szNewItem)
        i = win32api.MoveFile (szItem, szNewItem)
        #TODO: returns None; should return success or not
        #   ...Maybe should use python ren or similar
        return True
        #print i
        #else
        #Unix
        #strSrc = self.m_strCurDir
        #strSrc += '/'
        #strSrc += szItem
        #strDst = self.m_strCurDir
        #strDst += '/'
        #strDst += szNewItem
        #return wxRenameFile(strSrc, strDst);
        #endif

    #bool Vfs_Local::Copy(VfsItem &item, const char *szNewName, Vfs *pVfsDest, wxInt64 nOffset)
    def Copy(self, item, szNewName, pVfsDest, nOffset):
        if(pVfsDest.GetType() == VFS_LOCAL):
            strDest = pVfsDest.GetDir()
            #//strDest += (szNewName)?   szNewName : item.GetName();
            #//TOFIX
            if not (strDest [-1] == '\\' or strDest [-1] == '/'):
                strDest += '/'

            if(NULL != szNewName):
                strDest += szNewName
            else:
                strDest += item.GetName()
            return self.CopyToLocal(item, strDest, nOffset)
        else:
            #//wxString strFullPath = m_strCurDir + item.GetName();
            #//TOFIX '/'
            strFullPath = self.m_strCurDir
            strFullPath += '/'
            strFullPath += item.GetName()

            if(szNewName):
                item.SetName(szNewName)

            return pVfsDest.CopyFromLocal(strFullPath, item, nOffset)

        return False

    #bool Vfs_Local::Execute(const char *szItem, bool bLocalDir)
    def Execute(self, szItem, bLocalDir = True):
        strPath = ""
        if bLocalDir:
            strPath = self.m_strCurDir
            strPath += '/'
        strPath += szItem

        #//TOFIX get command string for selected files
        return ExecuteFile (szItem, None, self.m_strCurDir, 0)
        #//::wxShell(strPath);
        #//return true;

    #bool Vfs_Local::CopyToLocal(VfsItem &item, const char *szLocalPath, long nOffset)
    def CopyToLocal(self, item, szLocalPath, nOffset):
        #//TOFIX
        #return self.FileCopy(self.m_strCurDir + '/' + item.GetName(), szLocalPath, self.m_pProgress, nOffset)
        #TOMAKEBETTER: make better
        strCurDir = self.m_strCurDir
        if not (self.m_strCurDir [-1] == '\\' or self.m_strCurDir [-1] == '/'):
            strCurDir += '/'
        #print strCurDir + item.GetName(), szLocalPath, self.m_pProgress
        return self.FileCopy(strCurDir + item.GetName(), szLocalPath, self.m_pProgress, nOffset)


    #bool Vfs_Local::CopyFromLocal(const char *szLocalPath, VfsItem &item, long nOffset)
    def CopyFromLocal(self, szLocalPath, item, nOffset):
        return self.FileCopy(szLocalPath, self.m_strCurDir + '/' + item.GetName(), self.m_pProgress, nOffset)

    #//TOFIX move somwhere else ?
    #//TOFIX use wxFile with 64 bit support when available?
    #bool FileCopy(const char *szSrc, const char *szDest, OpState *pProgress, int nOffset)
    def FileCopy(self, szSrc, szDest, pProgress, nOffset):
        bRes = false

        #ifdef __WXMSW__
        #szSrc = 'c:\\test.DAT'
        #szDest = 'c:\\neu\\AVG6DB_F.DAT'
        #print szSrc, szDest

        ### check if the source file really can be opened

        #TOMAKEBETTER: ask, if file exists or catch 'file not exist exception'
        bopend = True
        try:
            nSrcFile = open(szSrc, 'rb', 0)
        except:
            bopend = False
        #nSrcFile = _open(szSrc, _O_BINARY|_O_RDONLY, 0);
        #if(nSrcFile > -1):
        if bopend:
            #//if the destination file exists and is read-only

            ### check if the destination file already exists
            bopend = True
            try:
                nSrcFile = open(szDest, 'rb', 0)
            except:
                bopend = False
            if bopend:
            #if(0 == access(szDest, 00))
                dwAttr = win32file.GetFileAttributes (szDest)
                if(-1 != dwAttr and dwAttr & win32con.FILE_ATTRIBUTE_READONLY):
                    #//remove read only flag
                    dwAttr &= ~(win32con.FILE_ATTRIBUTE_READONLY)
                    win32file.SetFileAttributes(szDest, dwAttr)

            #//TOFIX _O_RDWR instead of _O_RDONLY for rollback segment checking
            #nDstFile = open(szDest, _O_BINARY|_O_CREAT|_O_WRONLY, _S_IREAD);
            nDstFile = open(szDest, 'wb')

            ### check if the nDstFile can be created

            #if(nDstFile > -1)
            #
            if(nDstFile != -1):
                #char szBuffer[10000];
                nRead = 0

                #struct _stati64 st;
                #_stati64(szSrc, &st);
                #uSrcSize = 0
                uSrcSize = os.path.getsize(szSrc)
                #wxInt64 uSrcSize = st.st_size;  //__int64
                #_stati64(szDest, &st);
                #wxInt64 uDstSize = st.st_size;
                uDstSize = 0

                #TOMAKEBETTER: find better solution
                #//TOFIX implement overlapping resuming for content checking
                #if(nOffset>0 && uSrcSize > uDstSize){
                if nOffset > 0 and uSrcSize > uDstSize:
                    nSrcFile.seek(nSrcFile, uDstSize, 0) #SEEK_SET)
                    nStartProgress = uDstSize
                nStartProgress = 0

                if(NULL != pProgress):
                    pProgress.InitCurrentFiles(szSrc, szDest)
                    pProgress.InitCurrentProgress(nStartProgress, uSrcSize)

                #i = 0
                while nRead < uSrcSize:
                    #print nRead, uSrcSize
                    szBuffer = nSrcFile.read (1000000)
                    #szBuffer = os.read (1000000)
                    nReaded = len (szBuffer)
                    #i += 1
                    if szBuffer == '':
                        break
                    if (NULL != pProgress):
                        if pProgress.IsAborted():
                            break
                        nRead += nReaded
                        #sleeptime = (random() * 2) + 0.5
                        #time.sleep(sleeptime/4)

                        pProgress.StepPos(nReaded)
                    #nDstFile.write (szBuffer, 10000)
                    #time.sleep(0.1)
                    nDstFile.write (szBuffer)

                #//TOFIX what if user wants to keep partialy copied file ? (option?)
                if(pProgress and pProgress.IsAborted()):
                    #//TOFIX reuse code common with Delete() -> version without Dlgs
                    nDstFile.close()
                    dwAttr = win32file.GetFileAttributes(szDest);
                    if(-1 != dwAttr and dwAttr & win32con.FILE_ATTRIBUTE_READONLY):
                        #//remove read-only style (so delete API won't fail)
                        dwAttr &= ~(win32con.FILE_ATTRIBUTE_READONLY)
                        win32file.SetFileAttributes(szDest, dwAttr)
                    #//VERIFY
                    os.remove(szDest)
                else:
                    #//copy file attributes
                    dwAttrib = win32file.GetFileAttributes(szSrc)
                    #if(-1 != dwAttrib):
                    #    win32file.SetFileAttributes(szDest, dwAttrib)

                    #//before closing the file copy file dates
                    #FILETIME ftCreated, ftAccessed, ftModified;
                    #HANDLE hSrc = (HANDLE)_get_osfhandle(nSrcFile);
                    #HANDLE hDst = (HANDLE)_get_osfhandle(nDstFile);

                    nDstFile.close()
                    nSrcFile.close()
                    #print 'SetFileTime'
                    #hSrc = win32file.CreateFile(nSrcFile,  win32file.GENERIC_READ, 0, None, win32file.OPEN_EXISTING, 0, 0)
                    hSrc = win32file.CreateFile(szSrc, win32file.GENERIC_READ, 0, None, win32file.OPEN_EXISTING, 0, 0)
                    #TOMAKEBETTER: better solution

                    try:
                        hDst = win32file.CreateFile(szDest,  win32file.GENERIC_WRITE, 0, None, win32file.OPEN_EXISTING, 0, 0)
                        filetime = win32file.GetFileTime(hSrc)
                        if (filetime):
                            win32file.SetFileTime(hDst, filetime[1], filetime[2], filetime[3])
                        hDst.Close()
                    except:
                        wxMessageBox(_("cannot access to destination file!"))
                    #erst hier, sonst kam bei filetime von read only 'cannot access to destination file!'
                    if(-1 != dwAttrib):
                        win32file.SetFileAttributes(szDest, dwAttrib)

                    #[1, <PyTime:05.08.2003 21:12:20>, <PyTime:09.01.2004 23:00:00>, <PyTime:10.01.2004 18:28:40>]
                    hSrc.Close()
                    #if(GetFileTime(hSrc, &ftCreated, &ftAccessed, &ftModified))
                    #    SetFileTime(hDst, &ftCreated, &ftAccessed, &ftModified);

                bRes = True

            nSrcFile.close()
        #else
        '''
        //TOFIX add missing code
        int nSrcFile = open(szSrc, O_RDONLY, 0);
        if(nSrcFile > -1)
        {
            //if the destination file exists and is read-only
            if(0 == access(szDest, 00)){
            }

            //TOFIX O_RDWR instead of O_RDONLY for rollback segment checking
            int nDstFile = open(szDest, O_CREAT|O_WRONLY|O_LARGEFILE, S_IREAD);
            if(nDstFile > -1)
            {
                char szBuffer[10000];
                wxUint32 nRead;

            struct stat st;
            stat(szSrc, &st);
            wxInt64 uSrcSize = st.st_size;  //__int64
            stat(szDest, &st);
            wxInt64 uDstSize = st.st_size;

            wxInt64 nStartProgress = 0;

            //TOFIX implement overlapping resuming for content checking
            if(nOffset>0 && uSrcSize > uDstSize){
                lseek64(nSrcFile, uDstSize, SEEK_SET);
                nStartProgress = uDstSize;
            }

            if(NULL != pProgress){
                    pProgress->InitCurrentFiles(szSrc, szDest);
                    pProgress->InitCurrentProgress(nStartProgress, uSrcSize);
                }

                while(0 != (nRead = read(nSrcFile, szBuffer, sizeof(szBuffer))))
                {
                    if(NULL != pProgress){
                        if(pProgress->IsAborted())
                            break;
                        pProgress->StepPos(nRead);
                    }

                    write(nDstFile, szBuffer, nRead);
                }

                //TOFIX what if user wants this !!! (option)
                if(pProgress && pProgress->IsAborted())
                {
                    //delete file - including readonly file
                    //TOFIX reuse code common with Delete() -> version without Dlgs
                    ::wxRemoveFile(szDest);
                }
                else
                {
                    //copy file attributes
                }

                close(nDstFile);
                bRes = true;
            }

            close(nSrcFile);
        }

        #endif
        '''
        return bRes

    def GetDriveFreeSpace(self):
        return win32api.GetDiskFreeSpace()

def OpDeleteFileDlgThreadsafe(szPath):
    #print "OpDeleteFileDlgThreadsafe"
    event = wxCommandEvent ()
    event.SetEventType (wxEVT_COMMAND_BUTTON_CLICKED)
    event.SetId (20003)

    g_strTitle = szPath

    pFrm = wxGetApp().GetFrame()
    if(pFrm):
        wxPostEvent(pFrm, event)

    wxYield()
    #//wait for GUI to end with owerwrite dialog
    #g_objGUISyncSemaphore.Wait();

    return g_nGuiResult

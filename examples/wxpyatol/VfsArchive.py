#print "import vfsarchive"
from wxPython.wx import *
from Vfs import *
from VfsSelection import *
from PathName import *
#from MainFrame import *

class Vfs_Archive(Vfs):
    def __init__(self):
        #friend class VfsManager;

        #// mount / unmount new virtual file system
        #virtual bool Open();

        #// directory change
        #//for display purposes
        #virtual wxString GetPathTitle();

        #// operations
        #virtual bool Copy(VfsItem &item, const char *szNewName, Vfs *pVfsDest, wxInt64 nOffset = 0);
        #virtual bool Execute(const char *szItem, bool bLocalDir = true);

        #virtual bool CopyToLocal(VfsItem &item, const char *szLocalPath, long nOffset = 0);
        #virtual bool CopyFromLocal(const char *szLocalPath, VfsItem &item, long nOffset = 0);


        #ArchiverPlugin *m_pPlugin;
        #wxString        m_strArchiveFile;
        #wxString        m_strTitle;

        self.m_pPlugin = 0
        self.m_hArchive = 0
        self.m_bReadOnly = False
        self.m_bReadFile = False
        #//after archive closes
        self.m_bDeleteFile = False
        self.m_lstTree = VfsSelection ()
        self.m_nType = VFS_ARCHIVE
        self.m_pProgress = 0

        #extern PluginManager g_PlugManager;

        #int ProgressProc(const char *FileName,int Size, int dwUser);



    def Open(self):
        #//ASSERT(0 == m_hArchive);
        #//ASSERT(NULL != m_pPlugin);

        if 0 != self.m_pPlugin:
            #//check if read only
            '''
            /*
                    int dwAttr = GetFileAttributes(m_strArchiveFile);
                    if( 0xFFFFFFFF != dwAttr &&
                        (dwAttr & FILE_ATTRIBUTE_READONLY))
                        m_bReadOnly = TRUE;
                    else
                        m_bReadOnly = FALSE;
            */
            '''
            #//tOpenArchiveData data;
            #//strcpy(data.ArcName, m_strArchiveFile); //TOFIX?
            #//TOFIX readonly as param
            #self.m_hArchive = self.m_pPlugin.m_pfnOpenArchive(m_strArchiveFile)
            self.m_hArchive = self.m_pPlugin.OpenArchive(self.m_strArchiveFile)
            #//ASSERT(m_hArchive > 0);
            return self.m_hArchive > 0

        return False

    def Close(self):
        #//ASSERT(NULL != m_pPlugin);

        if 0 != self.m_pPlugin:
            #self.m_pPlugin.m_pfnCloseArchive(m_hArchive)
            self.m_pPlugin.CloseArchive(m_hArchive)
            self.m_hArchive = 0

            #//TOFIX clean other data
            self.m_lstTree.Clear();

        #//for "archive in archive" delete file from temp dir after disconnect
        #//TOFIX
        #//if(m_bDeleteFile)
        #//  VERIFY(::DeleteFile(m_strArchiveFile));
        return False

    def SetDir(self, szPath):
        #//TOFIX ? check dir
        self.m_strCurDir = szPath
        path_instance = PathName ()
        path_instance.EnsureTerminated(m_strCurDir, '/')
        #PathName::EnsureTerminated(m_strCurDir, '/');
        return True

    def Rename(self, szFrom, szTo):
        #//not supported
        return False

    #//NOTE: single file / empty dir delete
    #bool Vfs_Archive::Delete(const char *szItem, int &nOpSettings)
    def Delete (self, szItem, nOpSettings):
        #//ASSERT(NULL != m_pPlugin);
        #//ASSERT(0 != m_hArchive);

        #//check if archiver supports operation
        if not self.CheckArchiverCaps (PK_CAPS_DELETE):
            return False

        if self.m_bReadOnly:
            wxMessageBox(_("Read-only archive!"))
            return False

        if 0 != self.m_pPlugin:
            #//TOFIX stripPrefix
            path_instance = PathName ()
            path_instance.EnsureTerminated(m_strCurDir, '/')
            #PathName::EnsureTerminated(m_strCurDir, '/');
            strPath = self.m_strCurDir + szItem

            #//TOFIX ensure not prefixed with \ or / -> to detect exit from archive
            if len (strPath.Length) > 0:
                if strPath[0] == '\\' or strPath[0] == '/':
                    strPath= strPath[strPath.Length()-1:]
            #//TOFIX
            strPath = strPath.replace("/","\\");

            #//init plugin progress callback
            if 0 != self.m_pPlugin.m_pfnSetProcessDataProc:
                #self.m_pPlugin.m_pfnSetProcessDataProc (self.m_hArchive, ProgressProc, self)
                self.m_pPlugin.SetProcessDataProc (self.m_hArchive, ProgressProc, self)

            #//init progress range indicator
            #//ASSERT(NULL != m_pProgress);
            #//NOTE do this before initsingle
            #//m_pProgress->InitFileNames(strPath, NULL);
            #//m_pProgress->InitSingle(1);

            bRes = False
            if 0 != self.m_pPlugin.m_pfnDeleteEntry:
                #bRes = self.m_pPlugin.m_pfnDeleteEntry (self.m_hArchive, strPath)
                bRes = self.m_pPlugin.DeleteEntry (self.m_hArchive, strPath)
                #//if(!bRes)
                #//  TRACE("ERROR: failed to delete %s from archive %s\n", strPath, m_strArchiveFile);

            #//m_pProgress->SingleSetPos(1);
            #//operation changed archive - read tree again
            self.m_bReadFile = True
            return bRes

        return False

    #bool Vfs_Archive::MkDir(const char *szDir)
    def MkDir(self, szDir):
        if not CheckArchiverCaps (PK_CAPS_MODIFY):
            return False

        if self.m_bReadOnly:
            wxMessageBox(_("Read-only archive!"))
            return False

        #//ASSERT(NULL != m_pPlugin);
        #//ASSERT(0 != m_hArchive);

        if 0 != self.m_pPlugin:
            strPath = self.m_strCurDir
            path_instance = PathName ()
            path_instance.EnsureTerminated(strPath, '/')
            #PathName::EnsureTerminated(strPath, '/');
            strPath += szDir

            #//force creating directory in archive
            bRes = False
            if self.m_pPlugin.m_pfnMakeDir:
                #bRes = self.m_pPlugin.m_pfnMakeDir(self.m_hArchive, strPath)
                bRes = self.m_pPlugin.MakeDir(self.m_hArchive, strPath)

            #//operation changed archive - read tree again
            m_bReadFile = True
            return bRes

        return False

    #bool Vfs_Archive::ListDir(VfsListing &list, bool &bAbort)
    def ListDir(self, list, bAbort):
        #//TOFIX
        strRootUnix = self.m_strCurDir
        strRootDos = self.m_strCurDir
        strRootUnix = strRootUnix.replace("\\", "/")
        strRootDos = strRootDos.replace("/", "\\")

        list.Clear()

        if self.m_bReadFile or self.m_lstTree == "":
            self.BuildTree()

        #//default entry -> TOFIX posebna funkcija za init default entry?
        info = VfsItem ()
        info.m_nAttrib = ATTR_DIR
        info.SetName("..")
        list.Insert(info)

        #//TOFIX support for apsolute zip entries like "C:\aaa\bb.txt"
        pListLevel =  ""
        pListLevel = self.m_lstTree.find(m_strCurDir)
        #//ASSERT(NULL != pListLevel);

        if -1 != pListLevel:
            for i in range (len(pListLevel)):
                #//TRACE("Testing zip entry: %s\n", info.m_strName);
                info = pListLevel[i]
                list.Insert(info)

        #//TOFIX? keep archive closed most of the time / not needed CloseArchive()
        #//TOFIX
        return True

    #def_Archive::InitArchiver(const char * szFileName)
    def InitArchiver (self, szFileName):
        #//store file name for later opening
        self.m_strArchiveFile = szFileName

        #//find plugin using extension
        strExt = ""
        path_instance = PathName ()
        strExt = path_instance.GetExt (szFileName)
        #strExt = PathName::GetExt(szFileName);
        strExt = strExt.lower()

        self.m_pPlugin = wxGetApp().GetFrame().m_PluginManager.FindArchiver(strExt)

        return self.m_pPlugin != 0

    def BuildTree(self):
        self.m_lstTree.Clear();

        #//TOFIX podrska za gradnju stabla i sl kao u prvotnom zipu
        #//ASSERT(NULL != m_pPlugin);
        if 0 != m_pPlugin:
            #self.m_pPlugin.m_pfnInitEntryEnum(m_hArchive)
            self.m_pPlugin.InitEntryEnum(m_hArchive)

            info = tArchiveEntry ()
            fileInf = VfsItem ()

            i = 0

            while 1:
                #//init info
                #if not self.m_pPlugin.m_pfnGetNextEntry(self.m_hArchive, info):

                info = self.m_pPlugin.GetNextEntry(self.m_hArchive)
                if info == -1:
                    break

                #//TRACE("Archive entry: %s\n", info.szPath);

                #//NOTE: it is extremely important that also MatchPaths() support this!!!! (so the file can be unpacked)
                #//FIX for relative paths like "./dir/file"
                #//FIX for strange entries found (like "././@LongLink")
                pszEntry = info.szPath
                while pszEntry.find ("./") != -1:
                    pszEntry = pszEntry[2:]

                #//
                pEntry = self.m_lstTree.Insert(pszEntry)
                if 0 != pEntry:
                    path_instance = PathName ()
                    pEntry.m_strName = path_instance.GetBaseName(pszEntry)
                    pEntry.m_nSize   = info.nUnpSize;
                    pEntry.m_nAttrib = info.dwAttribs;
                    pEntry.m_nLastModDate = info.tmModified;

                    #//NOTE: FIX some "bad" archives have not directory flag set for some directories
                    if (('\\' == info.szPath[len(info.szPath)-1]  or
                        '/'  == info.szPath[len(info.szPath)-1]) and
                        not info.bDir):
                            pEntry.m_nAttrib = ATTR_DIR

                i += 1

        #//TOFIX fix dates for "..", dirs, ...

        #//done reading the tree
        self.m_bReadFile = FAalse

    #defool Vfs_Archive::Copy(VfsItem &item, const char *szNewName, Vfs *pVfsDest, wxInt64 nOffset)
    def Copy (self, item, szNewName, pVfsDest, nOffset):
        if pVfsDest.GetType() == VFS_LOCAL or pVfsDest.GetType() == VFS_NET:
            strDest = pVfsDest.GetDir()
            strDest += '/'
            strDest += szNewName
            return CopyToLocal(item, strDest)
        else:
            #//create temporary path name
            path_instance = PathName ()
            strTmpPath = path_instance.Path_TempDirectory()
            path_instance.EnsureTerminated(strTmpPath, '/')
            #PathName::EnsureTerminated(strTmpPath, '/');
            strTmpPath += item.GetName()
            #strTmpPath = wxFileName::CreateTempFileName(strTmpPath);
            ftmp = open (strTmpPath, 'wb')
            ftmp.write("")
            ftmp.close()

            #//TOFIX handle double progress (unpack + copy/pack)???
            if (self.CopyToLocal(item, strTmpPath) and pVfsDest.CopyFromLocal(strTmpPath, item)):
                return True
        return False

    #bool Vfs_Archive::CopyFromLocal(const char *szLocalPath, VfsItem &item, long nOffset)
    def CopyFromLocal (self, szLocalPath, item, nOffset):
        if self.CheckArchiverCaps(PK_CAPS_MODIFY):
            return False

        if self.m_bReadOnly:
            wxMessageBox(_("Read-only archive!"))
            return false

        #//ASSERT(NULL != m_pPlugin);
        #//ASSERT(0 != m_hArchive);

        if 0 != self.m_pPlugin:
            #//init plugin progress callback
            if 0 != self.m_pPlugin.m_pfnSetProcessDataProc:
                #self.m_pPlugin.m_pfnSetProcessDataProc(m_hArchive, ProgressProc, self)
                self.m_pPlugin.SetProcessDataProc(m_hArchive, ProgressProc, self)

            #//NOTE do this before initsingle
            path_instance = PathName ()
            path_instance.EnsureTerminated(m_strCurDir, '/')
            #PathName::EnsureTerminated(m_strCurDir, '/');

            if 0 != m_pProgress:
                self.m_pProgress.InitCurrentFiles(szLocalPath, m_strCurDir + item.GetName())
                #//init progress range indicator
                self.m_pProgress.InitCurrentProgress(0, item.m_nSize)

            bRes = False

            #//PackFile(int dwArchID, const char *szFile, const char *SubPath, const char*szDestName);
            if 0 != self.m_pPlugin.m_pfnPackFile:
                #bRes = self.m_pPlugin.m_pfnPackFile(self.m_hArchive, szLocalPath, self.m_strCurDir, item.GetName())
                bRes = self.m_pPlugin.PackFile(self.m_hArchive, szLocalPath, self.m_strCurDir, item.GetName())

            #//operation changed archive - read tree again
            self.m_bReadFile = True
            return bRes

        return False

    #def CopyToLocal(VfsItem &item, const char *szLocalPath, long nOffset)
    def CopyToLocal (self, item, szLocalPath, nOffset):
        #//ASSERT(NULL != m_pPlugin);
        #//ASSERT(0 != m_hArchive);

        if 0 != self.m_pPlugin:
            #//TOFIX
            path_instance = PathName ()
            #PathName::EnsureTerminated(m_strCurDir, '/')
            path_instance.EnsureTerminated(self.m_strCurDir, '/')
            strPath = self.m_strCurDir + item.GetName()
            #//TOFIX
            strPath = strPath.replace("/","\\");

            #//init plugin progress callback
            if 0 != self.m_pPlugin.m_pfnSetProcessDataProc:
                #self.m_pPlugin.m_pfnSetProcessDataProc(self.m_hArchive, ProgressProc, self)
                self.m_pPlugin.SetProcessDataProc(self.m_hArchive, ProgressProc, self)

            #//init progress range indicator
            if 0 != self.m_pProgress:
                #//NOTE do this before initsingle
                self.m_pProgress.InitCurrentFiles(strPath, szLocalPath)
                #/*not good for recursion -> GetItemSize(szItem)*/
                self.m_pProgress.InitCurrentProgress(0, item.m_nSize)

            #//UnpackFile(int dwArchID, const char *szEntry, const char *szDest);
            if 0 != self.m_pPlugin.m_pfnUnpackFile:
                #return self.m_pPlugin.m_pfnUnpackFile(self.m_hArchive, strPath, szLocalPath)
                return self.m_pPlugin.UnpackFile(self.m_hArchive, strPath, szLocalPath)

        return False

    #def ProgressProc(const char *FileName,int Size, int dwUser)
    def ProgressProc (self, FileName, Size, dwUser):
        pArchive = dwUser
        #//ASSERT(NULL != pArchive);

        if 0 != pArchive and 0 != pArchive.m_pProgress:
            pArchive.m_pProgress.SetPos(Size)
        return 1

    def GetDriveFreeSpace(self):
        #//TOFIX
        return 100000
        #//return RealGetDiskFreeSpace(m_strArchiveFile.Left(3));

    #defVfs_Archive::CheckArchiverCaps(int dwCapsRequested)
    def CheckArchiverCaps (self, dwCapsRequested):
        #//check if archiver supports operation
        if 0 != self.m_pPlugin and 0 != self.m_pPlugin.m_pfnGetArchiverCaps:
            path_instance = PathName ()
            #strExt = PathName::GetExt(m_strArchiveFile);
            strExt = path_instance.GetExt (self.m_strArchiveFile)
            dwCapsArchiver = self.m_pPlugin.GetArchiverCaps (strExt)
            if 0 == (dwCapsRequested & dwCapsArchiver):
                wxMessageBox(_("Archiver does not support this operation!"))
                return False

            return True
        return False
    '''
    /*
    bool Vfs_Archive::IsConnected()
    {
        return (m_hArchive != 0);
    }

    bool Vfs_Archive::RootDir()
    {
        m_strCurDir.Empty();
        return true;
    }

    //TOFIX move to VFS
    bool Vfs_Archive::UpDir()
    {
        CPath path(GetDir());

        //TOFIX add this to other types?
        if(path.GetPath().IsEmpty() || path.GetPath().GetLength() <= 1)
            return false;

        CString strNewPath = path.GetParentDirPath('/');
        if(strNewPath != GetDir())
        {
            SetDir(strNewPath); //path se postavlja samo ako se promijenio
            return true;
        }

        return false;
    }

    bool Vfs_Archive::ExecuteItem(const char *szFileName)
    {
    if(wxYES == wxMessageBox(_("Unpack to temp and execute this file?"), WX_YESNO))
        {
            CString strTemp  = CPath::Path_TempDirectory();
            CString strLocal = strTemp + szFileName;

            //currently disable operation progress
            CProgressInfo *pProgress = m_pProgress;
            m_pProgress = NULL;

            //unpack
            VfsItem item;
            item.m_strName = szFileName;
            item.CalculateOther();
            if(!CopyToLocal(item, strLocal, 0)){
                m_pProgress = pProgress;    //reenable progress
                AfxMessageBox(g_info.ML.tr(35,"Failed to unpack the file!"));
                return false;
            }

            m_pProgress = pProgress;    //reenable progress

            //execute
            CWaitCursor cur;

            HANDLE hProcess = NULL;
            bool bRes = SHELL::Execute(szFileName, NULL, strTemp, &hProcess);
            if(bRes)
            {
                //file started, now we are responsible to delete it after we are done
                g_objProcessList.AddFile(strLocal, hProcess);
            }
            else
            {
                //could not start unpacked file, so delete it
                ::DeleteFile(strLocal);
            }

            return bRes;
        }

        return false;
    }

    bool Vfs_Archive::ExecuteCmd(const char *szCmdLine)
    {
        wxMessageBox(g_info.ML.tr(54,"Not supported!"));
        return false;
    }

    //napravi title koji koristi sve pathove u lancu VFS-a
    wxString Vfs_Archive::GetPathTitle()
    {
        wxString strRes;

        //recursive
        if(NULL != m_pParentVFS)
            strRes = m_pParentVFS.GetPathTitle();

        //title is used when we want to mask archive file location
        //eg. archive inside archve unpacks inner archive into temp directory

        if(m_strTitle.IsEmpty())
        {
            CPath path(self.m_strArchiveFile);
            strRes += path.GetBaseName();
        }
        else
        {
            strRes += m_strTitle;
        }

        strRes += m_strCurDir;
        PathName::EnsureTerminated(strRes, '/');
        return strRes;
    }

    HICON Vfs_Archive::GetVFSIcon()
    {
        //FIX: with LoadIcon we get ugly results when icon being drawed on button
        //return LoadIcon(AfxGetInstanceHandle(), MAKEINTRESOURCE(IDI_ZIP_TMP));
        return (HICON)LoadImage(AfxGetInstanceHandle(), MAKEINTRESOURCE(IDI_ZIP_TMP), IMAGE_ICON, 16, 16, LR_DEFAULTCOLOR|LR_DEFAULTSIZE);
    }
    '''

    def IsRootDir(self):
        #ifdef __WXMSW__
        if len(self.m_strCurDir) <= 3:
           return True
        #else
        #    if(m_strCurDir.Len() < 2)
        #        return true;
        #endif

        return False

    def SetRootDir(self):
        #//TOFIX
        return True

    #def Execute(const char *szItem, bool bLocalDir)
    def Execute (self, szItem, bLocalDir):
        return False

    #//for display purposes
    def GetPathTitle(self):
        strTitle = ""
        #//custom title is used when we want to mask archive file location
        #//eg. archive inside archve unpacks inner archive into temp directory
        if self.m_strTitle == "":
            #TOMAKEBETTER: use static (unbound method)
            path_instance = PathName ()
            strTitle = path_instance.GetBaseName (self.m_strArchiveFile)
            #strTitle += PathName::GetBaseName(m_strArchiveFile);
        else:
            strTitle = self.m_strTitle

        strTitle += self.m_strCurDir
        return strTitle


#import win32api#, win32con, winerror, win32evtlog, string
#from ctypes import *
##import calldll
import struct
from Plugin_defs import *
from array import *
#//shared file
#import 'plugin_defs.h'
#include 'ArchiverPlugin.h'
#include 'wx/dynlib.h'
#include 'wx/msgdlg.h'
#include 'wx/string.h'
#include 'wx/dynlib.h'


class ArchiverPlugin:
    def __init__ (self):
        pass


    #/TOFIX separate file with interface description?

    #typedef unsigned int    (*tGetArchiverCaps)(const char *szExt);
    #tested, ok
    def GetArchiverCaps (self, strExt):
        #m_pfnGetArchiverCaps ist gesetzt
        if self.m_pfnGetArchiverCaps:
            #call_foreign_function (string: 4 erweitert auf 5), 5 passt, 6 erweitert auf 7
            #adr_buf = calldll.membuf(len (strExt))
            bufIn = array('c', strExt + '\0')
            #adr_buf.write(strExt)
            #print adr_buf.read()
            #print 'adr:', adr_buf
            #i = calldll.call_foreign_function(self.m_pfnGetArchiverCaps,'l', 'l', (adr_buf.address(),))
            i = calldll.call_foreign_function(self.m_pfnGetArchiverCaps,'w', 'l', (bufIn,))
            #print 'GetArchiverCaps:', i
            return i
        else:
            #print 'GetArchiverCaps not found'
            return -1

    #typedef const char* (*tGetExtensions)();
    #tested, ok
    def GetExtensions (self):
        if self.m_pfnGetExtensions:
            i = calldll.call_foreign_function(self.m_pfnGetExtensions,'', 's', ())
            #print 'GetExtensions:', i
            return i
        else:
            #print 'GetExtensions not found', i
            return ''
    '''
    #for testing purpose
    #tested, ok; without pInfo
    #typedef int (*tGetNextEntry)(int dwArchID, tArchiveEntry *pInfo);
    def GetNextEntry (self, dwArchID, pInfo):
        if self.m_pfnGetNextEntry:
            dwArchID_buf = calldll.membuf(16)
            dwArchID_buf.write(str(dwArchID))
            #print 'read:', dwArchID_buf.read()
            #i = calldll.call_foreign_function(self.m_pfnGetNextEntry,'', 'ls', (dwArchID_buf.adress(), pInfo))
            #test
            #i = calldll.call_foreign_function(self.m_pfnGetNextEntry,'l', '', (dwArchID_buf.address(), ))
            #erstes input, zweites output
            i = calldll.call_foreign_function(self.m_pfnGetNextEntry,'l', 'l', (dwArchID,))
            #print 'GetNextEntry:', i
            return i
        else:
            #print 'GetNextEntry not found'
            return -1
    '''

    #typedef int (*tGetNextEntry)(int dwArchID, tArchiveEntry *pInfo);
    #tested, ok
    def GetNextEntry (self, dwArchID, pInfo):
        if self.m_pfnGetNextEntry:
            #260 + 4*6
            pInfo_buf = calldll.membuf(284)
            #pInfo_buf.write('aa')
            #pInfo_buf.write('bb')
            #print pInfo.szPath
            #pInfo_buf.write (struct.pack('<260s', pInfo.szPath))
            pInfo_buf.write (struct.pack('<260siiiiii', pInfo.szPath, pInfo.nPackSize, pInfo.nUnpSize, pInfo.bDir,
                pInfo.dwAttribs,  pInfo.dwFileCRC,  pInfo.tmModified))

            i = calldll.call_foreign_function(self.m_pfnGetNextEntry,'ll', 'l', (dwArchID, pInfo_buf.address()))

            #TODO: struktur unpack

            ret_tArchiveEntry = tArchiveEntry ()

            ResultTuple = struct.unpack('<260siiiiii', i);
            ret_tArchiveEntry.szPath      = ResultTuple [0]
            ret_tArchiveEntry.szPath      = ResultTuple [1]
            ret_tArchiveEntry.nPackSize   = ResultTuple [2]
            ret_tArchiveEntry.nUnpSize    = ResultTuple [3]
            ret_tArchiveEntry.bDir        = ResultTuple [4]
            ret_tArchiveEntry.dwAttribs   = ResultTuple [5]
            ret_tArchiveEntry.dwFileCRC   = ResultTuple [6]
            ret_tArchiveEntry.tmModified  = ResultTuple [7]

            #print 'GetNextEntry:', i
            return ret_tArchiveEntry
        else:
            #print 'GetNextEntry not found'
            return -1

    #typedef void (*tProcessMultiple)(int dwArchID, int nOperation);
    #tested, ok
    def ProcessMultiple (self, dwArchID, nOperation):
        if self.m_pfnProcessMultiple:
            calldll.call_foreign_function(self.m_pfnProcessMultiple, 'll', '', (dwArchID, nOperation))
            #print 'ProcessMultiple'
        else:
            pass
            #print 'ProcessMultiple not found'


    #typedef bool (*tPackFile)(int dwArchID, const char *szFile, const char *SubPath, const char*szDestName);
    #self.PackFile (1, 'file1', 'path1', 'destname'):
    #tested, ok
    def PackFile (self, dwArchID, szFile, SubPath, szDestName):
        if self.m_pfnPackFile:

            szFile_buf = array('c', szFile + '\0')
            SubPath_buf = array('c', SubPath + '\0')
            szDestName_buf = array('c', szDestName + '\0')

            #szFile_buf = calldll.membuf(len (szFile))
            #szFile_buf.write(szFile)
            #print szFile, len (szFile)
            #print szFile_buf.read()
            #SubPath_buf = calldll.membuf(len (SubPath))
            #SubPath_buf.write(SubPath)
            #szDestName_buf = calldll.membuf(len (szDestName))
            #szDestName_buf.write(szDestName)
            i = calldll.call_foreign_function(self.m_pfnPackFile,'lwww', 'l',
                #(dwArchID, szFile_buf.address(), SubPath_buf.address(), szDestName_buf.address()))
                #(dwArchID, szFile_buf.address(), szFile_buf.address(), szFile_buf.address()))
                #(dwArchID,bufIn,bufIn,bufIn))
                (dwArchID, szFile_buf, SubPath_buf, szDestName_buf))
            if i:
                i = True
            else:
                i = False
            #print 'PackFile:', i
            return i
        else:
            #print 'PackFile not found'
            return False

    #typedef bool (*tUnpackFile)(int dwArchID, const char *szEntry, const char *szDest);
    #tested, ok
    def UnpackFile (self, dwArchID, szEntry, szDest):
        if self.m_pfnUnpackFile:
            szEntry_buf = array('c', szEntry + '\0')
            szDest_buf = array('c', szDest + '\0')
            i = calldll.call_foreign_function(self.m_pfnUnpackFile,'lww', 'l',
                (dwArchID, szEntry_buf, szDest_buf))
            if i:
                i = True
            else:
                i = False
            #print 'UnpackFile:', i
            return i
        else:
            #print 'UnpackFile not found'
            return False


    #typedef bool (*tDeleteEntry)(int dwArchID, const char *szEntry);
    #tested, ok
    def DeleteEntry (self, dwArchID, szEntry):
        if self.m_pfnDeleteEntry:
            szEntry_buf = array('c', szEntry + '\0')
            i = calldll.call_foreign_function(self.m_pfnDeleteEntry,'lw', 'l', (dwArchID, szEntry_buf))
            if i:
                i = True
            else:
                i = False
            #print 'DeleteEntry', i
            return i
        else:
            #print 'DeleteEntry not found'
            return False

    #def typedef void (*tEndProcessMulti)(int dwArchID);
    #tested, ok
    def EndProcessMulti (self, dwArchID):
        if self.m_pfnEndProcessMulti:
            calldll.call_foreign_function(self.m_pfnEndProcessMulti,'l', '', (dwArchID,))
            #print 'EndProcessMulti'
        else:
            pass
            #print 'EndProcessMulti not found'

    #typedef void (*tInitEntryEnum)(int dwArchID);
    #tested, ok
    def InitEntryEnum (self, dwArchID):
        if self.m_pfnInitEntryEnum:
            calldll.call_foreign_function(self.m_pfnInitEntryEnum,'l', '', (dwArchID,))
            #print 'InitEntryEnum'
        else:
            pass
            #print 'InitEntryEnum not found'

    #typedef void (*tConfigurationDlg)(long hWndParent, long hDllInstance);
    #tested, ok
    def ConfigurationDlg (self, hWndParent, hDllInstance):
        if self.m_pfnConfigurationDlg:
            calldll.call_foreign_function(self.m_pfnConfigurationDlg, 'll', '', (hWndParent, hDllInstance))
            #print 'ConfigurationDlg'
        else:
            pass
            #print 'ConfigurationDlg not found'

    #typedef void (*tSetChangeVolProc)(int dwArchID, tChangeVolProc pChangeVolProc1);
    #tested, ok
    def SetChangeVolProc (self, dwArchID, pChangeVolProc1):
        #TODO?
        if self.m_pfnSetChangeVolProc:
            calldll.call_foreign_function(self.m_pfnSetChangeVolProc, 'll', '', (dwArchID, pChangeVolProc1))
            #print 'SetChangeVolProc'
        else:
            pass
            #print 'SetChangeVolProc not found'

    #typedef void *tSetProcessDataProc)(int dwArchID, tProcessDataProc pProcessDataProc, unsigned int dwUser);
    #tested, ok
    def SetProcessDataProc (self, dwArchID, pProcessDataProc, dwUser):
        if self.m_pfnSetProcessDataProc:
            calldll.call_foreign_function(self.m_pfnSetProcessDataProc, 'lll', '', (dwArchID, pProcessDataProc, dwUser))
            #print 'SetProcessDataProc'
        else:
            pass
            #print 'SetProcessDataProc not found'

    #typedef void (*tSetPasswordProc)(tPasswordProc pPwdProc, unsigned int dwUser);
    #tested, ok
    def SetPasswordProc (self, pPwdProc, dwUser):
        #self.m_pfnSetPasswordProc
        #self.SetPasswordProc(PasswordProc, 0)
        if self.m_pfnSetPasswordProc:
            calldll.call_foreign_function(self.m_pfnSetPasswordProc, 'll', '', (pPwdProc, dwUser))
            #print 'SetPasswordProc'
        else:
            #print 'SetPasswordProc not found'
            pass

    #typedef bool (*tMakeDir)(int dwArchID, const char *szDir);
    #tested, ok
    def MakeDir (self, dwArchID, szDir):
        if self.m_pfnMakeDir:
            szDir_buf = array('c', szDir + '\0')
            i = calldll.call_foreign_function(self.m_pfnDeleteEntry,'lw', 'l', (dwArchID, szDir_buf))
            if i:
                i = True
            else:
                i = False
            #print 'MakeDir:', i
            return i
        else:
            #print 'MakeDir not found'
            return False

    #// Ask to swap disk for multi-volume archive
    #typedef int (*tChangeVolProc)(char *ArcName, int Mode);
    #tested, ok
    def ChangeVolProc (self, ArcName, Mode):
        if self.m_pfnChangeVolProc:
            ArcName_buf = array('c', ArcName + '\0')
            i = calldll.call_foreign_function(self.m_pfnDeleteEntry,'wl', 'l', (ArcName_buf, Mode))
            #print 'ChangeVolProc', i
            return i
        else:
            #print 'ChangeVolProc not found'
            return -1

    # // Notify that data is processed - used for progress dialog
    #typedef int (*tProcessDataProc)(const char *FileName, int Size, int dwUser);
    #tested, ok
    def ProcessDataProc (self, FileName, Size, dwUser):
        if self.m_pfnProcessDataProc:
            FileName_buf = array('c', FileName + '\0')
            i = calldll.call_foreign_function(self.m_pfnProcessDataProc,'wll', 'l', (FileName, Size, dwUser))
            #print 'ProcessDataProc:', i
            return i
        else:
            #print 'ProcessDataProc not found'
            return -1

    #// ask password callback
    #typedef int (*tPasswordProc)(char *szPwdBuf, int Size, int dwUser);
    #tested, ok
    def PasswordProc (self, szPwdBuf, Size, dwUser):
        if self.m_pfnPasswordProc:
            szPwdBuf_buf = array('c', szPwdBuf + '\0')
            i = calldll.call_foreign_function(self.m_pfnPasswordProc, 'wll', 'l', (szPwdBuf_buf, Size, dwUser))
            #print 'PasswordProc:', i
            return i
        else:
            #print 'PasswordProc not found'
            return - 1

    #typedef int (*tOpenArchive)(const char *);
    #tested, ok
    def OpenArchive (self, szArhive):
        if self.m_pfnOpenArchive:
            szArhive_buf = array('c', szArhive + '\0')
            i = calldll.call_foreign_function(self.m_pfnOpenArchive,'w', 'l', (szArhive_buf,))
            #print 'OpenArchive:', i
            return i
        else:
            #print 'OpenArchive not found'
            return -1

    #typedef bool (*tCloseArchive)(int dwArchID);
    #tested, ok
    def CloseArchive (self, dwArchID):
        if self.m_pfnCloseArchive:
            i = calldll.call_foreign_function(self.m_pfnConfigurationDlg, 'l', 'l', (dwArchID, ))
            if i:
                i = True
            else:
                i = False
            #print 'CloseArchive:', i
            return i
        else:
            #print 'CloseArchive not found'
            return False

    #bool ArchiverPlugin::Load(const char *szFile)
    def Load (self, szFile):
         # DLL-interface
        self.m_dllHandle = calldll.load_library(szFile)
        #print self.m_dllHandle

        #import array
        #formstring = array.array('c','baud=9600 parity=N data=8 stop=1\0')
        #formstr_addr, formstr_len = formstring.buffer_info()
        #print formstring, '2', formstr_addr, formstr_len, '4', formstring.buffer_info()

        #adr_buf = calldll.membuf(4)
        #i = calldll.call_foreign_function(address,'l', 'l', (adr_buf.address(),))#, 'w', 'i', (buf,))
        #i = calldll.call_foreign_function(address,'', 's', ())#, 'w', 'i', (buf,))
        #print i

        self.m_pfnGetArchiverCaps = self.m_pfnOpenArchive =  self.m_pfnCloseArchive =  self.m_pfnInitEntryEnum =\
        self.m_pfnGetNextEntry    = self.m_pfnProcessMultiple = self.m_pfnEndProcessMulti =  self.m_pfnPackFile =\
        self.m_pfnUnpackFile      = self.m_pfnDeleteEntry =  self.m_pfnConfigurationDlg = self.m_pfnSetChangeVolProc =\
        self.m_pfnSetProcessDataProc = self.m_pfnSetPasswordProc = self.m_pfnMakeDir = self.m_pfnProcessDataProc =\
        self.m_pfnPasswordProc = self.m_pfnSetChangeVolProc = 0


        if(self.m_dllHandle):
            self.m_pfnGetExtensions      = calldll.get_proc_address(self.m_dllHandle, ('GetExtensions'))
            self.m_pfnGetArchiverCaps    = calldll.get_proc_address(self.m_dllHandle, ('GetArchiverCaps'))
            self.m_pfnOpenArchive        = calldll.get_proc_address(self.m_dllHandle, ('OpenArchive'))
            self.m_pfnCloseArchive       = calldll.get_proc_address(self.m_dllHandle, ('CloseArchive'))
            self.m_pfnInitEntryEnum      = calldll.get_proc_address(self.m_dllHandle, ('InitEntryEnum'))
            self.m_pfnGetNextEntry       = calldll.get_proc_address(self.m_dllHandle, ('GetNextEntry'))
            self.m_pfnProcessMultiple    = calldll.get_proc_address(self.m_dllHandle, ('ProcessMultiple'))
            self.m_pfnEndProcessMulti    = calldll.get_proc_address(self.m_dllHandle, ('EndProcessMulti'))
            self.m_pfnPackFile           = calldll.get_proc_address(self.m_dllHandle, ('PackFile'))
            self.m_pfnUnpackFile         = calldll.get_proc_address(self.m_dllHandle, ('UnpackFile'))
            self.m_pfnDeleteEntry        = calldll.get_proc_address(self.m_dllHandle, ('DeleteEntry'))
            self.m_pfnConfigurationDlg   = calldll.get_proc_address(self.m_dllHandle, ('ConfigurationDlg'))
            self.m_pfnSetChangeVolProc   = calldll.get_proc_address(self.m_dllHandle, ('SetChangeVolProc'))
            self.m_pfnSetProcessDataProc = calldll.get_proc_address(self.m_dllHandle, ('SetProcessDataProc'))
            self.m_pfnSetPasswordProc    = calldll.get_proc_address(self.m_dllHandle, ('SetPasswordProc'))
            self.m_pfnMakeDir            = calldll.get_proc_address(self.m_dllHandle, ('MakeDir'))
            self.m_pfnProcessDataProc    = calldll.get_proc_address(self.m_dllHandle, ('ProcessDataProc'))
            self.m_pfnPasswordProc       = calldll.get_proc_address(self.m_dllHandle, ('PasswordProc'))
            self.m_pfnChangeVolProc      = calldll.get_proc_address(self.m_dllHandle, ('ChangeVolProc'))

            #//check minimal requirements for read-only archive plugin
            if( 0 == self.m_pfnGetExtensions      or
                0 == self.m_pfnOpenArchive        or
                0 == self.m_pfnCloseArchive       or
                0 == self.m_pfnGetArchiverCaps    or
                0 == self.m_pfnInitEntryEnum      or
                0 == self.m_pfnGetNextEntry       or
                0 == self.m_pfnUnpackFile ):
                self.Unload()
                return False

            #//cache archive extensions list
            self.m_strExtensions = self.GetExtensions()

            ####################################################
            #test routines
            ####################################################

            ##typedef const char* (*tGetExtensions)();
            #self.GetExtensions()

            #str = 'abcdefgh'
            ##typedef unsigned int    (*tGetArchiverCaps)(const char *szExt);
            #self.GetArchiverCaps (str)

            #typedef int (*tGetNextEntry)(int dwArchID, tArchiveEntry *pInfo);
            #testtArchiveEntry = tArchiveEntry ()
            #self.GetNextEntry (1, testtArchiveEntry)

            #typedef void            (*tProcessMultiple)(int dwArchID, int nOperation);
            #self.ProcessMultiple (1, 2)

            #typedef bool (*tPackFile)(int dwArchID, const char *szFile, const char *SubPath, const char*szDestName);
            #self.PackFile (1, 'fwaber', 'path', 'destname')

            #typedef bool (*tUnpackFile)(int dwArchID, const char *szEntry, const char *szDest);
            #self.UnpackFile (1, 'a', 'b')

            #typedef bool (*tDeleteEntry)(int dwArchID, const char *szEntry);
            #self.DeleteEntry (1, 'abc')

            #def typedef void (*tEndProcessMulti)(int dwArchID);
            #self.EndProcessMulti (1)

            #typedef void (*tInitEntryEnum)(int dwArchID);
            #self.InitEntryEnum (1)

            #typedef void (*tConfigurationDlg)(long hWndParent, long hDllInstance);
            #self.ConfigurationDlg (1234, 56578)

            #typedef void (*tSetChangeVolProc)(int dwArchID, tChangeVolProc pChangeVolProc1);
            #self.SetChangeVolProc (1, self.m_pfnSetChangeVolProc)

            #typedef void *tSetProcessDataProc)(int dwArchID, tProcessDataProc pProcessDataProc, unsigned int dwUser);
            #self.SetProcessDataProc (1, self.m_pfnProcessDataProc, 2)

            #typedef void (*tSetPasswordProc)(tPasswordProc pPwdProc, unsigned int dwUser);
            #self.SetPasswordProc (self.m_pfnPasswordProc, 0)

            #typedef bool (*tMakeDir)(int dwArchID, const char *szDir);
            #self.MakeDir (1, 'testdir')

            #typedef int (*tChangeVolProc)(char *ArcName, int Mode);
            #self.ChangeVolProc ('test', 1)

            #typedef int (*tProcessDataProc)(const char *FileName, int Size, int dwUser);
            #self.ProcessDataProc ('test', 10, 1)

            #typedef int (*tPasswordProc)(char *szPwdBuf, int Size, int dwUser);
            #self.PasswordProc ('abc', 1, 3)

            #typedef int (*tOpenArchive)(const char *);
            #self.OpenArchive ('temp.gz')

            #typedef bool (*tCloseArchive)(int dwArchID);
            #self.CloseArchive (1);

            if(None != self.m_pfnSetPasswordProc):
                self.SetPasswordProc(self.m_pfnPasswordProc, 0)

            #//OK!
            return True

        return False

        def Unload (self, szFile):
            calldll.free_library(self.m_dllHandle)
            self.m_dllHandle = 0



def PasswordProc(FileName, Size, dwUser):
    #//ASSERT(NULL != FileName);
    #//ASSERT(Size > 0);

    #//start password dialog and return typed password
    '''
    #/*TOFIX
    CPasswordDlg dlg;
    dlg.m_bSingleMode = true;

    if(IDOK == dlg.DoModal())
    {
        strncpy(FileName, dlg.m_strPwd, Size);
        FileName[Size-1] = '\0';
    }
    */
    '''
    return 1

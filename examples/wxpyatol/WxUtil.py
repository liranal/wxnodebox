from wxPython.wx import *
import os
import win32api
import win32con
from Globals import *
from Pidl import *

HINSTANCE_ERROR = 32

#def Tokenize(wxString strData, std::vector<wxString> &lstTokenized, char szSeparator)
def Tokenize(strData, lstTokenized, szSeparator = ';'):
    if strData [-1] == szSeparator:
        strData = strData[:-1]
    lstTokenized = strData.split (szSeparator)
    #if lstTokenized [-1] == '':
    #    del lstTokenized[-1]
    return lstTokenized
    '''
    #clear old list contents
    lstTokenized = []
    if strData == '':
        return lstTokenized
    #tokenize string
    strToken = ''
    nStart = 0
    while(True):
        nPos = strData.find(szSeparator, nStart)
        #add new token into the list
        if(nPos > 0):
            strToken = strData[nStart:nPos-nStart]
        else:
            #no match, add rest of the string into the list
            #-strToken = strData[nStart: len (strData)-nStart]
            strToken = strData[nStart:]

        if(strToken != ''):
            lstTokenized.append(strToken)
            #print strToken

        if(nPos > 0):
            #search next token
            nStart = nPos + 1;
        else:
            #no more tokens
            break
    return lstTokenized
    '''
'''
#does file name matches wildcard pattern (*.txt)
#supports wildcards * and ?
#bool fnmatch(const char* pattern, const char *string, bool caseSensitive, bool bDOS)
def fnmat(pattern, string, caseSensitive, bDOS):
    #print string, pattern
    #print fnmatch.fnmatch(string, pattern)
    return fnmatch.fnmatch(string, pattern)
    #return True
    #DOS version assumes '.' always exists
    strPtrn = pattern
    strName = string
    #print 'hi'
    #pos = pattern
    if(bDOS):
        pos = pattern.find('.')
        if(pos):
            strExtPtrn = pattern[pos+1:]

            #extract extension
            strExt = string
            nPos = strExt.rfind('.')
            if(nPos >= 0):
                #before dot
                strName = strExt[:nPos]
                #after dot
                strExt  = strExt[nPos+1:]
                #print '1:', strName, strExt
                #strExt  = strExt.Right(strExt.Len()-nPos-1);

            if(WildMatch(strExtPtrn, strExt, caseSensitive) == False):
                return False

            strPtrn = strPtrn[:pos]

    #match rest of the name
    return WildMatch(strPtrn, strName, caseSensitive)


#internal
#author Jack Handy
#Borrowed from http://www.codeproject.com/string/wildcmp.asp.
#Modified by Joshua Jensen.

#bool WildMatch( const char* pattern, const char *string, bool caseSensitive )
def WildMatch (pattern, string, caseSensitive):
    #Handle all the letters of the pattern and the string.
    #while ( *string != 0  &&  *pattern != '*' )
    #print 'w:', pattern, string
    patternindex = 0
    stringindex = 0
    #print pattern
    #print string
    #print caseSensitive
    while stringindex < len (string): #and patternindex < len (pattern)):
        if (pattern[patternindex] == '*'):
            break;
        #print patternindex, stringindex
        if pattern[patternindex] != '?':
            if (caseSensitive):
                if (pattern[patternindex] != string[stringindex]):
                    return False
            else:
                if (pattern[patternindex].upper() != string[stringindex].upper ()):
                    return False

        patternindex += 1
        stringindex += 1
        if patternindex == len(pattern):
            if patternindex == len (string):
                return True
            else:
                #return False
                break
        #print 'test:', string, stringindex, pattern, patternindex,

    #print 'p1:', pattern, patternindex, string, stringindex
    mp = ''
    cp = ''
    while (stringindex < len (string) and patternindex < len (pattern)):
        #print 'inside loop'
        if (pattern[patternindex] == '*'):
            #It's a match if the wildcard is at the end.
            patternindex += 1
            if (patternindex >= len(pattern)):
                return True

            mp = pattern[patternindex:]
            cp = string[stringindex + 1:]
        else:
            if (caseSensitive):
                if (pattern[patternindex] == string[stringindex]) or  pattern[patternindex] == '?':
                    patternindex += 1
                    stringindex += 1
                else:
                    pattern = mp
                    #fragezeichen
                    patternindex = 0
                    string = cp[:]
                    cp = cp [1:]
                    #fragezeichen
                    stringindex = 0
            else:
                if (pattern[patternindex].upper() == string[stringindex].upper) or pattern[patternindex] == '?':
                    patternindex += 1
                    stringindex += 1
                else:
                    pattern = mp
                    patternindex = 0
                    string = cp[:]
                    cp = cp [1:]
                    stringindex = 0

    #print 'p:', pattern, patternindex
    #Collapse remaining wildcards.
    #while (pattern[patternindex] == '*'):
    while (patternindex < len(pattern)):
        if (pattern[patternindex] == '*'):
            patternindex += 1
        else:
            break

    return patternindex >= len(pattern)# - 1
'''
#Format number as string separating every three digits
#with given separator for better readibility
#wxString FormatSize(wxInt64 nValue, char cDelimiter)
def FormatSize(nValue, cDelimiter = ','):
    #static const wxString strFormat = wxString::Format('%%%sd', wxLongLongFmtSpec)
    #strFormat = '%%%sd'
    #print nValue, cDelimiter
    #wxString strResult;
    strValue = str(nValue)
    #add delimiter to format size number
    #NOTE: delimiter is added from end of string forward to the start
    #      because it simplifies the calculation (next insertion
    #      point does not change index as we insert delimiters)
    '''
    nLen = len(strValue)
    nCommas = (nLen-1)/3;
    #print nCommas
    strResult = ''
    for i in range (nCommas + 1):
        #print nCommas, i
        pos = nLen - 3 * i
        if i > 0:
            strResult += cDelimiter
        strResult += strValue [pos: pos + 3]
        #strResult.insert(nLen-3*(i+1), cDelimiter)
    #strResult += strValue [:pos]
    #print strResult
    strResult += strValue [pos:]
    return strResult
    '''

    nLen = len(strValue)
    nCommas = (nLen-1)/3;
    nPos = nLen - nCommas * 3
    strResult = strValue [:nPos]
    for i in range(nCommas):
        #strResult.insert(nLen-3*(i+1), cDelimiter);
        strResult += cDelimiter
        strResult += strValue [nPos: nPos + 3]
        nPos += 3
    return strResult


#bool ExecuteFile(const char *szFile, const char *szArgs, const char *szDir, void *nData)
def ExecuteFile(szFile, szArgs, szDir, nData):
    strPath = szDir
    #//TOFIX
    strPath += szFile
    #print strPath
    #ifdef __WXMSW__
    #//determine what verb to use
    szVerb = ''
    szCmdLine = ''
    path = szFile
    #print path
    #wxFileName path(szFile);

    szVerb, ret = GetDefaultVerb(os.path.splitext(path)[1], szCmdLine)
    if not ret:
        szVerb = 'open'
        #//some cases ('.avi' on XP) do not work without this set explicitly!!

    #SHELLEXECUTEINFO si;

    ##HWND  hwnd, // handle to parent window
    ##LPCTSTR  lpOperation,   // pointer to string that specifies operation to perform
    ##LPCTSTR  lpFile,    // pointer to filename string
    ##LPTSTR  lpParameters,   // pointer to string that specifies executable-file parameters
    ##LPCTSTR  lpDirectory,   // pointer to string that specifies default directory
    ##INT  nShowCmd   // whether file is shown when opened

    #ZeroMemory(&si,sizeof(si));
    #si.cbSize       = sizeof(si);
    #si.lpVerb       = szVerb;
    #si.nShow        = SW_SHOW;
    #si.lpParameters = szArgs;
    #si.lpDirectory  = szDir;
    #si.fMask        = SEE_MASK_FLAG_NO_UI|SEE_MASK_FLAG_DDEWAIT|SEE_MASK_NOCLOSEPROCESS;
    #si.hwnd         = (HWND)nData;

    #//FIX use pidl as primary execute way instead of path to prevent bug
    #//    with files with name like 'ftp.htm', 'ftp.dat' where system
    #//    tries to open some 'fantom' ftp site
    #HINSTANCE result = 0;
    #LPITEMIDLIST pidl = PIDL::GetFromPath(strPath);
    pidl_instance = PIDL()
    #TOMAKEBETTER: make better: this is a static method
    # better name
    pidl_instance = pidl_instance.GetFromPath(strPath)
    if(1 != pidl_instance):
    #if 1:
        ##si.lpIDList = (LPVOID)pidl;
        ##si.fMask   |= SEE_MASK_INVOKEIDLIST;
        ##ShellExecuteEx(&si);
        #result = win32api.ShellExecute (nData, 'open', 'cmd', 'dir', '.', 1)
        #print win32con.SW_SHOW
        #TODO: use ShellExecuteEx: use messagebox 'das system kann angegebene Datei nicht finden'
        #print nData, szVerb, szFile, szArgs, szDir, win32con.SW_SHOW
        result = win32api.ShellExecute (nData, szVerb, szFile, szArgs, szDir, win32con.SW_SHOW)
        ##result = win32api.ShellExecute (0, 'open', 'cmd', 'dir', '.', 1)
        #pidl_instance.free(pidl)
        ##result = si.hInstApp;
    #}
    #//if PIDL version fails revert to path based version
    #//PIDL can fail:
    #// 1. szFile is URL
    #// 2. on WinXP failed with .avi file on CDROM drive!
    if (result <= HINSTANCE_ERROR):
        #si.lpIDList = NULL;
        #si.fMask   &= ~SEE_MASK_INVOKEIDLIST;
        si.lpFile = szFile
        result = win32api.ShellExecute (nData, szVerb, szFile, szArgs, szDir, win32con.SW_SHOW)
        #ShellExecuteEx(&si);
        #result = si.hInstApp;

    #// If it failed, get the .htm regkey and lookup the program
    if (result > HINSTANCE_ERROR):
        return True

    if SE_ERR_NOASSOC != result and SE_ERR_ASSOCINCOMPLETE  != result:
        self.ShowSystemErrorMessge(result)
        return false

    #//use our own version of the FindExecutable() ???
    #char szRes[MAX_PATH];
    if FindExecutable(szFile, szDir, szRes):
        #char szAppPath[MAX_PATH];
        #lstrcpyn(szAppPath, szDir, MAX_PATH);
        szAppPath = szDir [:MAX_PATH]
        #lstrcat(szAppPath, szFile);
        szAppPath += szFile;
        #what does PathQuoteSpaces do?
        #propably, what the name says
        #PathQuoteSpaces(szAppPath);
        szAppPath = "\"" + szAppPath + "\""

        #//TOFIX ShellExecute?
        #lstrcat(szRes, _T(' '));
        szRes += ' '
        #lstrcat(szRes, szAppPath);
        szRes += szAppPath
        #HINSTANCE result = (HINSTANCE)WinExec(szRes, SW_SHOW);
        result = WinExec(szRes, SW_SHOW)
        if result > HINSTANCE_ERROR:
            return True
        else:
            self.ShowSystemErrorMessge(result)
            return False

    #//at this point there were no association and we failed to find it manually
    OpenWith(szFile, szArgs, szDir)
    return true
    #else
    '''
    #strPath += '/'
	//::wxShell();  //TOFIX blocks main thread!!!
    //cmd << _T('/bin/sh -c '') << command << _T('\'');
	//pid_t pid = fork();
    //if ( pid == 0 )  // we're in child
    //{
    //   execvp (*mb_argv, mb_argv);
    //   _exit(-1);         // there is no return after successful exec()
    //}
    //return (::wxExecute(szFile, wxEXEC_ASYNC) == 0);

    wxString command;

	//if file is ELF executable, execute it directly
	struct stat64 st;
	if(0 == stat64(strPath.c_str(), &st))
	{
		if(st.st_mode & S_IXUSR)
		{
			//TOFIX?
            //command.Pr intf('/bin/sh -c '%s'', strPath.c_str());
			//wxExecute (command, wxEXEC_ASYNC);
			//return true;
		}
	}

	//TOFIX test: this should work both for Linux and Windows
	//TOFIX if file has executable flag?
	wxFileName name(szFile);
	wxFileType * ft ;
    wxString strExt = '.' + name.GetExt();

	ft = wxTheMimeTypesManager->GetFileTypeFromExtension(strExt);
    if ( ( ft ) && (ft->GetOpenCommand(&command, wxFileType::MessageParameters(strPath, ''))) )
	{
		//wxMessageBox(command);
		wxExecute (command, wxEXEC_ASYNC);
		delete ft ;
		return true;
	}
	else	// else an unknown (un associated file on this system
	{
        //command.Pr intf('/bin/sh -c '%s\'', szFile);
		//TOFIX open in editor?
        command.Pr intf('gedit '%s'', strPath.c_str());
		return (::wxExecute(command, wxEXEC_ASYNC) == 0);
    #//wxMessageBox(_("Failed to find associated application!"));
	}
    return False
    '''

    #endif

#wxString FormatSizeUnits(wxInt64 nBytes)
def FormatSizeUnits (nBytes):
    #print 'FormatSizeUnits'

    #wxString strResult;

    if(nBytes < 1024):
        #//less than 1 kB
        strResult = '%d bytes' % nBytes
    else:
        #//1 kB or larger
        dValue = nBytes
        #// convert to kB
        dValue /= float (1024)

        if(dValue < 1024):
            #//less than 1MB, stay with kB (one decimal place for kB)
            strResult = '%.1f kB' % dValue
        else:
            #//1 MB or larger
            #// convert to MB
            dValue /= float (1024)

            if(dValue < 1024):
                #//less than 1GB, stay with MB (two decimal places for MB)
                strResult = '%.2f MB' % dValue
            else:
                #// convert to GB
                dValue /= float (1024)

                #//if GB use two decimal places
                strResult = '%.2f GB' % dValue

    return strResult

#bool GetDefaultVerb(const char *szExt, char *szVerb, char *szCmdLine)
def GetDefaultVerb(szExt, szCmdLine):
    szVerb = ''
    #print 'GetDefaultVerb'
    #return
    #//File extension string equals to the registry key name.
    #//Value of this key points to another registry key describing shell actions
    #//for given file format (described by file extension string)
    szKey = ''
    if FindExecutableKey(szExt, szKey):
        #//TOFIX lstrcpyn
        szKey2 = szKey
        szKey2 += '\\shell'

        #//See if 'shell' subkey has default value defined
        #//(default shell action verb for this format)
        szVerb = win32api.RegQueryValue (win32con.HKEY_CLASSES_ROOT, szKey2)

        if (GetRegKey(HKEY_CLASSES_ROOT, szKey2, szVerb) == ERROR_SUCCESS) and len(szVerb) > 0:
            #//test if the verb is valid (must have valid 'command' subkey)
            szKey2 += '\\'
            szKey2 += szVerb
            szKey2 += '\\command'

            #//default value of '\\shell\\VERB\\command' subkey (replace VERB with actual value)
            #//gives us command line string (app + parameters)
            if GetRegKey(HKEY_CLASSES_ROOT, szKey2, szCmdLine) == ERROR_SUCCESS:
                return True
            szCmdLine = win32api.RegQueryValue (win32con.HKEY_CLASSES_ROOT, szKey2)
            if len (szCmdLine) > 0:
                return szVerb, True
        #//no default verb defined
        else:
            #//test for presence of standard 'open' subkey
            #//TOFIX lstrcpyn
            szKey2 = szKey
            #print szKey2
            #szKey2 += '\\shell\\open\\command'
            szKey2 += '\\shell\\shell\\open\\command' # auf meinem pc francesco
            #print szKey2

            #TODO
            szCmdLine =''
            #szCmdLine = win32api.RegQueryValue (win32con.HKEY_CLASSES_ROOT, szKey2)
            if len (szCmdLine) > 0:
                szVerb = 'open'
                #TODO: it works?
                if GetRegKey(HKEY_CLASSES_ROOT, szKey2, szCmdLine) == ERROR_SUCCESS:
                    szVerb = _('open')
                return szVerb, True

            #//else (last chance to find default verb)
            #//take first available subkey under 'shell'
            #//TOFIX lstrcpyn
            szKey2 = szKey
            szKey2 += '\\shell'

            #//enumerate subkeys until we find first subkey name
            #HKEY hkey;
            #RegOpenKeyEx(key, subKey , reserved , sam )
            try:
                win32api.RegOpenKeyEx(win32con.HKEY_CLASSES_ROOT, szKey2, 0, KEY_ENUMERATE_SUB_KEYS)
                #LONG retval = RegOpenKeyEx(HKEY_CLASSES_ROOT, szKey2, 0, KEY_ENUMERATE_SUB_KEYS, &hkey);
                ##retval = 0,

                #TODO: returns tuple?
                retval = win32api.RegEnumKeyEx (hkey)
                #retval = RegEnumKeyEx(hkey, 0, szVerb, &datasize, NULL, NULL, NULL, NULL);
                #RegCloseKey(hkey);
                win32api.RegCloseKey (hkey)
                #if (retval == ERROR_SUCCESS):
                if (retval != 0):
                    #//test if the verb is valid (must have valid 'command' subkey)
                    szKey2 = '\\'
                    szKey2 += szVerb
                    szKey2 += '\\command'

                    #//default value of '\\shell\\VERB\\command' subkey (replace VERB with actual value)
                    #//gives us command line string (app + parameters)
                    #TODO: it works?
                    if GetRegKey(HKEY_CLASSES_ROOT, szKey2, szCmdLine) == ERROR_SUCCESS:
                        return True
                    szCmdLine = win32api.RegQueryValue (win32con.HKEY_CLASSES_ROOT, szKey2)
                    return szVerb, True
            except:
                pass

    return szVerb, False

def ShowSystemErrorMessge(nError):
    #print "ShowSystemErrorMessge"
    #string = win32api.FormatMessage(errCode)
    lpMsgBuf = win32api.FormatMessage(\
        win32con.FORMAT_MESSAGE_ALLOCATE_BUFFER |\
        win32con.FORMAT_MESSAGE_FROM_SYSTEM |\
        win32con.FORMAT_MESSAGE_IGNORE_INSERTS,\
        NULL,\
        nError,\
        win32api.MAKELANGID(win32con.LANG_NEUTRAL, win32con.SUBLANG_NEUTRAL)\
        , None)

    #//format and show system error message
    #LPVOID lpMsgBuf;
    #FormatMessage(  FORMAT_MESSAGE_ALLOCATE_BUFFER |
    #                FORMAT_MESSAGE_FROM_SYSTEM |
    #                FORMAT_MESSAGE_IGNORE_INSERTS,
    #                NULL,
    #                nError,
    #                MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
    #                (LPTSTR) &lpMsgBuf, 0, NULL );
    wxMessageBox(lpMsgBuf, str(nError))
    #LocalFree( lpMsgBuf );

#def OpenWith(sefl, LPCSTR szApp, LPCSTR szArgs, LPCSTR szDir)
def OpenWith(szApp, szArgs, szDir):
    #//our last chance is to start 'Open With' shell dialog
    #wxString strParams;
    strParams = 'shell32.dll,OpenAs_RunDLL'
    strParams += szApp

    hInstance = win32api.ShellExecute (NULL, 'open', 'rundll32.exe', strParams, szDir, 1) #/*TOFIX CMD_SHOW?*/);

    if hInstance <= 32:
        #//format and show system error message
        self.ShowSystemErrorMessge(hInstance)
        return False

    return True

def FindExecutableKey(szExt, szBuffer):
    #TODO: it works?
    if GetRegKey(HKEY_CLASSES_ROOT, szExt, szBuffer) == ERROR_SUCCESS:
        return True
    szBuffer = win32api.RegQueryValue (win32con.HKEY_CLASSES_ROOT, szExt)
    if len (szBuffer) > 0:
        return True
    else:
        return False

g_found = False
g_path = ""

def GetExecutablePath():
    #static bool found = false;
    #static wxString path;

    global g_found
    global g_path
    if (g_found):
        return g_path
    else:
        #ifdef __WXMSW__
        #char buf[512];
        #*buf = '\0';
        #g_path = win32api.GetModuleFileName (0)
        g_path = os.getcwd()
        #print g_path
        #path = buf;
        #pass
    '''
        #elif defined(__WXMAC__)

        ProcessInfoRec processinfo;
        ProcessSerialNumber procno ;
        FSSpec fsSpec;

        procno.highLongOfPSN = NULL ;
        procno.lowLongOfPSN = kCurrentProcess ;
        processinfo.processInfoLength = sizeof(ProcessInfoRec);
        processinfo.processName = NULL;
        processinfo.processAppSpec = &fsSpec;

        GetProcessInformation( &procno , &processinfo ) ;
        path = wxMacFSSpec2MacFilename(&fsSpec);
    #else
        wxString argv0 = wxTheApp->argv[0];

        if (wxIsAbsolutePath(argv0))
            path = argv0;
        else
        {
            wxPathList pathlist;
            pathlist.AddEnvList(_("PATH"));
            path = pathlist.FindAbsoluteValidPath(argv0);
        }

        wxFileName filename(path);
        filename.Normalize();
        path = filename.GetFullPath();
    #endif
    '''
    g_found = True
    return g_path

    def OpenCommandPrompt(strDir, nData):
        #TODO
        #ifdef __WXMSW__
        #   SHELLEXECUTEINFO si;
        #   si.cbSize       = sizeof(si);
        #   si.fMask        = 0;
        #   si.hwnd         = (HWND)nData;  //m_hWnd
        #   si.lpVerb       = "open";
        #   //si.lpFile     = (SHELL::IsWinNT())? "cmd.exe" : "command.com";  //TOFIX
        #   si.lpFile       = "cmd.exe";
        #   si.lpParameters = NULL;
        #   si.lpDirectory  = strDir;
        #   si.nShow        = SW_SHOWNORMAL;

        #   ShellExecuteEx(&si);

        #   if(si.hProcess){
        #       //TOFIX set your title to this new window -> get main window from process
        #       //EnumThreadWindows((DWORD)(si.hProcess), EnumCmdPrompt, 0);
        #       //EnumWindows(EnumCmdPrompt, (DWORD)(si.hProcess));
        #       //CloseHandle(si.hProcess);
        #   }
        #
        #else
        #
        #   //::wxShell();  //TOFIX blocks main thread!!!
        #   ::wxSetWorkingDirectory(strDir);
        #   ::wxExecute("gnome-terminal", wxEXEC_ASYNC);
        #   //ExecuteFile("gnome-terminal", NULL, szDir, NULL)  //TOFIX
        #
        #endif
        pass

    #def GetRegKey (HKEY key, LPCTSTR subkey, LPTSTR retdata)
    def GetRegKey (key, subkey, retdata):
        #TODO
        #HKEY hkey;
        retval = win32api.RegOpenKeyEx(key, subkey, 0, KEY_QUERY_VALUE)

        if (retval == ERROR_SUCCESS):
            szBuffer = win32api.RegQueryValue(key, subkey)
            retdata = szBuffer
            RegCloseKey(key)

        return retval


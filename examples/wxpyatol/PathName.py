from WxUtil import *
import win32api

class PathName:
    def __init__(self):
        pass

    def GetIniDirectory(self):
        #ifdef __WXMSW__
        #//wxFileName path(::wxPathOnly(GetExecutablePath()));
        #//path.AppendDir(wxString('settings'));
        #//strDir = path.GetFullPath();
        #strDir = ::wxPathOnly(GetExecutablePath());
        #strDir = 'c:/Eigene Dateien/python/wxpyatol'
        strDir = GetExecutablePath ()
        strDir += '/settings'
        #else
        #wxFileName path;
        #path.AssignHomeDir();
        #path.AppendDir(wxString('.atol'));
        #strDir = path.GetFullPath();
        #endif

        return strDir;

    #//NOTE: only for local paths
    #bool PathName::EnsureDirExists(wxString &strDir)
    def EnsureDirExists(self, strDir):
        #// remove ending / if exists
        #TOMAKEBETTER?
        if strDir [-1] == "/" or strDir [-1] == "\\":
            strDir = strDir[:len(strDir) - 1]

        #// check if the directory already exists
        #ifdef __WXMSW__
        #define stat _stat
        #define S_IFDIR _S_IFDIR
        #endif
        #mode = os.stat(pathname)[ST_MODE]
        #print strDir
        #if os.path.isfile(strDir):
        if os.path.isdir(strDir):
            return True
        #if(0 == stat(strDir.c_str(), &st)){
        #    #//file exists, check if it is directory
        #    return (S_IFDIR == (st.st_mode & S_IFDIR));
        #}

        #// recursively check parent directory
        #int nPos = strDir.find_last_of(DELIMITERS);
        #TOMAKEBETTER: could use regular expressions
        nPos = strDir.rfind('/')
        if nPos == -1:
            nPos = strDir.rfind('\\')

        if -1 == nPos:
            #//no more searching (root/volume level)
            return True

        strParentDir = strDir[:nPos]
        if not self.EnsureDirExists(strParentDir):
            return False

        #//now create this directory
        os.mkdir (strDir)
        #print "mkdir", strDir
        return True

    def GetExt (self, szPath):
        index = szPath.find('.')
        if index != -1:
            return szPath[index:]
        else:
            return ''

    def GetBaseName(self, szPath):
        #strDelimiters = "/\\"
        strPath = szPath
        #TOMAKEBETTER:
        nPos = strPath.rfind('/')
        if nPos == -1:
            nPos = strPath.rfind('\\')

        #nPos = strPath.find_last_of(strDelimiters);
        if nPos >= 0:
            return strPath[len(strPath) - nPos - 1:]

        return ""

    #void PathName::EnsureTerminated(wxString &strPath, char cDelimiter)
    def EnsureTerminated (self, strPath, cDelimiter):
        if(strPath == ''):
            #print 'empty', strPath
            strPath += cDelimiter
        else:
            cLast = strPath [-1]
            #print cLast
            if(cLast != '\\' and cLast != '/'):
                strPath += cDelimiter
                #print 'ins', strPath
        return strPath
        #print 'ens:', strPath

    #void PathName::EnsureNotTerminated(wxString &strPath)
    def EnsureNotTerminated(self, strPath):
        if(strPath != ''):
            cLast = strPath [-1]
            if(cLast == '\\' or cLast == '/'):
                strPath = strPath[:-1]
        return strPath


    def Path_TempDirectory(self):
        #ifdef __WXMSW__
        #TCHAR szPathBuffer[MAX_PATH] = "";
        #GetTempPath(MAX_PATH, szPathBuffer);
        return win32api.GetTempPath ()

        #return wxString(szPathBuffer);
        #else
        #    return wxString("/tmp");
        #endif

    #wxString PathName::GetParentDirPath(const char *szPath)
    def GetParentDirPath(self, szPath):
        #static const wxString strDelimiters('/\\');

        #print 'parentdirpath of ', szPath
        strPath=szPath
        #wxString strPath(szPath);
        strPath = self.EnsureNotTerminated(strPath)
        #print '1:', strPath

        #size_t nPos = strPath.find_last_of(strDelimiters);
        #TOMAKEBETTER: could use regular expressions
        nPos = strPath.rfind('/')
        if nPos == -1:
            nPos = strPath.rfind('\\')

        #nPos = strPath.find_last_of(strDelimiters);
        #print nPos
        if(nPos > 0):
            strPath = strPath[:nPos]
        else:
            strPath = ''
        #print '2:', strPath

        # make better (for linux); query sysplatform
        strPath = self.EnsureTerminated(strPath, '\\')
        #print '3:', strPath
        return strPath;

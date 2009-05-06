from wxPython.wx import *
#wxInputStreamPtr
#wxTextFile?
from ConfigParser import *
from PathName import *

class IniFile:
    def __init__ (self):
        self.m_bDirty = false
        # Read datas
        self._config=ConfigParser()

    def SetPath (self, szFile):
        self.m_strPath = szFile

    #bool IniFile::Load(const char *szFile)
    def Load(self, szFile = None):
        if szFile == None:
            szFile = self.m_strPath
        self.m_bDirty = False   #//init flag
        #self.m_contents = []    #//clear storage
        self.SetPath(szFile)
        #print 'read'
        self._config.read(szFile)
        #self.Save()
        #print 'write'

        #self.m_sections = self._config.sections # lsit ['default', 'panel']
        #self.m_contents # keys

        return True

    def Save(self):
        #print 'write'
        self.m_bDirty = False

        #strDir = ::wxPathOnly(m_strPath);
        #TOFIX check success
        strDir = os.path.dirname (self.m_strPath)
        path_instance = PathName ()
        path_instance.EnsureDirExists(strDir)

        #open the INI file for writing
        #if(!iniFile.is_open())
        #  return false;
        f=open(self.m_strPath, 'w')
        self._config.write(f)
        f.close()

        #self._config.write(self.m_strPath)

        return True

    def ClearAll(self):
        #TODO: how to clear all
        self.m_bDirty = True
        #self.m_contents.clear()
        return True

    def SectionExists(self, szSection):
        return self._config.has_section(szSection)

    def KeyExists(self, szSection, szKey):
        return self._config.has_option(szSection, szKey)

    def GetValue (self, szSection, szKey, szDefault):
        if (self._config.has_option(szSection, szKey)):
            #TODO (return false, true und zuweisen)
            #self.get(section, option[, raw[, vars]])
            return self._config.get(szSection, szKey)
            #return True
        else:
            return szDefault
            #return False

    def SetValue (self, szSection, szKey, val):
        self.m_bDirty = True    #//content changes
        if not self._config.has_section(szSection):
            self._config.add_section(szSection)
        self._config.set (szSection, szKey, val)
        return True

    def AddSection (self, szSection, szKey, val):
        self.m_bDirty = True
        self._config.add_section(szSection)
        return True    #section already exists

    def RemoveSection (self, szSection):
        self._config.remove_section(szSection)
        return True


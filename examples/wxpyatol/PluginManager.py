from ArchiverPlugin import *
from MyDirTraverser import *
from PathName import *
from VfsListing import *
##import calldll
PLUGIN_EXT = '.atp'

class PluginManager:
#class PluginManager(ArchiverPlugin):
    #hat die liste drin
    def __init__ (self):
        #ArchiverPlugin.__init__ (self)
        #self.m_mapExt = []
        self.m_ArchiverList = []

    def LoadPlugins (self, szDir):
        #//empty plugin list
        #//scan directory for files (to load all plugins found)
        log = wxLogNull ()
        #VfsListing lstData;

        lstData = VfsListing ()
        lstData.Clear()
        MyDirTraverser (lstData, szDir)
        #print lstData
        strDir = szDir

        for i in range (lstData.GetCount()):
            #print i, PathName.GetExt(PathName(), lstData.GetAt(i).GetName())
            if PathName.GetExt(PathName(), lstData.GetAt(i).GetName()) == PLUGIN_EXT:
                #//TRACE('Plugin candidate: %s\n', szFile);
                strPath = strDir
                strPath += '/'
                strPath += lstData.GetAt(i).GetName()
                #print strPath

                lib = ArchiverPlugin ()
                if(lib.Load(strPath)):
                    #//TRACE('Plugin %s loaded\n', szFile);
                    self.m_ArchiverList.append(lib)
                    #//TOFIX ovo pravi kopiju objekta ? (a da -...vamo pointer)
        self.MapExtensions()


    #//unload plugins and empty plugin list
    def FreePlugins (self):
        #clear()
        for i in self.m_ArchiverList:
            i.Unload()
        #//for(int i=0; i<size(); i++)
        #//  operator [](i).Unload();
        pass

    def MapExtensions(self):
        lstTokens = []

        self.m_mapExt = {}

        for i in range(len(self.m_ArchiverList)):
        #for i in self.m_ArchiverList:
            #print  i.m_strExtensions
            lstTokens = Tokenize(self.m_ArchiverList[i].m_strExtensions, lstTokens, ';');
            #print lstTokens, lstTokens[0],  lstTokens[1]

            for j in range (len (lstTokens)):
            #for j in lstTokens:
                #//TOFIX find first?; protect from multiple plugins for same format
                #m_mapExt[lstTokens[j]] = i;
                #!!!map
                self.m_mapExt[lstTokens[j]] = i


    def GetCount(self):
        return len(self.m_ArchiverList)

    #ArchiverPlugin *FindArchiver(const char *szFileExt);
    def FindArchiver(self, szFileExt):
        #//check arguments
        if(None == szFileExt or '' == szFileExt):
            return 0

        if szFileExt in m_mapExt:
            ind = m_mapExt.index(szFileExt)
            return m_mapExt[ind]

        #//not found
        return 0

from PathName import *
from IniFile import *

class BrowseBookmark:
    def __init__ (self, m_strTitle, m_strPath):
        self.m_strTitle  = m_strTitle
        self.m_strPath   = m_strPath

    def IsValid(self):
        return self.m_strTitle != '' and self.m_strPath != ''

class BrowseBookmarkList:
    def __init__ (self):
        self.g_szSection = 'Bookmarks'
        self.m_lstBookmarks = []

    def CalcFileName(self):
        p = PathName ()
        strFile = p.GetIniDirectory()
        #//TOFIX
        strFile += '/'
        strFile += 'bookmarks.ini';
        #print strFile
        return strFile

    def Load(self):
        strFile = self.CalcFileName()

        ini = IniFile ()
        if not ini.Load(strFile):
            return False

        nTotalCount = int (ini.GetValue('Bookmarks', 'Count', 0))
        #print nTotalCount

        strKey = ''
        for i in range(nTotalCount):
            strKey = '%d_Title' % i
            strTitle = ini.GetValue(self.g_szSection, strKey, '')
            strKey = '%d_Path' % i
            strPath = ini.GetValue(self.g_szSection, strKey, '')
            item = BrowseBookmark (strTitle, strPath)

            if(item.IsValid()):
                self.m_lstBookmarks.append (item)

        return True

    def GetCount(self):
        return len(self.m_lstBookmarks)

    def Clear(self):
        self.m_lstBookmarks = []

    def Save(self):
        strFile = self.CalcFileName()

        ini = IniFile ()
        ini.SetPath(strFile)
        #ini.Load()#strFile)

        nTotalCount = len (self.m_lstBookmarks)
        ini.SetValue(self.g_szSection, 'Count', nTotalCount);


        for i in range(nTotalCount):
            strKey = '%d_Title' % i
            ini.SetValue(self.g_szSection, strKey, self.m_lstBookmarks[i].m_strTitle)
            strKey = '%d_Path' % i
            ini.SetValue(self.g_szSection, strKey, self.m_lstBookmarks[i].m_strPath)

        if not ini.Save():
            return False

        return True

    def FindBookByTitle(self, szTitle):
        for i in range(len(self.m_lstBookmarks)):
            if (self.m_lstBookmarks[i].m_strTitle == szTitle):
                return i
        #not found
        return -1

    def FindBookByPath(self, szTitle):
        for i in range(len(self.m_lstBookmarks)):
            if (self.m_lstBookmarks[i].m_strPath == szPath):
                return i
        #not found
        return -1

    def Remove(self, nIdx):
        #ASSERT(0 <= nIdx && nIdx < size());
        del self.m_lstBookmarks[nIdx]

    def Insert(self, strTitle, strPath):
        if self.FindBookByTitle(strTitle) >= 0:
            #can not overwrite existing bookmark
            return False

        item = BrowseBookmark (strTitle, strPath)
        self.m_lstBookmarks.append(item)
        return True

    def GetBookPath(self, nIdx):
        return self.m_lstBookmarks[nIdx].m_strPath

    def GetBookTitle(self, nIdx):
        return self.m_lstBookmarks[nIdx].m_strTitle

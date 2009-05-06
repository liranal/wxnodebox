from VfsItem import *

class VfsSelectionItem(VfsItem):
    def __init__ (self, newentry = None):
        VfsItem.__init__ (self)
        self.m_lstSubItems = []
        #copy constructor
        #TOMAKEBETTER: direct kopieren mit copy oder deepcopy?
        if newentry != None:
            self.m_strName =         newentry.m_strName
            self.m_nSize =           newentry.m_nSize
            self.m_nExtPos  =        newentry.m_nExtPos
            self.m_nLastModDate =    newentry.m_nLastModDate
            self.m_nAttrib  =        newentry.m_nAttrib
            self.m_nIconIdx =        newentry.m_nIconIdx

        #if newentry != None:
            #self.m_lstSubItems.append (newentry)



class VfsSelection:
    def __init__ (self):
        #self.m_lstRootItems = []
        self.Clear ()

    def Clear(self):
        self.m_lstRootItems = []

    def GetTotalCount(self):
        nSize = len (self.m_lstRootItems)
        uCount = nSize
        #print nSize
        for i in range (nSize):
            #print i
            uCount += self.GetTotalCountRecursive(self.m_lstRootItems[i])
        return uCount

    #def GetTotalCountRecursive(VfsSelectionItem *pItem)
    def GetTotalCountRecursive(self, pItem):
        uCount = 0
        if(None != pItem):
            nSize = len (pItem.m_lstSubItems)
            uCount = nSize
            for i in range (nSize):
                #uCount += GetTotalCountRecursive(&(pItem->m_lstSubItems[i]))
                uCount += self.GetTotalCountRecursive(pItem.m_lstSubItems[i])
        return uCount

    def GetTotalSize(self):
        uSize = 0

        nCount = len (self.m_lstRootItems)
        #print "c", nCount
        for i in range (nCount):
            uSize += self.GetTotalSizeRecursive(self.m_lstRootItems[i])
        return uSize

    #wxInt64 VfsSelection::GetTotalSizeRecursive(VfsSelectionItem *pItem)
    def GetTotalSizeRecursive(self, pItem):
        uSize = 0

        if(None != pItem):
            if(pItem.IsDir()):
                if(not pItem.IsDots()):
                    nCount = len (pItem.m_lstSubItems)
                    for i in range (nCount):
                        uSize += self.GetTotalSizeRecursive(pItem.m_lstSubItems[i])
            else:
                #print "usi", pItem.m_nSize
                uSize = pItem.m_nSize
        return uSize


    #search hierarchicaly using path 'dir1/dir2/file'
    #std::vector<VfsSelectionItem> *VfsSelection::Find(const char *szPath)
    def Find(self, szPath):
        strDir = szPath
        pChildList = self.m_lstRootItems

        #TOFIX extract Drive first (search for ':\\' like in 'C:\\')
        #while(-1 < (nPos = strDir.find('\\/')))
        while(-1 < strDir.find('\\')):
            #TODO: better solution in python
            nPos = strDir.find('\\')
            strName = strDir [:nPos]
            strDir = strDir[nPos + 1]

            if(0 == nPos):
                continue

            item = VfsSelectionItem ()
            item.SetName(strName)

            #!! .index
            if item in pChildList:
                if (strDir == ''):
                    return pChildList [pChildList.index(item)].m_lstSubItems
                else:
                    pChildList = pChildList [pChildList.index (item)].m_lstSubItems
            else:
                return None

        #last in line
        if(strDir != ''):
            item = VfsSelectionItem ()
            item.SetName(strDir)
            if item in pChildList:
                return pChildList [pChildList.index (item)].m_lstSubItems
            else:
                return None
        return pChildList

    def Insert(self, szPath):
        #ensure path not prefixed with delimiters
        while(szPath != None and (szPath[0] == '\\' or szPath[0] == '/')):
            szPath = szPath[1:]

        strDir = szPath
        pParent = None
        pEntry = None

        #TOFIX extract Drive first (search for ':\\' like in 'C:\\')
        while(-1 < strDir.find('\\')):
            nPos = strDir.find ('\\')
            strName = strDir[:nPos]
            strDir = strDir[nPos+1:]

            entry = VfsSelectionItem ()
            entry.SetName(strName)
            entry.m_nAttrib = ATTR_DIR

            pEntry = self.InsertUnder(entry, pParent)
            if(None == pEntry):
                return None

            pParent = pEntry

        #last in line
        if(strDir != ''):
            entry = VfsSelectionItem ()
            entry.SetName(strDir)

            pEntry = self.InsertUnder(entry, pParent)
        return pEntry


    #TOFIX insert as child?
    #VfsSelectionItem *VfsSelection::InsertUnder(VfsSelectionItem &item, VfsSelectionItem *pParent)
    def InsertUnder(self, item, pParent):
        #ASSERT_VALID(this)

        #std::vector<VfsSelectionItem> *pList = &m_lstRootItems;
        pList = self.m_lstRootItems
        if(None != pParent):
            pList = pParent.m_lstSubItems

        #std::vector<VfsSelectionItem>::iterator It = std::find(pList->begin(), pList->end(), item);
            if item in pChildList:
                if (strDir == ''):
                    return pChildList [pChildList.index(item)].m_lstSubItems
                else:
                    pChildList = pChildList [pChildList.index (item)].m_lstSubItems
            else:
                return None

        if item in pList:
            return pList[pList.index(item)]
        else:
            pList.append(item)

            #TOFIX move this out ?
            #NOTE: some 'bad' archives have not directory flag set for some directories
            if(None != pParent and not pParent.IsDir()):
                pParent.m_nAttrib = ATTR_DIR

            #return &((*pList)[pList->size()-1]);
            return pList [-1]

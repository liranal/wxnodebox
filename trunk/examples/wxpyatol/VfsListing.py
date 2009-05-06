from FilterDesc import *

ST_NONE = 0
ST_NAME = 1
ST_EXT  = 2
ST_SIZE = 3
ST_DATE = 4
ST_ATTR = 5

class VfsListing:
    def __init__(self):
        self.m_nCount  = 0
        self.m_List = []
        self.m_lstFiltered = []
        self.m_nCountRaw = 0
        self.m_nSortCol  = ST_NAME
        self.m_bAscending = True
        #filter applied to this file list

        self.m_objFilter = FilterDesc()
        #print 'init'

    def Clear(self):
        # entspricht der Klasse (self.m_List)
        #TOMAKEBETTER: von List ableiten?
        #self.m_List.clear()
        self.m_List = []
        self.m_lstFiltered = []
        self.m_nCount    = 0
        self.m_nCountRaw = 0
        #print 'clr'

    #int VfsListing::Insert(const VfsItem &item)
    def Insert (self, item):
        #insert item in the list - no sorting

        self.m_List.append(item)
        #print 'Insert', self.m_List[0].m_strName, item
        self.m_nCountRaw += 1

        #if item matches filter add its index into the index list
        if (self.m_objFilter.Match(item)):
            self.m_lstFiltered.append(self.m_nCountRaw-1)
            self.m_nCount += 1

        #TOFIX
        return 0


    def GetCount(self):
        return self.m_nCount

    def GetCountRaw(self):
        return self.m_nCountRaw

    def GetAtRaw(self, nRawIdx):
        return self.m_List[nRawIdx]

    def GetAt(self, nIdx):
        assert nIdx < len(self.m_lstFiltered)
        nRawIdx = self.m_lstFiltered[nIdx]
        return self.GetAtRaw(nRawIdx)


    #FilterDesc &GetFilter(){ return m_objFilter; }
    def GetFilter(self):
        return self.m_objFilter

    #void SetFilter(const FilterDesc &filter){ m_objFilter = filter; }
    def SetFilter(self, filter):
        self.m_objFilter = filter

    #int VfsListing::FindItem(const char *szName, int nStart)
    def FindItem(self, szName, nStart = 0):
        if(nStart < 0):
            nStart = 0
        szName = szName.lower()
        #int nCount = size()
        for i in range (nStart, len(self.m_List)):
            #print i, szName, self.m_List[i].m_strName
            if self.m_List[i].m_strName.lower() == szName:
                return i
        #    if(operator [](i).GetName() == szName)
        #        #return list index
        #        return i;

        return -1

    def Sort(self):
        #print "sort"
        #    self.m_List.sort (lambda a, b: self.normcompare(a, b, a.m_strName.lower(), b.m_strName.lower()))
        if self.m_nSortCol == ST_EXT:
            self.m_List.sort (self.specialcompare)
            #self.m_List.sort (self.normcompare)
        else:
            self.m_List.sort (self.normcompare)

        #//rebuild filter list
        self.FilterList()


    # compare list first by extension, than by name (like spreadsheet) first order, second order
    def specialcompare(self, aname, bname):
        #dir oben
        #auf lower abfragen
        #print a.GetName()
        if not self.m_bAscending:
            cname = aname
            aname = bname
            bname = cname
        a1 = aname.m_strName [aname.m_nExtPos + 1:].lower()
        b1 = bname.m_strName [bname.m_nExtPos + 1:].lower()
        a2 = aname.m_strName [:aname.m_nExtPos].lower()
        b2 = bname.m_strName [:bname.m_nExtPos].lower()
        #print a1, a2, b1, b2
        #(a1,a2),(b1,b2) = a,b
        #m_nExtPos

        #// item ".." is ALWAYS on top of the list (no matter which column is being sorted)
        #//directory is ALWAYS placed before file item (no matter which column is being sorted)
        strUp = '..'
        if aname.GetName() == strUp:
            if self.m_bAscending:
                return -1
            else:
                return 1
        if bname.GetName() == strUp:
            if self.m_bAscending:
                return 1
            else:
                return -1
        #// item ".." is ALWAYS on top of the list (no matter which column is being sorted)
        #//directory is ALWAYS placed before file item (no matter which column is being sorted)
        if aname.IsDir() and not bname.IsDir():
            if self.m_bAscending:
                return -1
            else:
                return 1
        if not aname.IsDir() and bname.IsDir():
            if self.m_bAscending:
                return 1
            else:
                return -1


        if a1 < b1:
            #if self.m_bAscending:
            return -1
            #else:
            #    return 1
        if a1 == b1:
            erg = cmp(a2,b2)
            if cmp != 0:
                #if self.m_bAscending:
                if erg == 1:
                    erg = -1
                #    else:
                #        erg = 1
            return erg
        #if self.m_bAscending:
        return 1
        #else:
        #    return -1

    #(b, a, b.m_strName.lower(), a.m_strName.lower())
    #def normcompare(self, aname, bname, a, b):
    def normcompare(self, aname, bname):
        if not self.m_bAscending:
            cname = aname
            aname = bname
            bname = cname
        if self.m_nSortCol == ST_NAME or self.m_nSortCol == ST_NONE:
            a = aname.m_strName.lower()
            b = bname.m_strName.lower()
        elif self.m_nSortCol == ST_SIZE:
            a = aname.m_nSize
            b = bname.m_nSize
        elif self.m_nSortCol == ST_DATE:
            a = aname.m_nLastModDate
            b = bname.m_nLastModDate
        elif self.m_nSortCol == ST_ATTR:
            a = aname.m_nAttrib
            b = bname.m_nAttrib


        strUp = '..'
        if aname.GetName() == strUp:
            if self.m_bAscending:
                return -1
            else:
                return 1
        if bname.GetName() == strUp:
            if self.m_bAscending:
                return 1
            else:
                return -1

        #// item ".." is ALWAYS on top of the list (no matter which column is being sorted)
        #//directory is ALWAYS placed before file item (no matter which column is being sorted)
        if aname.IsDir() and not bname.IsDir():
            if self.m_bAscending:
                return -1
            else:
                return 1
        if not aname.IsDir() and bname.IsDir():
            if self.m_bAscending:
                return 1
            else:
                return -1

        if a == b or a > b:
            return 1
        else:
            return -1
            #return a < b
        #print "0"
        #return -1
    #//TOFIX add option (as in WC) that dirs are sorted by name/asc no matter what!
    #def SetSort(enum _SORT_COL nColumn, bool bAscending):
    def SetSort(self, nColumn, bAscending):
        #print 'set sort'
        self.m_nSortCol   = nColumn
        self.m_bAscending = bAscending

        #//using functor object instead of function to store sort preferences
        #cmp =  VfsComparator ()
        if ST_NONE == self.m_nSortCol:
            self.m_nSortCol =  ST_NAME
        #else:
        #    m_nColumn =  self.m_nSortCol

    def GetSortCol(self):
        return self.m_nSortCol

    def GetSortAsc(self):
        return self.m_bAscending

    #//case insensitive, partial string search (forward/backward search)
    #int  FindPartial(const char *szPartial, int nStart = 0, bool bForward = true);
    def FindPartial(self, szPartial, nStart = 0, bForward = True):
        nCount = self.GetCount()
        #print nStart, nCount
        nLen = len(szPartial)
        if(bForward):
            if nStart < 0:
                nStart = 0;
            for i in range (nStart, nCount):
                #print self.GetAt(i).GetName()[:nLen]
                #print szPartial
                if self.GetAt(i).GetName()[:nLen].lower() == szPartial.lower():
                #if(0 == self.GetAt(i).GetName().Left(nLen).CmpNoCase(szPartial))
                    #//return index (filtered list)
                    return i
        else:
            if nStart > 0:
                pass
                #for(int i=nStart; i>=0; i--)
                for i in range (nStart, -1, - 1):
                    if self.GetAt(i).GetName()[:nLen].lower() == szPartial.lower():
                #    if(0 == self.GetAt(i).GetName().Left(nLen).CmpNoCase(szPartial)):
                #        #//return index (filtered list)
                        return i;
        return -1

    #rebuild filter list
    def FilterList(self):
        self.m_nCount = 0
        self.m_lstFiltered = []

        for i in range (self.m_nCountRaw):
            #if(m_objFilter.Match(operator[](i)))
            if(self.m_objFilter.Match(self.m_List[i])):
                self.m_nCount += 1
                self.m_lstFiltered.append(i)
                #print 'append:', self.m_List[i], i

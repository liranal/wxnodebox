from WxUtil import *
from Globals import *
from FindInFile import *
import time
import fnmatch

class FilterDesc:
    def __init__ (self):
        self.m_nGroups = 0
        self.m_nShowAttr = 0
        self.m_nHideAttr = 0
        #array of strings
        self.m_lstNameShow=[]
        self.m_lstNameHide=[]
        self.m_strTitle = ''
        #//modify/created/last access
        self.m_nDateType = 0
        #//lower, upper, age
        self.m_dwDateFlags = 0
        self.m_dateFrom = 0
        self.m_dateUntil = 0
        #//0, 1, 2 => <, =, >
        self.m_nAgeOperator = 0
        #//0, 1, 2, 3 => hours, days, weeks, months, years
        self.m_nAgeAmount = 0
        self.m_nAgeUnit = 0
        self.m_finder = FindInFile ()
        self.m_nSizeOperator = 0
        #self.m_finder.Close()

    def Clear(self):
        self.m_nGroups = 0
        #TOFIX clear other data

    def AddGroupFlags(self, nFlags):
        self.m_nGroups |= nFlags
        #print self.m_nGroups

    def RemoveGroupFlags(self, nFlags):
        self.m_nGroups &= ~nFlags

    #void FilterDesc::SetNameGroup(const wxString &strNameShowPtrn, const wxString &strNameHidePtrn)
    def SetNameGroup (self, strNameShowPtrn, strNameHidePtrn):
        if (strNameShowPtrn == '' and strNameHidePtrn == ''):
            #remove name filtering
            #m_nGroups &= ~(FILTER_MatchName);
            self.m_nGroups = self.m_nGroups and not FILTER_MatchName;
        else:
            self.m_nGroups = self.m_nGroups or FILTER_MatchName;

            #tokenize each group of wildcard patterns into the list
            #print '1', strNameShowPtrn
            #print '2', strNameHidePtrn
            self.m_lstNameShow = Tokenize (strNameShowPtrn, self.m_lstNameShow)
            self.m_lstNameHide = Tokenize (strNameHidePtrn, self.m_lstNameHide)
            #print '1a', self.m_lstNameShow
            #print '2a', self.m_lstNameHide

    def FindNameWildcard(self, strWild, bShowPtrn = True):
        if bShowPtrn:
            nMax = len (self.m_lstNameShow)
        else:
            nMax = len (self.m_lstNameHide)
        for i in range (nMax):
            if bShowPtrn:
                if self.m_lstNameShow[i] == strWild:
                    return i
            else:
                if self.m_lstNameHide[i] == strWild:
                    return i
        return -1

    def AddToNameGroup(self, strWild, bShowPtrn = True):
        if self.FindNameWildcard(strWild, bShowPtrn) >= 0:
            #//wildcard pattern is already in the list
            return

        if bShowPtrn:
            self.m_lstNameShow.append(strWild)
        else:
            self.m_lstNameHide.append(strWild)

        #//TOFIX refresh flags
        self.AddGroupFlags(FILTER_MatchName)

    def RemoveFromNameGroup(self, strWild, bShowPtrn = True):
        nPos = self.FindNameWildcard(strWild, bShowPtrn)
        if nPos < 0:
            #//wildcard pattern is not in the list
            return

        if bShowPtrn:
            del self.m_lstNameShow [nPos]
        else:
            del self.m_lstNameHide [nPos]

        #//TOFIX refresh flags

    #void FilterDesc::SetContentsGroup(const wxString &strContents, bool bCaseSensitive)
    def SetContentsGroup(self, strContents, CaseSensitive = True):
        if(strContents == ''):
            #remove name filtering
            #self.m_nGroups = self.m_nGroups and not FILTER_MatchContents.__invert__()
            self.m_nGroups = self.m_nGroups & ~FILTER_MatchContents
        else:
            self.m_nGroups = self.m_nGroups | FILTER_MatchContents
            self.m_strContents    = strContents
            self.m_bCaseSensitive = CaseSensitive

            #init finder object
            self.m_finder.Clear()
            if(self.m_bCaseSensitive == False):
                self.m_finder.SetScanStyle(FS_CASE_INSENSITIVE)
            self.m_finder.SetSearchPattern(self.m_strContents)

    def SetSizeGroup(self, nSize, nRelation, nUnit):
        self.m_nGroups |= FILTER_MatchSize
        #//0, 1, 2, 3 => 0, <, =, >
        self.m_nSizeOperator = nRelation
        #print "size gr"
        #//kB, MB, ...?
        self.m_nSizeUnit     = nUnit
        self.m_nSizeAmount   = nSize

    def SetAttrGroup(self, nAttrShow, nAttrHide):
        self.m_nGroups |= FILTER_MatchAttr
        self.m_nShowAttr = nAttrShow
        self.m_nHideAttr = nAttrHide
        #print "1", nAttrHide

    def AddDateGroup(self, nSubflag, nAmount, nOperator, nUnit):
        self.m_nGroups |= FILTER_MatchDate
        self.m_dwDateFlags |= nSubflag

        if nSubflag & FILTER_DateFrom:
            self.m_dateFrom = nAmount
        elif nSubflag & FILTER_DateTo:
            self.m_dateUntil = nAmount
        elif nSubflag & FILTER_DateAge:
            self.m_nAgeAmount = nAmount
            self.m_nAgeOperator = nOperator
            self.m_nAgeUnit = nUnit

    #bool FilterDesc::Match(const VfsItem &item)
    def Match (self, item):
        #no filtering - empty filter
        #print 'in matching'
        if(0 == self.m_nGroups):
            return True
        if (self.MatchName(item) and self.MatchSize(item) and self.MatchDate(item)
                                 and self.MatchAttr(item) and self.MatchContents(item)):
            return True
        return False

    #bool FilterDesc::MatchName(const VfsItem &item) const
    def MatchName(self, item):
        #print self.m_nGroups, FILTER_MatchName
        #print item.GetName()
        if(self.m_nGroups & FILTER_MatchName):

            #check if directory skipping activated
            if(self.m_nGroups & FILTER_SkipDirMatch):
                if(item.IsDir()):
                    return True

            #skip matching '..' item
            if(item.IsDots()):
                return True

            #match file name agaings a list of wildcard patterns
            strItem = item.GetName()

            for i in range (len(self.m_lstNameHide)):
                if(self.MatchNameWild(strItem, self.m_lstNameHide[i])):
                    #matches one of the patterns that forbid display
                    return False

            bAnyMatch = False
            nCount = len(self.m_lstNameShow)
            if(nCount > 0):
                for i in range (nCount):
                    #print '2FILTER_MatchName', nCount, strItem, self.m_lstNameShow[i]
                    if(self.MatchNameWild(strItem, self.m_lstNameShow[i])):
                        bAnyMatch = True
                        break
                if(bAnyMatch == False):
                    #doesn't match any pattern required for display
                    return False
        return True

    #bool FilterDesc::MatchSize(const VfsItem &item) const
    def MatchSize(self, item):
        if(self.m_nGroups & FILTER_MatchSize):
            #directory is not matched by size
            if(item.IsDir() == False):
                #print "match size"
                nSizeInUnits = 0
                if self.m_nSizeUnit == 0:
                    #byte(s)
                    nSizeInUnits = item.m_nSize;
                elif self.m_nSizeUnit == 1:
                    #kB
                    nSizeInUnits = item.m_nSize / 1024
                elif self.m_nSizeUnit == 2:
                    #MB
                    nSizeInUnits = item.m_nSize / 1048576 #1024*1024
                elif self.m_nSizeUnit == 3:
                    #GB
                    nSizeInUnits = item.m_nSize / 1073741824 #1024*1024*1024

                #print self.nSizeOperator, nSizeInUnits, self.m_nSizeAmount
                if self.m_nSizeOperator == 0:
                    # <
                    if(nSizeInUnits >= self.m_nSizeAmount):
                        return False
                elif self.m_nSizeOperator == 1:
                    # =
                    if(nSizeInUnits != self.m_nSizeAmount):
                        return False
                elif self.m_nSizeOperator == 2:
                    # >
                    if(nSizeInUnits <= self.m_nSizeAmount):
                        return False
        return True

    #bool FilterDesc::MatchDate(const VfsItem &item) const
    def MatchDate(self, item):
        if(self.m_nGroups and FILTER_MatchDate):
            #//TOFIX support for different date times; if other not available use modified time
            #//      int m_nDateType;        //modify/created/last access
            if self.m_dwDateFlags & FILTER_DateFrom:
                if item.m_nLastModDate < self.m_dateFrom:
                    return False

            if self.m_dwDateFlags & FILTER_DateTo:
                if item.m_nLastModDate > self.m_dateUntil:
                    return False

            if self.m_dwDateFlags & FILTER_DateAge:
                #//calculate difference of current time and item time
                spanSec = time.time() - item.m_nLastModDate
                timeSpan = wxTimeSpan (0, 0, int (spanSec), 0)

                nAmountInUnits = 0
                #//hours
                if self.m_nAgeUnit == 0:
                    nAmountInUnits = timeSpan.GetHours()
                #//days
                elif self.m_nAgeUnit == 1:
                    nAmountInUnits = timeSpan.GetDays()
                #//week
                elif self.m_nAgeUnit == 2:
                    nAmountInUnits = timeSpan.GetWeeks()
                #//months
                #//TOFIX approximated? - use dates directly instead of span
                elif self.m_nAgeUnit == 3:
                    nAmountInUnits = timeSpan.GetWeeks() / 4
                #//years
                #//TOFIX approximated? - use dates directly instead of span
                elif self.m_nAgeUnit == 4:
                    nAmountInUnits = timeSpan.GetDays() / 365

                #//<
                if self.m_nAgeOperator == 0:
                    if nAmountInUnits >= self.m_nAgeAmount:
                        return False
                #//=
                elif self.m_nAgeOperator == 1:
                    if nAmountInUnits != self.m_nAgeAmount:
                        return False
                #//>
                elif self.m_nAgeOperator == 2:
                    if nAmountInUnits <= self.m_nAgeAmount:
                        return False
        return True

    #bool FilterDesc::MatchAttr(const VfsItem &item) const
    def MatchAttr(self, item):
        if self.m_nGroups & FILTER_MatchAttr:
            #//ensure all 'must have' attributes exist
            if(self.m_nShowAttr != (item.m_nAttrib & self.m_nShowAttr)):
                return False

            #//ensure no 'must NOT have' attributes exist
            if(0 != (item.m_nAttrib & self.m_nHideAttr)):
                return False

        return True

    def MatchContents(self, item):
        #//grep file for given contents
        #//TOFIX only for local files (Vfs_Local)!!!
        if self.m_nGroups & FILTER_MatchContents:
            #//if(m_lstContents.size() > 0)
            if self.m_strContents != "":
                #//NOTE: directory does not have text content
                if(item.IsDir()):
                    return False
                path = item.m_strPath
                if not (path [-1] == '/' or path [-1] == '\\'):
                    path += '/'
                if self.m_finder.SetScanFile (path + item.GetName()):
                    nPos = self.m_finder.Search()
                    self.m_finder.Close()
                    return -1 != nPos
                else:
                    return False
        return True

    #wxString FilterDesc::GetDescription()
    def GetDescription(self):
        #//TOFIX define filter string description (must not be too long - used in selection info contrl)
        if(self.m_strTitle == ''):
            return self.m_strTitle
        else:
            return _("Untitled")
            '''
            /*wxString strResult;
            if(m_nGroups & FILTER_MatchName){
                strResult += self.m_lstNameShow;
            }

            //TOFIX other marked with '...'
            return strResult;
            */
            '''

    def MatchNameWild(self, strName, strWild):
        #NOTE: matching filename against pattern list
        #(previously tokenized using ';' divider)
        #ifdef __WXMSW__
        #return fnmatch(strWild.c_str(), strName.c_str(), false, true);
        #print strName, strWild
        return fnmatch.fnmatch(string, pattern)
        #else
        #linuxTODO
            #return fnmatchcasefnmatch(strWild.c_str(), strName.c_str(), true, false);
            #return fnmatchcase(string, pattern)
        #endif

    def GetAttrShow(self):
        #//"must have" attributes
        return self.m_nShowAttr

    def GetAttrHide(self):
        #//"must not have" attributes
        return self.m_nHideAttr

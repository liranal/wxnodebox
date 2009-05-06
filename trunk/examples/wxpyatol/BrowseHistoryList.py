class BrowseHistoryList:
    def __init__(self):
        self.nMaxHistorySize = 20
        self.m_lstForward = []
        self.m_lstBackward = []
        self.m_strCurrent = ''

    def Clear(self):
        self.m_lstForward = []
        self.m_lstBackward = []
        self.m_strCurrent = ''

    def Push(self, szPath):
        strNew = szPath

        #if path valid and new
        if(strNew != '' and strNew != self.m_strCurrent):
            if(self.m_strCurrent != ''):
                self.m_lstBackward.append(self.m_strCurrent)

            #keep maximal length of history list
            if(len (self.m_lstBackward) > self.nMaxHistorySize):
                del self.m_lstBackward[0]

            self.m_strCurrent = szPath
            self.m_lstForward = []

    def CanMovePrev(self):
        return len (self.m_lstBackward) > 0

    def CanMoveNext(self):
        return len (self.m_lstForward) > 0

    def MovePrev(self):
        nSizeBackward = len (self.m_lstBackward)
        if(nSizeBackward>0):
            strPath = self.m_lstBackward[nSizeBackward-1]
            #backward path is now mowed forward
            self.m_lstBackward.pop()
            self.m_lstForward.append(self.m_strCurrent)
            self.m_strCurrent = strPath
            return strPath
        return ''

    def MoveNext(self):
        nSizeForward = len (self.m_lstForward)
        if(nSizeForward>0):
            strPath = self.m_lstForward[nSizeForward-1]
            self.m_lstForward.pop()
            self.m_lstBackward.append(self.m_strCurrent)
            self.m_strCurrent = strPath
            return strPath
        return ''

    def Move(self, nSteps, bBackwards):
        for i in range(nSteps):
            if(bBackwards):
                self.MovePrev()
            else:
                self.MoveNext()


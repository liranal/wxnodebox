from Globals import *
#//possible find styles
BUF_SIZE = 8*1024

class FindInFile:
    def __init__(self):
    #//TOFIX Get... functions, more styles?, debug timing

    #long Search(long nStartPos = 0);    //tofix int64

        self.m_dwStyle = 0

        #const _BYTE *self.m_pszPattern = ""
        self.m_pszPattern = ""
        self.m_nPtrnSize = 0
        #self.m_pszBlock = ""
        #self.m_nBlkSize = 0

        self.m_pFile = None
        #FILE    *selfm_pFile;
        #//file search buffer size
        self.m_shift = []



    def SetScanStyle(self, dwStyle):
        #//NOTE: you should NOT change style once the pattern is set
        #//      (since that functions used current style setting)
        #//ASSERT(NULL == m_pszPattern && 0 == self.m_nPtrnSize);
        self.m_dwStyle |= dwStyle

    #def SetSearchPattern(self, szText):
    #    self.m_pszPattern = szText
    #    #//TOFIX if NULL
    #    self.m_nPtrnSize  = len(szText)
    #    self.BuildShiftTable()

    def SetSearchPattern(self, szText, nSize = 0):
        self.m_pszPattern = szText
        if nSize != 0:
            self.m_nPtrnSize  = nSize
        else:
            self.m_nPtrnSize  = len(szText)
        self.BuildShiftTable();

    #// To ensure the pattern is not inadvertently chopped up,
    #// BMG_Patlen - 1 bytes is always moved to the start of the buffer
    #/ The next time we fill the buffer we fill it with BUFSIZ - (BMG_Patlen - 1) bytes.
    def SetScanFile(self, szFile):
        self.Close();

        strName = szFile
        #//m_mapFile.MapFile(strName, TRUE); //read-only
        self.m_pFile = open(szFile, "rb")

        #//m_pszBlock    = (const _BYTE *)m_mapFile.Open();
        #//m_nBlkSize    = m_mapFile.GetLength();

        return (None != self.m_pFile)

    def SetScanBuffer(self, szBuffer, nSize):
        self.Close()

        #self.m_pszBlock  = szBuffer
        #self.m_nBlkSize  = nSize
        #return self.m_pszBlock != NULL and m_nBlkSize > 0

    #//tofix int64
    def SearchMem(self, nStartPos):
        #//  Size of matched part
        match_size = 0
        #// Base of match of pattern
        match_base = ""
        #// Point within current match
        match_ptr  = ""
        #//  Last potiental match point
        limit      = ""
        #//  Concrete pointer to block data
        #block   = self.m_pszBlock
        #//  Concrete pointer to search value
        pattern = self.m_pszPattern

        #//ASSERT (block);                 //  Expect non-NULL pointers, but
        #//ASSERT (pattern);               //  fail gracefully if not debugging

        #if block == "" or pattern == "":
            #print "ret1"
        #    return -1

        #//  Pattern must be smaller or equal in size to string
        #if self.m_nBlkSize < self.m_nPtrnSize:
        #    #//  Otherwise it's not found
             #print "ret2"
        #    return -1

        #//  Empty patterns match at start
        if self.m_nPtrnSize == 0:
            #print "ret3"
            return 0

        #//  Search for the block, each time jumping up by the amount
        #//  computed in the shift table

        #limit = block + (m_nBlkSize - self.m_nPtrnSize + 1)
        #//ASSERT (limit > block);

        #TODO
        #//NOTE: two versions: case sensitive and case insensitive version
        if self.m_dwStyle & FS_CASE_INSENSITIVE:
            #for (match_base = block;
            #    match_base < limit;
            #    match_base += self.m_shift [ tolower(*(match_base + self.m_nPtrnSize)) ])
                match_ptr  = match_base
                match_size = 0

                #// Compare pattern until it all matches, or we find a difference
                ind = 0
                base_ind = 0
                while base_ind < len (self.pBuffer):
                # suche bis am ende sonst neu und index erhoehen

                    while ((base_ind + ind ) < len (self.pBuffer)) and (ind < len (pattern))\
                        and self.pBuffer[base_ind+ ind].lower() == pattern[ind].lower():
                    #while ((base_ind + ind ) < len (self.pBuffer)):
                    #    i = self.pBuffer[base_ind+ ind].lower()
                    #    u = pattern[ind].lower()
                        ind += 1
                        if ind >= len (pattern):
                            #print "ret"
                            return ind  # oder sonstwas, aber nicht -1

                        #print ind
                    base_ind += 1
                    ind = 0
                    #print len (self.pBuffer), base_ind, ind
                    #//ASSERT (match_size <= self.m_nPtrnSize && match_ptr == (match_base + match_size));
                    #// If we found a match, return the start address
                    #if (match_size >= self.m_nPtrnSize):
                        #print "ret6"
                    #    return (match_base - self.m_pszBlock)

        else:
            #TODO: same as above with not hte whole file, but pieces
                ind = 0
                base_ind = 0
                while base_ind < len (self.pBuffer):
                # suche bis am ende sonst neu und index erhoehen

                    while ((base_ind + ind ) < len (self.pBuffer)) and (ind < len (pattern))\
                        and self.pBuffer[base_ind+ ind] == pattern[ind]:
                    #while ((base_ind + ind ) < len (self.pBuffer)):
                    #    i = self.pBuffer[base_ind+ ind].lower()
                    #    u = pattern[ind].lower()
                        ind += 1
                        if ind >= len (pattern):
                            #print "ret"
                            return ind  # oder sonstwas, aber nicht -1

                        #print ind
                    base_ind += 1
                    ind = 0

        #// Found nothing
        return -1;

    def BuildShiftTable(self):
        #//  Build the shift table unless we're continuing a previous search

        #//  The shift table determines how far to shift before trying to match
        #//  again, if a match at this point fails.  If the byte after where the
        #//  end of our pattern falls is not in our pattern, then we start to
        #//  match again after that byte; otherwise we line up the last occurence
        #//  of that byte in our pattern under that byte, and try match again.
        self.m_shift = []
        for i in range (256):
            self.m_shift.append (self.m_nPtrnSize + 1)

        if self.m_dwStyle & FS_CASE_INSENSITIVE:
            #//case insensitive version
            for i in range (self.m_nPtrnSize):
                pass
                #self.m_shift[(_BYTE) tolower(m_pszPattern[i])] = self.m_nPtrnSize - i;
        else:
            #//case sensitive version
            for i in range (self.m_nPtrnSize):
                pass
                #self.m_shift[(_BYTE) m_pszPattern[i]] = self.m_nPtrnSize - i;

    def Close(self):
        #//m_mapFile.Close();
        if self.m_pFile != None:
            self.m_pFile.close()
            self.m_pFile = None

    def Clear(self):
        self.m_pszPattern = ""
        self.m_nPtrnSize  = 0
        #self.m_pszBlock   = ""
        #self.m_nBlkSize   = 0
        self.Close()

    #//TOFIX progress, abort, test, ...
    def SearchFile(self, nStartPos):
        #//ASSERT(NULL == m_pFile);
        if(None == self.m_pFile):
            return -1

        #_BYTE *pBuffer = new _BYTE [BUF_SIZE];
        #if(pBuffer):
        if 1:
            nSrcFile = self.m_pFile
            if nStartPos > 0:
                if -1 != nSrcFile.seek (nStartPos, SEEK_SET):
                    #// failed to set initial position
                    return -1

            #pBuffer = nSrcFile.read(BUF_SIZE)
            #TODO:  1 byte mindestens(?)
            self.pBuffer = nSrcFile.read()
            leng = len (self.pBuffer)
            #print leng, self.pBuffer [leng -1], self.pBuffer [leng -2]
            #TODO: is this correct?
            #self.m_pszBlock = pBuffer;
            #while nRead > 0:
            # TODO: len mit mit read buffer size vergleichen (nicht drueberlesen, sonst gibt es ''
            # gleich alles?
            #while pBuffer != '':
            #    self.m_nBlkSize = nRead

                #//parse buffer
            #print "1"
            nPos = self.SearchMem(0)
            #print "2"
            return nPos
            '''
            if nPos > -1:
                #delete [] pBuffer;
                #//something found
                return nPos;

                #//keep last N chars in the buffer
                #TODO
                #memmove(pBuffer, pBuffer + self.m_nPtrnSize, self.m_nPtrnSize);

                #//refill the buffer
                #nRead = read(pBuffer + self.m_nPtrnSize, 1, BUF_SIZE - self.m_nPtrnSize, self.m_pFile)
                self.pBuffer = nSrcFile.read(BUF_SIZE)
            #    if pBuffer > 0:
            #        nRead += self.m_nPtrnSize;
            '''
        return -1

    def Search(self, nStartPos = 0):
        if self.m_pFile:
            return self.SearchFile(nStartPos)
        else:
            return self.SearchMem(nStartPos)


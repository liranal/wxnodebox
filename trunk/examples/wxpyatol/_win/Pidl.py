class PIDL:
    def __init__(self):
        self.m_sfDesktop = 0

    def GetFromPath(self, pszPath):
        if 0 == self.m_sfDesktop:
            return 0
            #TODO: insert code
        #//
        #// Now convert the path to a Unicode string
        #// as required by ParseDisplayName
        #//
        #TODO: unicode
        olePath = pszPath
        pidl = 0
        #TODO: insert code:ParseDisplayName (what does it do)
        #hr = self.m_sfDesktop.ParseDisplayName(
        #        NULL,NULL,olePath,chEaten,pidl,NULL)
        #if( FAILED(hr) )
        #    return NULL;

        return pidl



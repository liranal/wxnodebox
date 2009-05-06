from Globals import *
from WxUtil import *


class VfsItem:
    def __init__(self):
        self.m_strName =''
        self.m_nSize     = -1
        self.m_nExtPos   = -1
        self.m_nLastModDate  = 0
        self.m_nAttrib   = 0
        #self.m_nIconIdx    = -1
        self.m_nIconIdx    = 0


#>>> from time import gmtime, strftime
#>>> strftime('%a, %d %b %Y %H:%M:%S +0000', gmtime())
#'Thu, 28 Jun 2001 14:17:15 +0000'

    def IsDir(self):
        return self.m_nAttrib & ATTR_DIR

    def IsDots(self):
        if self.IsDir():
            #TOFIX speedup using static const '.'/'..'
            if (self.m_strName == '.' or  self.m_strName == '..'):
                return True
        return False

    def GetName(self):
        return self.m_strName

    def GetTitle(self):
        if self.m_nExtPos > 0:
            return self.m_strName[:self.m_nExtPos]
        return self.m_strName

    def GetExt(self):
        if(self.m_nExtPos > 0):
            #//ext without dot
            return self.m_strName[self.m_nExtPos+1:]
        return ''

    def CalcExt(self):
        #//calculate start of extension within item name
        if self.IsDir():
            #//dirs don't have extensions
            self.m_nExtPos = -1
        else:
            #//find last '.' character in the name

            #TODO: is right?
            #m_nExtPos = m_strName.Find('.', TRUE);
            self.m_nExtPos = m_strName.find('.')

            #//when item starts with single . it is not counted as extension
            #//(since then item would have no name)
            if self.m_nExtPos == 0:
                self.m_nExtPos = -1

    def GetSize(self):
        if self.IsDir() and self.m_nSize < 0:
            return _("<DIR>")
        else:
            return FormatSize (self.m_nSize)

    #wxString VfsItem::GetDate() const
    def GetDate(self):
        import time
        #print time.gmtime(self.m_nLastModDate)
        return time.strftime ('%Y.%m.%d %H:%M', time.gmtime(self.m_nLastModDate))
        #pass
        #struct tm *pTM = localtime( &m_nLastModDate );
        #return wxString::Format('%04d.%02d.%02d %02d:%02d', 1900+pTM->tm_year, 1+pTM->tm_mon, pTM->tm_mday, pTM->tm_hour, pTM->tm_min);

    def GetAttr(self):
        #if(self.m_nAttrib & ATTR_UNIX):
        #else
        strAttr = ''
        if(self.m_nAttrib & ATTR_RONLY):
            strAttr += 'r'
        else:
            strAttr += '-'
        if(self.m_nAttrib & ATTR_ARCH):
            strAttr += 'a'
        else:
            strAttr += '-'
        if(self.m_nAttrib & ATTR_HIDDEN):
            strAttr += 'h'
        else:
            strAttr += '-'
        if (self.m_nAttrib & ATTR_SYSTEM):
            strAttr += 's'
        else:
            strAttr += '-'

        '''
        wxString VfsItem::GetAttr() const
        {
            wxString strAttr;

            if(m_nAttrib & ATTR_UNIX)
            {
                //calculate first letter
                if(m_nAttrib & ATTR_DIR)
                    strAttr.Append('d');
                else if(m_nAttrib & ATTR_LINK)
                    strAttr.Append('l');
                else
                    strAttr.Append('-');

                //calculate other letters
                if(m_nAttrib & ATTR_R_USR)  strAttr.Append('r'); else  strAttr.Append('-');
                if(m_nAttrib & ATTR_W_USR)  strAttr.Append('w'); else  strAttr.Append('-');
                if(m_nAttrib & ATTR_X_USR)  strAttr.Append('x'); else  strAttr.Append('-');

                if(m_nAttrib & ATTR_R_GRP)  strAttr.Append('r'); else  strAttr.Append('-');
                if(m_nAttrib & ATTR_W_GRP)  strAttr.Append('w'); else  strAttr.Append('-');
                if(m_nAttrib & ATTR_X_GRP)  strAttr.Append('x'); else  strAttr.Append('-');

                if(m_nAttrib & ATTR_R_OTH)  strAttr.Append('r'); else  strAttr.Append('-');
                if(m_nAttrib & ATTR_W_OTH)  strAttr.Append('w'); else  strAttr.Append('-');
                if(m_nAttrib & ATTR_X_OTH)  strAttr.Append('x'); else  strAttr.Append('-');
            }
            else
            {
                #if(m_nAttrib & ATTR_RONLY)  strAttr.Append('r'); else  strAttr.Append('-');
                #if(m_nAttrib & ATTR_ARCH)   strAttr.Append('a'); else  strAttr.Append('-');
                #if(m_nAttrib & ATTR_HIDDEN) strAttr.Append('h'); else  strAttr.Append('-');
                #if(m_nAttrib & ATTR_SYSTEM) strAttr.Append('s'); else  strAttr.Append('-');
            }

        '''
        return strAttr;

    def SetName(self, szName):
        self.m_strName = szName
        self.CalcExt()

    def GetPath(self):
        return self.m_strPath

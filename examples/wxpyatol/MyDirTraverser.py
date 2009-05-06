from wxPython.wx import *
import os
from VfsSelection import *
import win32file
import win32con
#from VfsSelectionItem import *

#helper class for directory traversing
class MyDirTraverser:
    def __init__ (self, VfsList, strDir):

        #self.lstData = traverse

        path = strDir
        dirlist = os.listdir(path)
        dirListLength = len(dirlist)

        for i in range(dirListLength):
            fullname = os.path.join(path, dirlist[i])
            #print path
            #print fullname
            #u = os.stat(path)
            #print u
            item = VfsSelectionItem ()
            #name = lis[i]
            #print lis, name
            #print lis[i]
            #print os.path.getsize(fullname)
            item.m_strName = dirlist[i]
            item.m_nExtPos = item.m_strName.rfind ('.')
            item.m_nSize = os.path.getsize(fullname)
            #print 'size:', i, item.m_nSize
            item.m_nLastModDate = os.path.getmtime(fullname)
            #win32file wxpython nicht enthalten: FILE_ATTRIBUTE_DIRECTORY
            #if os.path.isdir(fullname):
            #    item.m_nAttrib  = ATTR_DIR
            # //convert attributes to portable flags
            #ifdef __WXMSW__
            dwAttr = win32file.GetFileAttributes(fullname)
            if dwAttr != -1:
                #//#define ATTR_LINK 0x0004
                if(dwAttr & win32con.FILE_ATTRIBUTE_DIRECTORY):
                    item.m_nAttrib |= ATTR_DIR;
                    item.m_nExtPos = -1
                if(dwAttr & win32con.FILE_ATTRIBUTE_ARCHIVE):
                    item.m_nAttrib |= ATTR_ARCH
                if(dwAttr & win32con.FILE_ATTRIBUTE_HIDDEN):
                    item.m_nAttrib |= ATTR_HIDDEN
                if(dwAttr & win32con.FILE_ATTRIBUTE_READONLY):
                    item.m_nAttrib |= ATTR_RONLY
                if(dwAttr & win32con.FILE_ATTRIBUTE_SYSTEM):
                    item.m_nAttrib |= ATTR_SYSTEM

            '''
            #else
                    item.m_nAttrib |= ATTR_UNIX;
                    if(st.st_mode & S_IFDIR)    item.m_nAttrib |= ATTR_DIR;
                    if(S_ISLNK(st.st_mode))     item.m_nAttrib |= ATTR_LINK;

                    if(st.st_mode & S_IRUSR)    item.m_nAttrib |= ATTR_R_USR;
                    if(st.st_mode & S_IWUSR)    item.m_nAttrib |= ATTR_W_USR;
                    if(st.st_mode & S_IXUSR)    item.m_nAttrib |= ATTR_X_USR;
                    if(st.st_mode & S_IRGRP)    item.m_nAttrib |= ATTR_R_GRP;
                    if(st.st_mode & S_IWGRP)    item.m_nAttrib |= ATTR_W_GRP;
                    if(st.st_mode & S_IXGRP)    item.m_nAttrib |= ATTR_X_GRP;
                    if(st.st_mode & S_IROTH)    item.m_nAttrib |= ATTR_R_OTH;
                    if(st.st_mode & S_IWOTH)    item.m_nAttrib |= ATTR_W_OTH;
                    if(st.st_mode & S_IXOTH)    item.m_nAttrib |= ATTR_X_OTH;
            #endif
            '''
            #item.CalcExt();
            VfsList.Insert(item)
      #return list


        #//remove path from file name
        #wxString strExt;
        #wxFileName::SplitPath(filename, NULL, NULL, &item.m_strName, &strExt );
        #if(strExt.Length() > 0){
        #    item.m_strName += '.';
        #    item.m_strName += strExt;
        #}


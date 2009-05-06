from VfsListing import *
from Globals import *
from PathName import *

class Vfs:
    def __init__(self):
        self.m_pProgress = None
        self.m_nType = VFS_UNKNOVN
        self.m_strCurDir = ''

    def GetDir(self):
        return self.m_strCurDir

    def GetPathTitle(self):
        #for display purposes
        return self.GetDir()

    def GetType(self):
        return self.m_nType

    #def ExpandSelection(VfsSelection &sel, bool &bAbort)
    def ExpandSelection(self, sel, bAbort):
        self.ExpandTree(sel.m_lstRootItems, bAbort)

    #void Vfs::ExpandTree(std::vector<VfsSelectionItem> &list, bool &bAbort)
    def ExpandTree(self, list, bAbort):
        nSize = len (list)

        #print nSize
        for i in range(nSize):
            if(list[i].IsDir() and not list[i].IsDots()):
                strPath = self.GetDir()
                path_instance = PathName ()
                #//TOFIX it is very important to use '//' for SFTP sites!!!
                path_instance.EnsureTerminated(strPath, '/')

                strNewPath  = strPath
                #print "b", strNewPath
                #print list[i].GetName()
                #//TOFIX it is very important to use '//' for SFTP sites!!!
                cLast = strNewPath [-1]
                if(not (cLast == '\\' or cLast == '/')):
                    strNewPath += '/'
                strNewPath += list[i].GetName()

                if(self.SetDir(strNewPath)):
                    listing = VfsListing ()
                    #//TOFIX listing without '..' mode
                    self.ListDir(listing, bAbort)

                    #//add all listed/filtered files to the subtree
                    for j in range(listing.GetCount()):
                        if(not listing.GetAt(j).IsDots()):
                            list[i].m_lstSubItems.append(listing.GetAt(j))

                    #//recursively expand this new list
                    self.ExpandTree(list[i].m_lstSubItems, bAbort)

                    #//restore path
                    self.SetDir(strPath)
                else:
                    #//WXTRACE('WARNING: failed to set directory\n');
                    #//WXASSERT(FALSE);
                    pass

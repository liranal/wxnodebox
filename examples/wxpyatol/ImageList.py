from wxPython.wx import *
import win32con
from ctypes import *
from Globals import *
import win32file

class CImageList (wxImageList):
#    pass
    def __init__(self):
        wxImageList.__init__ (self, 16, 16)

        ##ifdef __WXMSW__
        #//attach system image list (small icons) to our own list
        dwFlags = SHGFI_USEFILEATTRIBUTES | SHGFI_SYSICONINDEX | SHGFI_SMALLICON
        #// Load the image list - use an arbitrary file extension for the
        #// call to SHGetFileInfo (we don't want to touch the disk, so use
        #// FILE_ATTRIBUTE_NORMAL && SHGFI_USEFILEATTRIBUTES).

        #self.m_hImageList = windll.shell32.SHGetFileInfo('.txt', win32file.FILE_ATTRIBUTE_NORMAL, byref(shfileinfo), sizeof(shfileinfo), dwFlags)
        #self.Add (windll.shell32.SHGetFileInfo('.txt', win32file.FILE_ATTRIBUTE_NORMAL, byref(shfileinfo), sizeof(shfileinfo), dwFlags))
        #print m_hImageList, type (m_hImageList)
        '''

        #print hex(shfileinfo.dwAttributes)
        #print repr(shfileinfo.szDisplayName)
        #print repr(shfileinfo.szTypeName)


        flags = SHGFI_DISPLAYNAME | SHGFI_TYPENAME | SHGFI_ATTRIBUTES
        #flags = SHGFI_USEFILEATTRIBUTES|SHGFI_SYSICONINDEX|SHGFI_SMALLICON
        #print windll.shell32.SHGetFileInfo(sys.executable,
        #                                0,
        #                                byref(shfileinfo),
        #                                sizeof(shfileinfo),
        #                                flags)

        #print hex(shfileinfo.dwAttributes)
        #print repr(shfileinfo.szDisplayName)
        #print repr(shfileinfo.szTypeName)
        '''
        #
        #    // Make the background colour transparent, works better for lists etc.
        #    //rpImageList->SetBkColor( CLR_NONE );
        ##else
        #wxImageList.Create(16,16)
        #u = wxBitmap('xpm/up_dir.xpm')
        # aus unerfindlichen Gruenden ist das nicht gegangen
        #i = wxIcon('xpm/up_dir.xpm', wxBITMAP_TYPE_XPM)
        #print u.GetHeight(), u.GetWidth(), u.GetDepth()
        self.Add(wxBitmap('xpm/up_dir.xpm'))
        self.Add(wxBitmap('xpm/folder.xpm'))
        self.Add(wxBitmap('xpm/folder.xpm'))
        self.Add(wxBitmap('xpm/folder.xpm'))
        self.Add(wxBitmap('xpm/folder.xpm'))
        self.Add(wxBitmap('xpm/folder.xpm'))
        self.Add(wxBitmap('xpm/folder.xpm'))
        self.Add(wxBitmap('xpm/folder.xpm'))
        self.Add(wxBitmap('xpm/folder.xpm'))
        self.Add(wxBitmap('xpm/blank.xpm'))
        ##endif

# TODO: CalcIconIndex
    def CalcIconIndex (self, item):
        #item.m_nIconIdx = 1
        #return
        #ifdef __WXMSW__
        dwFlags = SHGFI_USEFILEATTRIBUTES | SHGFI_SYSICONINDEX | SHGFI_SMALLICON | SHGFI_ICON

        if item.IsDir():
            #TODO: hier directory atttrib holen
            windll.shell32.SHGetFileInfo (item.GetName(), win32con.FILE_ATTRIBUTE_DIRECTORY, byref(shfileinfo), sizeof(shfileinfo), dwFlags)
        else:
            windll.shell32.SHGetFileInfo (item.GetName(), win32con.FILE_ATTRIBUTE_NORMAL, byref(shfileinfo), sizeof(shfileinfo), dwFlags)
            #SHGetFileInfo(item.GetName(), win32con.FILE_ATTRIBUTE_NORMAL, &sfi, sizeof(SHFILEINFO), dwFlags);
        item.m_nIconIdx = shfileinfo.iIcon
        '''
        #else
            if(item.IsDir())
            {
                static const wxString strUpDir = wxString('..');    //speedup using const
                if(item.GetName() == strUpDir)
                    item.m_nIconIdx = 0;    //up-dir icon
                else
                    item.m_nIconIdx = 1;    //directory icon
            }
            else
                item.m_nIconIdx = 2;    //file icon
        #endif
        '''

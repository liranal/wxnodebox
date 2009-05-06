from wxPython.wx import *
from FileListCtrl import *
from SelectionInfoCtrl import *
from PathInfoCtrl import *
import win32api
from PopupMenu import *
from VfsManager import *


if 1:
    ID_DRIVE_BUTTON  = 101
    ID_ROOT_BUTTON   = 102
    ID_PARENT_BUTTON = 103


class FilePanel (wxWindow):

    def __init__ (self, pParent):
        wxWindow.__init__ (self, pParent, -1, wxPoint( 0, 0 ), wxDefaultSize, wxWANTS_CHARS|wxCLIP_CHILDREN)
        self.Initialize ()
        EVT_SIZE(self, self.OnSize)
        EVT_SET_FOCUS(self, self.OnSetFocus)
        EVT_BUTTON(self, ID_DRIVE_BUTTON,  self.OnDriveButton)
        EVT_BUTTON(self, ID_ROOT_BUTTON,  self.OnRootButton)
        EVT_BUTTON(self, ID_PARENT_BUTTON, self.OnParentButton)
        #EVT_MENU_RANGE(self, 1, 100, self.OnDriveMenu)
        EVT_ERASE_BACKGROUND(self, self.OnEraseBkg)
        EVT_CHAR(self, self.OnChar)

    def GetSelection (self, sel):
        return self.m_pFileList.GetSelection(sel)

    def Activate (self, bActive = true):

        #check if child window valid
        if(self.m_wndPathInfo.IsBeingDeleted()):
            return
        pFrame = self.GetParent().GetParent()
        assert pFrame != NULL
        if(bActive):
            pFrame.m_pActivePanel = self

            #if(self.FindFocus() != self.m_pFileList):
            if(wxWindow_FindFocus() != self.m_pFileList):
                #print "hi"
                self.m_pFileList.SetFocus()

            self.m_wndPathInfo.SetBackgroundColour(wxColour(10,10,128))
            self.m_wndPathInfo.SetForegroundColour(wxColour(255,255,255))

            #deactivate other panel
            pOther = pFrame.GetInactivePanel()
            assert (pOther!= self)
            if(pOther):
                pOther.Activate(false)

        else:
            self.m_wndPathInfo.SetBackgroundColour(wxLIGHT_GREY);
            self.m_wndPathInfo.SetForegroundColour(wxColour(0,0,0));

        self.m_wndPathInfo.Refresh()

    def OnDriveButton (self, event):  #drive button handler
        #//show popup menu with all available drives/mount points
        menu = CPopupMenu ()

        #ifdef __WXMSW__
        dwDrives = win32api.GetLogicalDrives ()
        #print dwDrives
        #dwDrives   = ::GetLogicalDrives();
        nDriveIdx  = 0;

        while(nDriveIdx < 26):
            if(dwDrives & 1):
                #TODO (linux): TOMAKEBETTER
                szDrive = chr(ord ('A') + nDriveIdx) + ':'
                #szDrive[0] = 'A' + chr (nDriveIdx)
                menu.Append (nDriveIdx+1, szDrive)
            nDriveIdx += 1
            dwDrives >>= 1
        #wxpython
        self.PopupMenuXY(menu, 0, 20)
        nID = menu.GetSelectedID()
        if nID > 0:
            szDrive = chr (ord('A:') + nID - 1)

            #//make sure we have proper VFS
            while (self.m_pFileList.m_pVfs.GetType() != Vfs_LOCAL):
                wxGetApp().GetFrame().g_VfsManager.VfsStackPop(m_pFileList)

            self.m_pFileList.SetDirectory(szDrive)

        #else
        #//TOFIX add mount points into the menu!
        #endif

    def OnSetFocus (self, event):
        self.Activate(true)

    def Initialize (self):                        # create and configure the panel
        self.m_pFileList = FileListCtrl (self)

        #create drive selection button
        self.m_objDriveBtn = wxBitmapButton (self, ID_DRIVE_BUTTON, wxBitmap('xpm/drive.xpm'), wxPoint(0,0), wxSize(20,20), wxNO_3D|wxBU_EXACTFIT|wxSIMPLE_BORDER)
        self.m_objRootBtn = wxBitmapButton (self, ID_ROOT_BUTTON,    wxBitmap('xpm/root.xpm'),  wxPoint(0,0), wxSize(20,20), wxNO_3D|wxBU_EXACTFIT|wxSIMPLE_BORDER);
        self.m_objUpBtn = wxBitmapButton (self, ID_PARENT_BUTTON,  wxBitmap('xpm/parent.xpm'), wxPoint(0,0), wxSize(20,20), wxNO_3D|wxBU_EXACTFIT|wxSIMPLE_BORDER);

        #nHeight = self.GetClientSize().GetHeight() (wxPython wird es noch nicht gesetzt)
        #nHeight = self.GetClientSize()
        self.m_wndPathInfo = PathInfoCtrl (self, 1, _("<Path>"), wxPoint(20,4), wxDefaultSize, wxALIGN_LEFT|wxST_NO_AUTORESIZE)
        #print 'height', nHeight
        #nHeight = 300
        #TOFIX: nHeight liefert 0 zurueck
        #self.m_wndStatInfo = StatInfoCtrl (self, 2, '<Stat>', wxPoint(0, nHeight-20), wxDefaultSize, wxALIGN_LEFT|wxST_NO_AUTORESIZE)  #below the list ctrl
        self.m_wndStatInfo = StatInfoCtrl (self, 2, '', wxPoint(0, 0), wxDefaultSize, wxALIGN_LEFT|wxST_NO_AUTORESIZE)  #below the list ctrl

        self.m_pFileList.m_pPathInfo = self.m_wndPathInfo
        self.m_pFileList.m_pStatInfo = self.m_wndStatInfo

    def OnSize (self, event):
        #print 'height', self.GetClientSize().GetHeight()
        nHeight = self.GetClientSize().GetHeight()
        nWidth  = self.GetClientSize().GetWidth()

        #self.m_wndPathInfo.SetSize(20, 4, nWidth-61, 14)
        #wxpython anders
        self.m_wndPathInfo.SetDimensions(20, 4, nWidth-61, 14)
        self.m_pFileList.SetDimensions(0, 20, nWidth-1, nHeight - 40)
        self.m_wndStatInfo.SetDimensions(0, nHeight-21, nWidth, 20)

        #wxWindows
        #self.m_objRootBtn.Move(nWidth-41, 0)
        #wxPython
        self.m_objRootBtn.MoveXY(nWidth-41, 0)
        self.m_objUpBtn  .MoveXY(nWidth-21, 0)

        self.m_pFileList.Refresh()

    def OnEraseBkg (self, event):
        event.Skip();

    #drive menu result handler
    '''
    def OnDriveMenu (self, event):
        #ifdef __WXMSW__
        szDrive = chr (ord('A') + event.GetId() - 1) + ':' + '\\'
        self.m_pFileList.SetDirectory(szDrive)
        #else
        #    wxMessageDialog dlg(this, wxString::Format('%d',event.m_id));
        #    dlg.ShowModal();
        #endif
    '''

    def OnRootButton (self, event):
        '''
        #print "onroot button"
        #print event
        #print
        #print event.GetString()
        #print event.GetSelection()
        #print event.GetInt()
        #print event.GetExtraLong()
        #print event.GetClientData()
        #print
        #print event.GetEventObject ()
        #print event.GetEventType ()
        #print event.GetId ()
        #print event.GetSkipped ()
        #print event.GetTimestamp ()
        '''
        evDummy = wxMenuEvent ()
        self.m_pFileList.OnRootDir(evDummy)

    def OnParentButton (self, event):
        evDummy = wxMenuEvent ()
        self.m_pFileList.OnUpDir(evDummy)

    def OnChar (self, event):
        #needed by command line to catch key press (skips splitter parent)
        self.GetParent().GetParent().ProcessEvent(event)

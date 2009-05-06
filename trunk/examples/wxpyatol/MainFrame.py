from wxPython.wx import *
from FilePanel import *
from ImageList import *
from VfsManager import *
from CommandLineCtrl import *
from AboutDlg import *
from FileSearchDlg import *
from OptionsDlg import *
from PathName import *
from VfsSelection import *
from VfsItem import *
from OpManager import *
from PluginManager import *
from CompressDlg import *
from WxUtil import *
from wxPython.lib import splashscreen
from OverwriteDlg import *
from DeleteDlg import *
import os
from GuiLanguage import *
#print GetExecutablePath()
#from globals import *
#import images

IDC_SPLITTER = 101
#gibt es in wxpython anscheinend nicht


if 1:
    def menuAdd(root, menu, name, desc, funct, id, kind=wxITEM_NORMAL):
        menu.Append(id, name, desc, kind)
        EVT_MENU(root, id, funct)


#print wxLANGUAGE_AFRIKAANS, wxLANGUAGE_GERMAN
class MainFrame(wxFrame):
    def __init__(self):
        wxFrame.__init__(self, None, -1, 'wxPyAtol', size=(600,480),
            style=wxDEFAULT_FRAME_STYLE|wxNO_FULL_REPAINT_ON_RESIZE)

        self.m_fSplitterPercent = 0.50;  #50 %

        self.m_wndSplitter = wxSplitterWindow(self, -1, wxDefaultPosition, wxDefaultSize, wxSP_BORDER)
        self.m_wndCommandLine = CommandLineCtrl (self)

        self.m_objOpManager = OpManager()

        self.g_Lang = GuiLanguage()

        self.wxMessageBoxCaptionStr = _("Message")

        #build toolbar
        ID_TOOLBAR = 1001
        style = wxTB_FLAT | wxTB_DOCKABLE | wxTB_HORIZONTAL
        pToolBar = self.CreateToolBar(style, ID_TOOLBAR)

        #//m_wndHistPrevBtn.Create(pToolBar, CMD_HISTORY_PREV_POPUP, wxBitmap(down_arrow_xpm), wxPoint(0,0), wxSize(20,20), wxNO_3D|wxSIMPLE_BORDER);
        #//m_wndHistNextBtn.Create(pToolBar, CMD_HISTORY_NEXT_POPUP, wxBitmap(down_arrow_xpm), wxPoint(0,0));
        #wxpython besonderheit
        pToolBar.AddTool(CMD_REFRESH, wxBitmap('xpm/refresh.xpm'), shortHelpString='Refresh listing')

        pToolBar.AddSeparator()
        pToolBar.AddTool(CMD_HISTORY_PREV, wxBitmap('xpm/left_arrow.xpm'), shortHelpString='Previous Directory')
        #//pToolBar->AddControl(&m_wndHistPrevBtn);
        #//pToolBar->AddTool(CMD_HISTORY_PREV_POPUP, _("Help"),  wxBitmap(down_arrow_xpm),   _("Help button"), wxITEM_NORMAL);
        pToolBar.AddTool(CMD_HISTORY_NEXT, wxBitmap('xpm/right_arrow.xpm'), shortHelpString='Next Directory')

        #//pToolBar->AddControl(&m_wndHistNextBtn);
        #//pToolBar->AddTool(CMD_HISTORY_NEXT_POPUP, _("Help"),  wxBitmap(down_arrow_xpm),   _("Help button"), wxITEM_NORMAL);

        pToolBar.Realize()

        # 2 Filepanels hinein
        self.m_pLeftPanel  = FilePanel (self.m_wndSplitter)
        #self.m_pLeftPanel.SetBackgroundColour (wxColor(20,20,20))
        self.m_pRightPanel = FilePanel (self.m_wndSplitter)
        #self.m_pRightPanel.SetBackgroundColour (wxColor(20,20,20))
        self.m_pActivePanel  = NULL;

        self.m_wndSplitter.SplitVertically(self.m_pLeftPanel, self.m_pRightPanel)
        self.m_wndSplitter.SetMinimumPaneSize(20)
        self.m_wndSplitter.Move((0, 0))


        pMenuFile = wxMenu()
        menuAdd(self, pMenuFile, _("Exit") +"\tAlt+F4", _("Exit"), self.OnClose, wxID_CLOSE)
        menuBar = wxMenuBar()
        # Adding the menus to the MenuBar
        menuBar.Append(pMenuFile, _("&File"))

        pMenuView = wxMenu()
        menuAdd(self, pMenuView, _("Refresh\tF2"), _("Refresh"), self.OperationRefresh, CMD_REFRESH)
        #menuAdd(self, pMenuView, _("Refresh\tF2"), _("Refresh"), self.OnCmdLineAddPath, CMD_CMDLINE_ADD_NAME)
        menuAdd(self, pMenuView, _("Swap Panels") + "\tCtrl+U", _("Swap Panels"), self.OnSwapPanels, CMD_SWAP_PANELS)
        menuAdd(self, pMenuView, _("Equal Panels") + "\tCtrl+E", _("Equal Panels"), self.OnEqualPanels, CMD_EQUAL_PANELS)
        pMenuView.AppendCheckItem(CMD_SHOW_HIDDEN_FILES, _("Show hidden files"))
        pMenuView.Check(CMD_SHOW_HIDDEN_FILES, False)

        menuAdd(self, pMenuView, _("Filter"), _("Filter"), self.OnFilter, CMD_FILTER)

        pMenuSelect = wxMenu()
        menuAdd(self, pMenuSelect, _("All"), _("All"), self.OnSelectAll, CMD_SELECT_ALL)
        menuAdd(self, pMenuSelect, _("None"), _("None"), self.OnSelectNone, CMD_SELECT_NONE)
        menuAdd(self, pMenuSelect, _("Invert"), _("Invert"), self.OnSelectInvert, CMD_SELECT_INVERT)
        menuAdd(self, pMenuSelect, _("Select\t+"), _("Select\t+"), self.OnSelect, CMD_SELECT)
        menuAdd(self, pMenuSelect, _("Deselect\t-"), _("Deselect\t-"), self.OnDeselect, CMD_DESELECT)
        pMenuView.AppendMenu(1, _("Selection"), pMenuSelect, _("Menu Select"))
        menuBar.Append(pMenuView,_("&View"))
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        self.menubar = menuBar
        pMenuAdvanced = wxMenu()
        menuAdd(self, pMenuAdvanced, _("Search\tCtrl+F"), _("Search"), self.OnFileSearch, CMD_FILE_SEARCH)
        menuAdd(self, pMenuAdvanced, _("Compare directories\tShift+F2"), _("Compare directories"), self.OnCompareDirs, CMD_COMPARE_DIRS)
        menuAdd(self, pMenuAdvanced, _("Options\tCtrl+O"), _("Options"), self.OnProgramOptions, CMD_OPTIONS)
        menuAdd(self, pMenuAdvanced, _("Pack file\tAlt+F5"), _("Pack file"), self.OnCompressFiles, CMD_COMPRESS_FILES)
        menuBar.Append(pMenuAdvanced,_("&Advanced"))


        pMenuCmds = wxMenu()
        menuAdd(self, pMenuCmds, _("Open prompt\tCtrl+F3"), _("Open prompt"),  self.OnOpenPrompt,   CMD_OPEN_PROMPT,)
        menuAdd(self, pMenuCmds, _("Edit file\tF4"), _("Edit file"),           self.OnFileEdit,     CMD_FILE_EDIT)
        menuAdd(self, pMenuCmds, _("Copy\tF5"), _("Copy"),                     self.OperationCopy,  CMD_COPY)
        menuAdd(self, pMenuCmds, _("Move\tF6"), _("Move"),                     self.OperationMove,  CMD_MOVE)
        menuAdd(self, pMenuCmds, _("Make directory\tF7"), _("Make directory"), self.OperationMkdir, CMD_MKDIR)
        menuBar.Append(pMenuCmds, _("&Commands"))

        pMenuLanguage = wxMenu()
        self.g_Lang.BuildMenu (pMenuLanguage)

        menuBar.Append(pMenuLanguage, _("&Language"))

        pMenuHelp = wxMenu()
        menuAdd(self, pMenuHelp, _("About"), _("About"), self.OnAboutBox, CMD_TIP_OF_DAY)
        menuAdd(self, pMenuHelp, _("Tip of Day"), _("Tip of Day"), self.OnTipOfDay, CMD_ABOUT_BOX)
        menuBar.Append(pMenuHelp, _("&Help"))


        # TODO: original Image List
        m_objIconList = CImageList()
        self.m_pLeftPanel.m_pFileList.SetImageList(m_objIconList, wxIMAGE_LIST_SMALL)
        self.m_pRightPanel.m_pFileList.SetImageList(m_objIconList, wxIMAGE_LIST_SMALL)


        self.il = wxImageList(16, 16)
        #self.idx1 = self.il.Add(images.getSmilesBitmap())
        self.il.Add(wxBitmap('xpm/up_dir.xpm'))
        self.il.Add(wxBitmap('xpm/folder.xpm'))
        self.il.Add(wxBitmap('xpm/blank.xpm'))

        self.m_pLeftPanel.m_pFileList.SetImageList(self.il, wxIMAGE_LIST_SMALL)
        self.m_pRightPanel.m_pFileList.SetImageList(self.il, wxIMAGE_LIST_SMALL)


        #globals()['g_VfsManager'] = VfsManager ()
        #print globals()['g_VfsManager']
        #global g_VfsManager
        self.g_VfsManager = VfsManager ()
        #globals()['g_VfsManager'].InitList(self.m_pLeftPanel.m_pFileList, NULL)
        self.g_VfsManager.InitList(self.m_pLeftPanel.m_pFileList, NULL)
        self.g_VfsManager.InitList(self.m_pRightPanel.m_pFileList, NULL)

        self.GetActivePanel().Activate(true);

        entries = wxAcceleratorTable([
            #(wxACCEL_NORMAL, WXK_F2,     CMD_CMDLINE_ADD_NAME),
            (wxACCEL_NORMAL, WXK_F2,     CMD_REFRESH),
            (wxACCEL_NORMAL, WXK_F5,     CMD_COPY),
            (wxACCEL_NORMAL, WXK_F6,     CMD_MOVE),
            (wxACCEL_NORMAL, WXK_TAB,    CMD_NEXT_PANEL),
            (wxACCEL_ALT,    WXK_F1,     CMD_LDRIVE_MENU),
            (wxACCEL_ALT,    WXK_F2,     CMD_RDRIVE_MENU),
            (wxACCEL_NORMAL, WXK_DELETE, CMD_DELETE),
            (wxACCEL_NORMAL, WXK_F7,     CMD_MKDIR),
            (wxACCEL_SHIFT,  WXK_F6,     CMD_RENAME),
            (wxACCEL_CTRL,   ord('F'),   CMD_FILE_SEARCH),
            (wxACCEL_CTRL,   WXK_F3,     CMD_OPEN_PROMPT),
            (wxACCEL_NORMAL, WXK_F4,     CMD_FILE_EDIT),
            (wxACCEL_CTRL,   ord('P'),   CMD_CMDLINE_ADD_PATH),
            (wxACCEL_CTRL,   WXK_RETURN, CMD_CMDLINE_ADD_NAME),
            (wxACCEL_CTRL,   ord('U'),   CMD_SWAP_PANELS),
            (wxACCEL_CTRL,   ord('E'),   CMD_EQUAL_PANELS),
            (wxACCEL_SHIFT,  WXK_F2,     CMD_COMPARE_DIRS),
            (wxACCEL_CTRL,   ord('O'),   CMD_OPTIONS),
            (wxACCEL_ALT,    WXK_F5,     CMD_COMPRESS_FILES)])
        self.SetAcceleratorTable(entries)

        #ifdef __WXMSW__
        wxBitmap('xpm/drive.xpm')
        self.SetIcon(wxIcon('xpm/atol.ico', wxBITMAP_TYPE_ICO))
        #else
        #self.SetIcon(wxIcon(drive_xpm)); //TOFIX temporary
        #endif

        self.Show(true)
        #TOMAKEBETTER: later: or what is adjusted in options or in lnk file
        #self.Maximize(true)

        p = PathName ()
        strFile = p.GetIniDirectory()
        #print strFile
        #TOFIX
        strFile += '/atol.ini'

        ini = IniFile ()
        ini.Load(strFile)

        #show splash?
        nValue = int (ini.GetValue('Default', 'ShowSplash', 1))
        if (nValue > 0):
            self.ShowSplash()

        #set show hidden files filter
        nValue = int (ini.GetValue('Default', 'ShowHiddenFiles', 1))
        #hide hidden files
        #print "setsh"
        #print nValue
        if(nValue == 0):
            self.SetShowHiddenFiles(0)
        else:
            self.SetShowHiddenFiles(1)
            #pMenuView.Check(CMD_SHOW_HIDDEN_FILES, True)


        #set starting panel directories
        nValue = int (ini.GetValue('Default', 'RestorePaths', 0))
        if(nValue > 0):
            strValue = ini.GetValue('Panel', 'LeftPath', '')
            if(strValue != ''):
                if os.path.isdir (strValue):
                    self.m_pLeftPanel.m_pFileList.SetDirectory(strValue)
                #leave it in root
                #else:
                #print "set to c"
            strValue = ini.GetValue('Panel', 'RightPath', '')
            if(strValue != ''):
                if os.path.isdir (strValue):
                    self.m_pRightPanel.m_pFileList.SetDirectory(strValue)
                #leave it in root
                #else:
                #print "set to c"

        #load tip startup preferences and start tips if wanted
        nValue = int (ini.GetValue('Default', 'ShowTips', 0))
        if(nValue > 0):
            dummy = wxMenuEvent ()
            self.OnTipOfDay(dummy)

        #load plugins
        #wxString strPluginDir = wxPathOnly(GetExecutablePath());
        strPluginDir = GetExecutablePath()
        #strPluginDir = 'c:/Eigene Dateien/python/wxpyatol'
        strPluginDir += '/plugins';
        self.m_PluginManager = PluginManager()
        self.m_PluginManager.LoadPlugins(strPluginDir);

        EVT_SPLITTER_SASH_POS_CHANGED(self, IDC_SPLITTER, self.OnSplitterResized)
        EVT_ERASE_BACKGROUND(self, self.OnEraseBkg)
        EVT_SIZE(self, self.OnSize)
        EVT_MENU(self, CMD_DELETE, self.OperationDelete)
        EVT_MENU(self, CMD_SHOW_HIDDEN_FILES, self.OnShowHiddenFile)

        EVT_UPDATE_UI(self, CMD_SHOW_HIDDEN_FILES, self.OnShowHiddenFileUpdate)
        EVT_UPDATE_UI(self, CMD_FILE_EDIT, self.OnFileEditUpdate)

        EVT_MENU(self, CMD_HISTORY_PREV, self.OnHistPrev)
        EVT_MENU(self, CMD_HISTORY_PREV_POPUP, self.OnHistPrevPopup)
        EVT_MENU(self, CMD_HISTORY_NEXT, self.OnHistNext)
        EVT_MENU(self, CMD_HISTORY_NEXT_POPUP, self.OnHistNextPopup)
        EVT_UPDATE_UI(self, CMD_HISTORY_PREV, self.OnHistPrevUpdate)
        EVT_UPDATE_UI(self, CMD_HISTORY_NEXT, self.OnHistNextUpdate)
        EVT_UPDATE_UI(self, CMD_HISTORY_PREV_POPUP, self.OnHistPrevUpdate)
        EVT_UPDATE_UI(self, CMD_HISTORY_NEXT_POPUP, self.OnHistNextUpdate)
        EVT_MENU(self, CMD_RENAME, self.OperationRename)
        EVT_MENU(self, CMD_LDRIVE_MENU,   self.DropDriveMenuLeft)
        EVT_MENU(self, CMD_RDRIVE_MENU,   self.DropDriveMenuRight)
        EVT_MENU(self, CMD_NEXT_PANEL,    self.SwitchActivePanel)
        EVT_MENU(self, CMD_REFRESH,       self.OperationRefresh)
        EVT_MENU_RANGE (self, CMD_LANGUAGE_FIRST, CMD_LANGUAGE_LAST, self.OnSelectLanguage)
        EVT_CHAR(self, self.OnChar)
        #EVT_BUTTON(self, 9999, self.OnpdateProgress)
        #EVT_MENU(self, wxID_CLOSE, self.Close)

        EVT_BUTTON(self, 19999, self.OnOverwriteDlg)
        EVT_BUTTON(self, 20000, self.OnNameInputDlg)
        EVT_BUTTON(self, 20001, self.OnDeleteDirDlg)
        EVT_BUTTON(self, 20002, self.OnDeleteErrDlg)
        EVT_BUTTON(self, 20003, self.OnDeleteFileDlg)
        EVT_MENU(self, CMD_CMDLINE_ADD_PATH,  self.OnCmdLineAddPath)
        EVT_MENU(self, CMD_CMDLINE_ADD_NAME,  self.OnCmdLineAddName)

        #import win32file
        #hSrc = win32file.CreateFile('c:\\INSTALL.LOG', win32file.GENERIC_READ, 0, None, win32file.OPEN_EXISTING, 0, 0)
        #print hSrc

        #win32file.CopyFile(source,'%s\%s.bak' % (self.used, os.path.basename(source)),0)
        #print 'testing attributes'
        #print win32file.GetFileAttributes ('c:\\test.txt')

        #self.g = CProgressDlg (NULL, 1, 'progress test ...', wxDefaultPosition, wxDefaultSize, wxCAPTION)
        #self.g.Show(True)
        # def OnpdateProgress (self, event):
        #print 'ev in main'

    def OnSize(self,event):
        pFrm = wxGetApp().GetFrame()
        #global g_SingleInstanceChecker
        #print g_SingleInstanceChecker
        '''
        print 'size'
        event = wxCommandEvent ()
        #event.SetEventType (10001)
        event.SetEventType (wxEVT_COMMAND_BUTTON_CLICKED)
        #event.m_id  = 10001
        event.SetId (102)

        event.m_isCommandEvent = True
        #wxPostEvent(self.m_pLeftPanel, event)
        #self.m_pLeftPanel.ProcessEvent(event)
        self.m_pLeftPanel.AddPendingEvent(event)

        #print event.GetEventObject ()
        #print event.GetEventType ()
        #print event.GetId ()
        #print event.GetSkipped ()
        #print event.GetTimestamp ()

        #EVT_BUTTON(self, ID_ROOT_BUTTON,  self.OnRootButton)

        #print event
        #print event.m_eventType
        #print event.m_id
        #print event.m_isCommandEvent
        '''

        #ShowSystemErrorMessge(3)

        nHeight = self.GetClientSize().GetHeight()
        nWidth  = self.GetClientSize().GetWidth()

        self.m_wndSplitter.SetSize(wxSize( nWidth, nHeight-21 ))
        #keep splitter percent ratio when main window is resized
        self.m_wndSplitter.SetSashPosition((int)(nWidth * self.m_fSplitterPercent))
        self.m_wndCommandLine.SetDimensions(0, nHeight-21, nWidth, 21)


    def OnEraseBkg(self, event):
        pass

    def OnSplitterResized(self, event):
        #recalculate new splitter position percent
        nWidth  = self.GetClientSize().GetWidth()
        nPos    = self.m_wndSplitter.GetSashPosition()
        self.m_fSplitterPercent = nPos / nWidth

    def OnClose(self,event):
        #store startup preferences
        p = PathName ()
        strFile = p.GetIniDirectory()
        #print strFile
        #TOFIX
        strFile += '/atol.ini'

        ini = IniFile ()
        ini.Load(strFile)
        ini.SetValue('Panel', 'LeftPath', self.m_pLeftPanel.m_pFileList.m_pVfs.GetDir())
        ini.SetValue('Panel', 'RightPath', self.m_pRightPanel.m_pFileList.m_pVfs.GetDir())
        ini.SetValue('Default', 'ShowHiddenFiles', self.GetShowHiddenFiles())
        ini.SetValue('Default', 'Language', self.g_Lang.m_strCurLang)
        #print self.m_strCurLang
        #print 'set', self.m_strCurLang
        #ini.SetValue('Default', 'Language', self.m_strCurLang)
        #print 'onclose1'

        ini.Save()
        #print 'onclose2'
        self.Close()
        #print 'onclose3'

    def OnFilter(self,event):
        self.GetActivePanel().m_pFileList.OnFilter(event)

    def GetActivePanel(self):
        if(NULL == self.m_pActivePanel):
            #FIX for initial state
            self.m_pActivePanel = self.m_pLeftPanel;
        return self.m_pActivePanel;


    def GetInactivePanel(self):
        if(NULL == self.m_pActivePanel):
            #FIX for initial state
            self.m_pActivePanel = self.m_pLeftPanel

        if(self.m_pActivePanel == self.m_pLeftPanel):
            return self.m_pRightPanel
        else:
            return self.m_pLeftPanel

    #void MainFrame::OperationRefresh(wxMenuEvent &event)
    def OperationRefresh(self, event):
        #print self.GetActivePanel().m_pFileList.GetEditControl()
        #ifdef __WXMSW__
        #FIX: skip command if command was triggered while file list was in label editing mode
        if(None != self.GetActivePanel().m_pFileList.GetEditControl()):
            #default processing
            event.Skip()
            return
        #endif

        #TOFIX create OpRefresh -> separate thread

    def OperationRename(self, event):
        #ifdef __WXMSW__
        #FIX: skip command if command was triggered while file list was in label editing mode
        if(None != self.GetActivePanel().m_pFileList.GetEditControl()):
            #default processing
            event.Skip()
            return
        #endif

        pListCtrl = self.GetActivePanel().m_pFileList
        if(pListCtrl):
            nItem = pListCtrl.GetItemFocus()
            if(nItem >= 0):
                pListCtrl.EditLabel(nItem)

    def OnSelect (self, event):
        self.GetActivePanel().m_pFileList.OnSelect(event)

    def OnDeselect (self, event):
        self.GetActivePanel().m_pFileList.OnDeselect(event)

    def OnSelectAll (self, event):
        self.GetActivePanel().m_pFileList.SelectAll(event)

    def OnSelectNone (self, event):
        #here no event
        self.GetActivePanel().m_pFileList.ClearSelection()

    def OnSelectInvert (self, event):
        self.GetActivePanel().m_pFileList.InvertSelection(event)

    def OnSwapPanels (self, event):
        #print 'swap panels'
        #swap lists (VFS's) for left/right panels
        #NOTE: we must exchange entire VFS stacks in the panels

        #TOFIX exchange entire VFS stack
        #exchange Vfs pointers
        pVfsTmp = self.m_pLeftPanel.m_pFileList.m_pVfs
        self.m_pLeftPanel.m_pFileList.m_pVfs = self.m_pRightPanel.m_pFileList.m_pVfs;
        self.m_pRightPanel.m_pFileList.m_pVfs = pVfsTmp;

        #exchange listing (no need for listing the Vfs)
        lstTemp = VfsListing ()
        lstTemp = self.m_pLeftPanel.m_pFileList.GetListing()
        self.m_pLeftPanel.m_pFileList.SetListing(self.m_pRightPanel.m_pFileList.GetListing())
        self.m_pRightPanel.m_pFileList.SetListing(lstTemp)

        #exchange history lists
        tmpHistory = self.m_pLeftPanel.m_pFileList.m_lstHistory
        self.m_pLeftPanel.m_pFileList.m_lstHistory = self.m_pRightPanel.m_pFileList.m_lstHistory
        self.m_pRightPanel.m_pFileList.m_lstHistory = self.m_pLeftPanel.m_pFileList.m_lstHistory

    #make inactive panel showing same dir as active one
    #void MainFrame::OnEqualPanels(wxMenuEvent &event)
    def OnEqualPanels(self, event):
        #TOFIX will need rewrite when start using multiple Vfs
        #TOFIX clean Vfs stack and add same Vfs type as in other panel
        #TOFIX speedup process (do not list again)
        strDir = self.GetActivePanel().m_pFileList.m_pVfs.GetDir()
        self.GetInactivePanel().m_pFileList.SetDirectory(strDir)

    #void MainFrame::OnShowHiddenFile(wxMenuEvent &event)
    def OnShowHiddenFile(self, event):
        #reverse hidden state
        #print "ons"
        i = self.GetShowHiddenFiles()
        #print i
        if i:
            i = 0
        else:
            i = 1
        #print i
        self.SetShowHiddenFiles(i)

    #void MainFrame::OnShowHiddenFileUpdate(wxUpdateUIEvent& event)
    def OnShowHiddenFileUpdate(self, event):
        #print "update"
        #print self.GetShowHiddenFiles()
        event.Check(self.GetShowHiddenFiles())

    #bool MainFrame::GetShowHiddenFiles()
    def GetShowHiddenFiles(self):
        #ifdef __WXMSW__
        #hidden files under Windows OS are files having hidden attribute flag set
        bHiddenLeft  =  (ATTR_HIDDEN == (ATTR_HIDDEN & self.m_pLeftPanel.m_pFileList.GetListing().GetFilter().GetAttrHide()))
        bHiddenRight =  (ATTR_HIDDEN == (ATTR_HIDDEN & self.m_pRightPanel.m_pFileList.GetListing().GetFilter().GetAttrHide()))
        #else
        #'hidden' files under Linux are considered files whose name start with '.'
        #static const wxString strWild('.*');
        #bool bHiddenLeft  =  (0 <= m_pLeftPanel->m_pFileList->GetListing().GetFilter().FindNameWildcard(strWild, false));
        #bool bHiddenRight =  (0 <= m_pRightPanel->m_pFileList->GetListing().GetFilter().FindNameWildcard(strWild, false));
        #endif
        bHidden = bHiddenLeft and bHiddenRight
        #print bHiddenRight, bHiddenLeft
        if bHidden == False:
            return 1
        else:
            return 0

    #void MainFrame::SetShowHiddenFiles(bool bShow)
    def SetShowHiddenFiles(self, bShow):
        #print "sets", bShow
        #'hide' command effects both file panels
        #ifdef __WXMSW__
        nAttrShow1 = self.m_pLeftPanel.m_pFileList.GetListing().GetFilter().GetAttrShow()
        nAttrShow2 = self.m_pRightPanel.m_pFileList.GetListing().GetFilter().GetAttrShow()

        nAttrHide1 = self.m_pLeftPanel.m_pFileList.GetListing().GetFilter().GetAttrHide()
        nAttrHide2 = self.m_pRightPanel.m_pFileList.GetListing().GetFilter().GetAttrHide()

        #print "s", nAttrHide1, bShow
        if(bShow):
            #//remove hidden files flag (do not hide them)
            nAttrHide1 &= ~(ATTR_HIDDEN)
            #//remove hidden files flag (do not hide them)
            nAttrHide2 &= ~(ATTR_HIDDEN)
        else:
            #//hide hidden files
            nAttrHide1 |= ATTR_HIDDEN
            #//hide hidden files
            nAttrHide2 |= ATTR_HIDDEN

        self.m_pLeftPanel.m_pFileList.GetListing().GetFilter().SetAttrGroup(nAttrShow1, nAttrHide1)
        self.m_pRightPanel.m_pFileList.GetListing().GetFilter().SetAttrGroup(nAttrShow2, nAttrHide2)
        '''
        #else
        static const wxString strWild('.*');
        if(bShow){
            m_pLeftPanel->m_pFileList->GetListing().GetFilter().RemoveFromNameGroup(strWild, false);
            m_pRightPanel->m_pFileList->GetListing().GetFilter().RemoveFromNameGroup(strWild, false);
        }
        else{
            m_pLeftPanel->m_pFileList->GetListing().GetFilter().AddToNameGroup(strWild, false);
            m_pRightPanel->m_pFileList->GetListing().GetFilter().AddToNameGroup(strWild, false);
        }
        #endif
        '''
        #refilter the lists
        self.m_pLeftPanel.m_pFileList.RefilterList()
        self.m_pRightPanel.m_pFileList.RefilterList()

    def OnFileSearch(self, event):
        dlg = CFileSearchDlg (self)
        dlg.SetPathDefault (self.GetActivePanel().m_pFileList.m_pVfs.GetDir())
        dlg.ShowModal()

    def OnCompareDirs(self, event):
        wait = wxBusyCursor ()

        #//select all FILES, unselects other
        nFiles1 = self.m_pLeftPanel.m_pFileList.SelectFilesOnly()
        nFiles2 = self.m_pRightPanel.m_pFileList.SelectFilesOnly()
        nCommonCount = 0

        bAnyRemote = false

        if( self.m_pLeftPanel.m_pFileList.m_pVfs.GetType() == VFS_FTP    or
            self.m_pLeftPanel.m_pFileList.m_pVfs.GetType() == VFS_SFTP   or
            self.m_pRightPanel.m_pFileList.m_pVfs.GetType() == VFS_FTP   or
            self.m_pRightPanel.m_pFileList.m_pVfs.GetType() == VFS_SFTP):
            self.bAnyRemote = true

        nMax = self.m_pLeftPanel.m_pFileList.GetListing().GetCount()
        for i in range (nMax):
            #only files are compared
            if(self.m_pLeftPanel.m_pFileList.GetListing().GetAt(i).IsDir() == False):
                strItem = self.m_pLeftPanel.m_pFileList.GetListing().GetAt(i).GetName()
                nPos = self.m_pRightPanel.m_pFileList.GetListing().FindItem(strItem)
                if(nPos >= 0):
                    #item found, compare size, date?
                    nSize1 = self.m_pLeftPanel.m_pFileList.GetListing().GetAt(i).m_nSize
                    nSize2 = self.m_pRightPanel.m_pFileList.GetListing().GetAt(nPos).m_nSize

                    if(nSize1 == nSize2):
                        if(bAnyRemote == False):
                            #if both VFS are local compare additionaly by date + attributes
                            strDate1 = self.m_pLeftPanel.m_pFileList.GetListing().GetAt(i).GetDate()
                            strDate2 = self.m_pRightPanel.m_pFileList.GetListing().GetAt(nPos).GetDate()
                            if(strDate1 == strDate2):
                                dwAttr1 = self.m_pLeftPanel.m_pFileList.GetListing().GetAt(i).m_nAttrib
                                dwAttr2 = self.m_pRightPanel.m_pFileList.GetListing().GetAt(nPos).m_nAttrib

                                if(dwAttr1 == dwAttr2):
                                    self.m_pLeftPanel.m_pFileList.DeselectItem(i)
                                    self.m_pRightPanel.m_pFileList.DeselectItem(nPos)
                                    nCommonCount += 1
                        else:
                            self.m_pLeftPanel.m_pFileList.DeselectItem(i)
                            self.m_pRightPanel.m_pFileList.DeselectItem(nPos)
                            nCommonCount += 1

        #message box if the two directories look identical
        if(nFiles1 == nFiles2 and nFiles1 == nCommonCount):
            wxMessageBox(_("The two directories look identical!"))

    def OnProgramOptions (self,event):
        dlg = COptionsDlg ()
        dlg.ShowModal()

    def OnCompressFiles (self,event):
        dlg = CCompressDlg (self)
        dlg.ShowModal()

        #TOFIX

    def OnAboutBox (self,event):
        dlg = AboutDlg (self)
        dlg.ShowModal()

    def OnTipOfDay (self,event):
        #wxString strDir = wxPathOnly(GetExecutablePath());
        strDir = GetExecutablePath ()
        #strDir = 'c:/Eigene Dateien/python/wxpyatol'
        strDir += '/tips.txt'

        log = wxLogNull ()
        tipProvider = wxCreateFileTipProvider(strDir, 0)
        bShowAtStartup = wxShowTip(self, tipProvider)

        #store startup preferences
        #wxString strFile = PathName::GetIniDirectory();
        p = PathName ()
        strFile = p.GetIniDirectory()
        #TOFIX
        strFile += '/atol.ini'

        ini = IniFile ()
        ini.Load(strFile)
        if (bShowAtStartup):
            nValue = 1
        else:
            nValue = 0
        ini.SetValue('Default', 'ShowTips', nValue)
        return

    def OnOpenPrompt (self, event):
        #print '1ind Languages'
        pass

    def OnFileEdit (self, event):
        nPos = self.GetActivePanel().m_pFileList.GetItemFocus()
        if nPos >= 0:
            item = self.GetActivePanel().m_pFileList.GetListing().GetAt(nPos)
            if not item.IsDir():
                #//TOFIX read from INI settings with default values for various platforms
                #wxString strEditor;
                #ifdef __WXMSW__
                strEditor = "notepad.exe"
                #else
                #strEditor = "gedit";
                #endif
                #def ExecuteFile(szFile, szArgs, szDir, nData):

                ExecuteFile(strEditor, item.GetName(), self.GetActivePanel().m_pFileList.m_pVfs.GetDir(), 0)

    def OnFileEditUpdate (self, event):
        #print "onf"
        #//TOFIX also check if focus is on the file
        if self.GetActivePanel().m_pFileList.m_pVfs.GetType() == VFS_LOCAL:
            event.Enable(True)
        else:
            event.Enable(False)

    def OperationCopy (self, event):
        #print '1', thread.get_ident()

        #ifdef __WXMSW__
        #FIX: skip command if command was triggered while file list was in label editing mode
        if(None != self.GetActivePanel().m_pFileList.GetEditControl()):
            #default processing
            event.Skip()
            return
        #endif

        #STEP 1: create list of items selected in currently active file panel
        objSel = VfsSelection ()
        self.GetActivePanel().GetSelection(objSel)

        #last checks
        if(0 == objSel.GetTotalCount()):
            wxMessageBox(_("No selection!"))
            return
        #print objSel.GetTotalCount()
        nRes = wxMessageBox(_("Do you want to copy selected items?"), self.wxMessageBoxCaptionStr, wxYES_NO|wxCENTRE)
        if(wxYES != nRes):
            return

        pVfsSrc = self.GetActivePanel().m_pFileList.m_pVfs
        pVfsDst = self.GetInactivePanel().m_pFileList.m_pVfs

        #STEP 2: start copy operation with progress (op executing in separate thread)
        self.m_objOpManager.StartOperation(OP_COPY, pVfsSrc, pVfsDst, objSel)

        #TOFIX:move to manager + check to refresh active if needed

        #print '2', thread.get_ident()
        self.GetInactivePanel().m_pFileList.RefreshList()

    def OperationMove (self, event):
        #ifdef __WXMSW__
        #//FIX: skip command if command was triggered while file list was in label editing mode
        if(None != self.GetActivePanel().m_pFileList.GetEditControl()):
            #//default processing
            event.Skip()
            return
        #endif

        #//STEP 1: create list of items selected in currently active file panel
        objSel = VfsSelection ()
        self.GetActivePanel().GetSelection(objSel)

        #//last checks
        if(0 == objSel.GetTotalCount()):
            wxMessageBox(_("No selection!"))
            return

        nRes = wxMessageBox(_("Do you want to move selected items?"), self.wxMessageBoxCaptionStr, wxYES_NO|wxCENTRE)
        if(wxYES != nRes):
            return;

        pVfsSrc = self.GetActivePanel().m_pFileList.m_pVfs
        pVfsDst = self.GetInactivePanel().m_pFileList.m_pVfs

        #//STEP 2: start copy operation with progress (op executing in separate thread)
        self.m_objOpManager.StartOperation(OP_MOVE, pVfsSrc, pVfsDst, objSel)

        #//TOFIX:move to manager + check to refresh active if needed
        self.GetActivePanel().m_pFileList.RefreshList()
        self.GetInactivePanel().m_pFileList.RefreshList()

    def OperationDelete (self, event):
        #//FIX: seems that wx roots commands improperly
        #//(Del key pressed inside command line edit is first passed to MainFrame?)
        if(wxWindow_FindFocus() == self.m_wndCommandLine):
            #//default processing
            event.Skip()
            return

        #ifdef __WXMSW__
        #//FIX: skip command if command was triggered while file list was in label editing mode
        if(None != self.GetActivePanel().m_pFileList.GetEditControl()):
            #//default processing
            event.Skip()
            return
        #endif

        #//STEP 1: create list of items selected in currently active file panel
        objSel = VfsSelection ()
        self.GetActivePanel().GetSelection(objSel)

        #//last checks
        if(0 == objSel.GetTotalCount()):
            wxMessageBox(_("No selection!"))
            return


        nRes = wxMessageBox(_("Do you want to delete selected items?"), self.wxMessageBoxCaptionStr, wxYES_NO|wxCENTRE)
        if(wxYES != nRes):
            return;

        pVfsSrc = self.GetActivePanel().m_pFileList.m_pVfs
        pVfsDst = self.GetInactivePanel().m_pFileList.m_pVfs
        #print pVfsSrc, pVfsDst
        #return
        #//STEP 2: start copy operation with progress (op executing in separate thread)
        self.m_objOpManager.StartOperation(OP_DELETE, pVfsSrc, pVfsDst, objSel)

        #//TOFIX:move to manager + check to refresh active if needed

        self.GetActivePanel().m_pFileList.RefreshList()

    def OperationMkdir (self, event):
        #ifdef __WXMSW__
        #//FIX: skip command if command was triggered while file list was in label editing mode
        if(None != self.GetActivePanel().m_pFileList.GetEditControl()):
            #//default processing
            event.Skip()
            return
        #endif

        dlg = CNameInputDlg ()
        dlg.SetTitle(_("New directory name"))
        if(wxOK == dlg.ShowModal()):
            #//TOFIX Op class with blocking (waiting)
            pVfsSrc = self.GetActivePanel().m_pFileList.m_pVfs
            pVfsSrc.MkDir(dlg.m_strValue)

            #//TOFIX:move to manager + check to refresh active if needed
            self.GetActivePanel().m_pFileList.RefreshList()

    def ShowSplash (self):
        return
        #'//TOFIX store bitmap as resource?
        #//calculate splash bitmap path
        #strFile = wxPathOnly(GetExecutablePath());
        #strFile = 'c:/Eigene Dateien/python/wxpyatol'
        strFile = GetExecutablePath ()
        strFile += '/splash.png';
        #print 'show splash'
        #TODO: how does it work?
        #//prevent error dialog if file not found
        # in wxpython?
        log = wxLogNull ()

        bitmap = wxBitmap (strFile, wxBITMAP_TYPE_PNG)
        #TODO: what does it exactly do? (seen so often yet)
        wxInitAllImageHandlers()

        #if (bitmap.LoadFile(strFile, wxBITMAP_TYPE_PNG)):
        #print bitmap
        if bitmap:
            #print 'bef'
            splashscreen.SplashScreen(NULL, -1, _("Welcome to wxpyatol"),
                wxSIMPLE_BORDER|wxSTAY_ON_TOP,
                6000, strFile)
                #TODO
                #callback?

            #splashscreen.SplashScreen(bitmap,
            #    wxSPLASH_CENTRE_ON_SCREEN|wxSPLASH_TIMEOUT,
            #    6000, NULL, -1, wxDefaultPosition, wxDefaultSize,
            #    wxSIMPLE_BORDER|wxSTAY_ON_TOP);
        wxYield()


    def OnHistPrev(self, event):
        list = self.GetActivePanel().m_pFileList.m_lstHistory
        if(list.CanMovePrev()):
            strPath = list.MovePrev()
            self.GetActivePanel().m_pFileList.SetDirectory(strPath, False)

    def OnHistNext(self, event):
        list = self.GetActivePanel().m_pFileList.m_lstHistory
        if(list.CanMoveNext()):
            strPath = list.MoveNext()
            self.GetActivePanel().m_pFileList.SetDirectory(strPath, False)

    def OnHistPrevPopup(self, event):
        #show popup menu with backwards browsing history items
        menu = CPopupMenu ()
        list = self.GetActivePanel().m_pFileList.m_lstHistory.m_lstBackward
        nCmdID = 1
        nSize  = len(list)

        for i in range(len(list)):
            strPath = list[nSize-1-i]
            menu.Append(nCmdID, strPath)
            nCmdID += 1

        #wxToolBar *pToolBar = GetToolBar();
        #TOFIX position
        self.PopupMenu(menu, 20, 20)

        #execute
        nCmdID = menu.GetSelectedID()
        if(nCmdID > 0):
            strPath = list[nSize-nCmdID]
            self.GetActivePanel().m_pFileList.m_lstHistory.Move(nCmdID, true)
            self.GetActivePanel().m_pFileList.SetDirectory(strPath, false)

    def OnHistNextPopup(self, event):
        #show popup menu with forward browsing history items
        menu = CPopupMenu ()
        list = self.GetActivePanel().m_pFileList.m_lstHistory.m_lstForward
        nCmdID = 1
        nSize  = len(list)

        for i in range(len(list)):
            strPath = list[nSize-1-i]
            menu.Append(nCmdID, strPath)
            nCmdID += 1

        self.PopupMenu(menu, 40, 20)

        #execute
        nCmdID = menu.GetSelectedID()
        if(nCmdID > 0):
            strPath = list[nSize-nCmdID]
            self.GetActivePanel().m_pFileList.m_lstHistory.Move(nCmdID, false)
            self.GetActivePanel().m_pFileList.SetDirectory(strPath, false)

    #void MainFrame::OnHistPrevUpdate(wxUpdateUIEvent& event)
    def OnHistPrevUpdate(self, event):
        list = self.GetActivePanel().m_pFileList.m_lstHistory
        event.Enable(list.CanMovePrev())

    def OnHistNextUpdate(self, event):
        list = self.GetActivePanel().m_pFileList.m_lstHistory
        event.Enable(list.CanMoveNext())

    def ClearCmdLine(self):
        return self.m_wndCommandLine.ClearCmd()

    def ExecuteCmdLine(self):
        return self.m_wndCommandLine.ExecuteCmd()


    def OnOpenPrompt(self, event):
        #//pick initial directory to be set inside console window
        #wxString strDir;
        if(self.GetActivePanel().m_pFileList.m_pVfs.GetType() == VFS_LOCAL):
            strDir = self.GetActivePanel().m_pFileList.m_pVfs.GetDir()

        OpenCommandPrompt(strDir, self.GetHandle())

    def OnChar(self, event):
        nKey = event.GetKeyCode()
        #if ispri nt(nKey) and not event.HasModifiers():
        #TOMAKEBETTER: (delete, backspace work?)
        if chr(nKey) >= 32 and not event.HasModifiers():
            #wxString str;
            #str = '%c', (unsigned char)nKey);
            self.m_wndCommandLine.AppendString(chr(nKey))
            return
        elif (nKey == WXK_RETURN):
            if self.m_wndCommandLine.ExecuteCmd():
                return
        elif (nKey == WXK_ESCAPE):
            if self.m_wndCommandLine.ClearCmd():
                return

        event.Skip()


    def DropDriveMenuLeft(self, event):
        #//dummy
        evDummy = wxCommandEvent ()
        self.m_pLeftPanel.OnDriveButton(evDummy)

    def DropDriveMenuRight(self, event):
        #//dummy
        evDummy = wxCommandEvent ()
        self.m_pRightPanel.OnDriveButton(evDummy)

    def SwitchActivePanel(self, event):
        #print 'SwitchActivePanel'
        self.GetActivePanel().Activate(False)
        self.m_pActivePanel = self.GetInactivePanel()
        self.m_pActivePanel.Activate(True)

    #//TOFIX move to GuiLanguage
    def OnSelectLanguage(self, event):
        i = event.GetId() - CMD_LANGUAGE_FIRST
        #print i
        #print self.m_arStrAvailLang[0]
        #print self.m_arStrAvailLang[1]
        #print self.m_arStrAvailLang[2]
        #// francesco
        #// gleich geblieben: keine Restart message
        #// unchanged: not message is needed
        #print 'change'
        if self.g_Lang.m_strCurLang != self.g_Lang.m_arStrAvailLang[i]:
            self.g_Lang.m_strCurLang = self.g_Lang.m_arStrAvailLang[i]
            if (self.g_Lang.m_bLangRestartReminder):
                self.g_Lang.m_bLangRestartReminder = false;
                wxMessageBox (_("You need to restart to set the new language:"))

    #void MainFrame::OnOverwriteDlg(wxCommandEvent &event)
    def OnOverwriteDlg(self, event):
        #print "OnOverwriteDlg"
        dlg = COverwriteDlg ()
        dlg.m_strInfo = g_strTitle
        g_nGuiResult = dlg.ShowModal()

        #TODO
        #g_objGUISyncSemaphore.Post();

    def OnNameInputDlg(self, event):
        #print "OnNameInputDlg"
        #//TOFIX
        dlg = CNameInputDlg ()
        dlg.m_strTitle = g_strTitle;
        dlg.m_strValue = g_strResult

        g_nGuiResult = dlg.ShowModal()
        #TODO
        #g_strResult = dlg.m_strValue;
        #g_objGUISyncSemaphore.Post();

    def OnDeleteDirDlg(self, event):
        #print "OnDeleteDirDlg"
        g_nGuiResult = 0;
        if(wxNO == wxMessageBox(_("Directory %s is not empty! Delete?") % g_strTitle, self.wxMessageBoxCaptionStr, wxYES_NO|wxCENTRE)):
            g_nGuiResult = OPF_SKIP

        #TODO
        #g_objGUISyncSemaphore.Post();

        #//TOFIX
        #//#define STR_DELETE_DIR    "Directory %s is not empty!\r\nDo you want to delete it with all its contents?"
        '''
        /*
        COperationDlg dlg;
        dlg.m_strMessage.Format(STR_DELETE_DIR, szPath);
        return dlg.DoModal();
        */
        '''

    def OnDeleteErrDlg(self, event):
        #print "OnDeleteErrDlg"
        #//TOFIX
        '''
        /*  //TOFIX support for retry
            CDeleteErrDlg dlg;
            dlg.m_strError = strMsg;
            return dlg.DoModal(); //OK - continue, Cancel - Abort all
        */
        '''
        wxMessageBox(g_strTitle)
        #TODO
        #g_objGUISyncSemaphore.Post();

    def OnDeleteFileDlg(self, event):
        #print "OnDeleteFileDlg"
        dlg = CDeleteDlg ()
        dlg.SetTitle = _("%s is read only! Delete?") % g_strTitle
        g_nGuiResult = dlg.ShowModal()
        #TODO
        #g_objGUISyncSemaphore.Post();

    def OnCmdLineAddPath(self, event):
        strDir = self.GetActivePanel().m_pFileList.m_pVfs.GetDir()
        self.m_wndCommandLine.AppendString(strDir)

    def OnCmdLineAddName(self, event):
        nPos = self.GetActivePanel().m_pFileList.GetItemFocus()
        if(nPos >= 0):
            #VfsItem &item = GetActivePanel()->m_pFileList->GetListing().GetAt(nPos);
            item = self.GetActivePanel().m_pFileList.GetListing().GetAt(nPos)
            strName = item.GetName()
            self.m_wndCommandLine.AppendString(strName)


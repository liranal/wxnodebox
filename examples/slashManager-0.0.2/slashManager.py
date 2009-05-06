#! /usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; fill-column: 79; coding: iso-latin-1-unix -*-
#
# Tested with Python 2.2, wxWindows 2.4.2, and wxPython 2.4.2.4

import sys, os

from wxPython.wx import true, false, wxNewId, wxInitAllImageHandlers, wxDefaultPosition
from wxPython.wx import wxMessageBox, wxMessageDialog
from wxPython.wx import EVT_MENU, EVT_KEY_DOWN, EVT_COMBOBOX, EVT_TOOL
from wxPython.wx import wxNO_BORDER, wxWANTS_CHARS, wxDEFAULT_FRAME_STYLE, wxNO_FULL_REPAINT_ON_RESIZE
from wxPython.wx import WXK_BACK, WXK_LEFT, WXK_RIGHT, WXK_DELETE
from wxPython.wx import wxACCEL_ALT, wxACCEL_NORMAL, wxACCEL_CTRL
from wxPython.wx import wxCB_DROPDOWN, wxCB_READONLY
from wxPython.wx import wxST_SIZEGRIP
from wxPython.wx import wxMB_DOCKABLE
from wxPython.wx import wxTB_HORIZONTAL, wxTB_DOCKABLE
from wxPython.wx import wxITEM_CHECK
from wxPython.wx import wxART_TOOLBAR, wxART_FRAME_ICON
from wxPython.wx import wxOK, wxYES, wxYES_NO
from wxPython.wx import wxApp, wxButton, wxComboBox, wxFrame, wxMenu, wxMenuBar, wxSize, wxSplitterWindow
from wxPython.wx import wxAcceleratorTable, wxIcon
from wxPython.wx import wxICON_INFORMATION

__version__ = (0, 0, 4)

from itemlist import smNotebook
from dirctrl import smDirCtrl
from viewers import ProcessManager
#from clipboard import TheClipboard
#from misc import PathComboWithCompletion
from art import TheArtProvider
import smicons

class smFrame(wxFrame):
    def __init__(self, parent, ID, title, pos, size, pm, paths):
        wxFrame.__init__(self, parent, ID, title, pos, size,
                         wxWANTS_CHARS|wxDEFAULT_FRAME_STYLE|wxNO_FULL_REPAINT_ON_RESIZE, title)

        self.procMngr = pm

        if 0:
            #self.SetIcon(wxIcon(d, 16, 16))
            bmp = TheArtProvider.GetBitmap(TheArtProvider.SM, wxART_FRAME_ICON, (16, 16))
            ico = wxIcon("",16)
            ico.CopyFromBitmap(bmp)
            self.SetIcon(ico)

        self.SetIcons(smicons.GetIconBundle())

        self.refreshStr = " Refresh the display"
        self.goUpStr = " Go up to parent item"
        self.goBackStr = " Go to previous item in history"
        self.goForwardStr = " Go to next item in history"
        self.goHomeStr = " Go to home directory"
        self.copyStr = " Copy selected items to clipboard"
        self.cutStr = " Cut selected items to clipboard"
        self.pasteStr = " Paste from clipboard"
        self.deleteStr = " Delete selected items"
        self.setupToolbar()
        self.setupMenus()

        self.splitterId = wxNewId()
        self.splitter = wxSplitterWindow(self, self.splitterId)

        # validity of 'paths'
        newPaths = []
        for path in paths:
            path = os.path.abspath(os.path.expanduser(path))
            if not os.path.exists(path) or not os.path.isdir(path):
                continue
            newPaths.append(path)
        if not newPaths: # no valid paths
            newPaths.append("/")
        paths = newPaths

        self.ntbook = smNotebook(self.splitter, wxNewId(), self.statusBar, self.OnItemSelected,
                                 self.ShowHidden, paths)
        self.dirCtrl = smDirCtrl(self.splitter, false, self.OnDirSelected, paths[0])

        self.splitter.SetMinimumPaneSize(20)
        self.splitter.SplitVertically(self.dirCtrl, self.ntbook)
        self.splitter.SetSashPosition(100)

        # let the menus and accelerator tables do the work
        #EVT_KEY_DOWN(self, self.OnKeyDown)
        # I cannot get these to work through menu accelerators (aka keyboard shortcuts)
        # It interferes with label editing: steals keystrokes!
        aTable = wxAcceleratorTable([(wxACCEL_NORMAL, WXK_BACK, self.goUpId),
                                     (wxACCEL_ALT, WXK_LEFT, self.goBackId),
                                     (wxACCEL_ALT, WXK_RIGHT, self.goForwardId),
                                     (wxACCEL_NORMAL, WXK_DELETE, self.deleteId)])
        self.dirCtrl.SetAcceleratorTable(aTable)
        self.ntbook.SetAcceleratorTable(aTable)

    def ShowHidden(self, flag):
        # don't to change the flag if it's not necessary (setting the flag triggers more events)

        curFlag = self.dirCtrl.GetShowHidden()
        # flag and curFlag may be different objects (boolean vs. integer)
        if flag:
            if not curFlag: self.dirCtrl.ShowHidden(flag)
        else:
            if curFlag: self.dirCtrl.ShowHidden(flag)

    def OnDirSelected(self, path): # called when DirCtrl has new path
        self.ntbook.SetPath(path)
        self.SetComboPath(path)

    def OnItemSelected(self, item):
        if os.path.isdir(item):
            self.dirCtrl.FixedSetPath(item)
            self.SetComboPath(item)
        else:
            self.procMngr.OpenFile(self, item)

        #FIXME
        #else: ViewFile(self, fullPath)

    def SetComboPath(self, path):
        # if in the middle of wxCombobox event process don't touch the combo
        if not self.pathComboAllowed: return

        cBox = self.pathCombo
        cBox.Clear()
        while 1:
            cBox.Append(path)
            dirName = os.path.dirname(path)
            if path == dirName: break
            path = dirName

    def OnKeyDown(self, event, client=None):
        print event.HasModifiers()
        print event.MetaDown(), event.ShiftDown()
        print WXK_BACK, event.KeyCode()
        event.Skip()
        return false

    def OnAbout(self, event):
        # Create a message dialog box
        dialog = wxMessageDialog(self, " slashManager is a Unix-oriented file manager\n"
                                 " written in wxPython.",
                                 "About slashManager", wxOK | wxICON_INFORMATION)
        dialog.ShowModal() # Shows it
        dialog.Destroy()   # finally destroy it when finished

    def OnExit(self, event):
        # there are many shortcuts to get here (menu, accelerators) so better ask
        answer = wxMessageBox("Do you really want to quit?", "Exit confirmation", wxYES_NO, self)
        if answer == wxYES:
            self.Close(true) # Close the frame.
            event.Skip()     # Make sure the default handler runs too...
        else: pass

    def OnCombo(self, event):
        path = event.GetString()
        # the combobox cannot be changed during its event processing so block it
        self.pathComboAllowed = false
        self.OnItemSelected(path)
        # allow event processing; this will leave the combobox slightly out of date, but it will
        # be fixed during the first click after combobox processing is done
        # the out-of-date state may be regarded as a feature: if selected the wrong entry
        # in the combobox then they will all still be available
        self.pathComboAllowed = true

    def setupToolbar(self):
        # A Statusbar in the bottom of the window
        self.statusBar = self.CreateStatusBar(2, wxST_SIZEGRIP)
        self.statusBar.SetStatusWidths([300, -1]) # two areas: 300px + the rest

        self.toolBar = tb = self.CreateToolBar(wxTB_HORIZONTAL | wxTB_DOCKABLE | wxNO_BORDER )

        self.pathCombo = wxComboBox(tb, wxNewId(), size=(300, -1), choices=["/"], style=wxCB_DROPDOWN|wxCB_READONLY)
        self.pathComboAllowed = true
        tb.AddControl(self.pathCombo)
        EVT_COMBOBOX(self, self.pathCombo.GetId(), self.OnCombo)
                     #lambda e, self=self: sys.stdout.write(e.GetString()+"\n"))#self.OnDirSelected(e.GetString()))
        tb.AddSeparator()

        client = wxART_TOOLBAR
        size = 16
        self.tbNewDirId = wxNewId()
        self.tbGoUpId = wxNewId()
        self.tbGoBackId = wxNewId()
        self.tbGoForwardId = wxNewId()
        self.tbRefreshId = wxNewId()
        self.tbGoHomeId = wxNewId()
        self.tbCopyId = wxNewId()
        self.tbCutId = wxNewId()
        self.tbPasteId = wxNewId()
        self.tbDeleteId = wxNewId()
        tap = TheArtProvider
        for t in ((self.tbNewDirId, "New item", " Create new item", tap.NEW_DIR),
                  (),
                  (self.tbGoUpId, "Go up", self.goUpStr, tap.GO_UP),
                  (self.tbGoBackId, "Go back", self.goBackStr, tap.GO_BACK),
                  (self.tbGoForwardId, "Go forward", self.goForwardStr, tap.GO_FORWARD),
                  (self.tbRefreshId, "Refresh", self.refreshStr, tap.REFRESH),
                  (self.tbGoHomeId, "Home", self.goHomeStr, tap.GO_HOME),
                  (),
                  (self.tbCopyId, "Copy", self.copyStr, tap.COPY),
                  (self.tbCutId, "Cut", self.cutStr, tap.CUT),
                  (self.tbPasteId, "Paste", self.pasteStr, tap.PASTE),
                  (),
                  (self.tbDeleteId, "Delete", self.deleteStr, tap.TRASH)):

            if len(t) < 3:
                tb.AddSeparator()
                continue
            id, txt, toolTip, artid = t
            bmp = TheArtProvider.GetBitmap(artid, client, (size, size))
            tb.AddSimpleTool(id, bmp, txt, toolTip)

        tb.AddSeparator()
        self.globCombo = wxComboBox(tb, wxNewId(), "*", choices=["*"], style=wxCB_DROPDOWN)
        self.globButton = wxButton(tb, wxNewId(), "Filter")
        tb.AddControl(self.globCombo)
        tb.AddControl(self.globButton)

        EVT_TOOL(self, self.tbNewDirId, lambda e, self=self: self.ntbook.NewItem())
        EVT_TOOL(self, self.tbGoUpId, lambda e, self=self: self.ntbook.HistoryGo(e, 0))
        EVT_TOOL(self, self.tbGoBackId, lambda e, self=self: self.ntbook.HistoryGo(e, -1))
        EVT_TOOL(self, self.tbGoForwardId, lambda e, self=self: self.ntbook.HistoryGo(e, +1))
        EVT_TOOL(self, self.tbGoHomeId, lambda e, self=self: self.ntbook.GoHome())
        EVT_TOOL(self, self.tbRefreshId, lambda e, self=self: self.ntbook.Refresh())
        EVT_TOOL(self, self.tbCopyId, lambda e, self=self: self.ntbook.CopyCutPaste(0))
        EVT_TOOL(self, self.tbCutId, lambda e, self=self: self.ntbook.CopyCutPaste(1))
        EVT_TOOL(self, self.tbPasteId, lambda e, self=self: self.ntbook.CopyCutPaste(2))
        EVT_TOOL(self, self.tbDeleteId, lambda e, self=self: self.ntbook.DeleteItems(e))

    def setupMenus(self):
        self.newId = wxNewId()
        self.openId = wxNewId()
        self.viewId = wxNewId()
        self.editId = wxNewId()
        self.openWithId = wxNewId()
        self.propertiesId = wxNewId()
        self.deleteId = wxNewId()
        self.exitId = wxNewId()
        self.cutId = wxNewId()
        self.copyId = wxNewId()
        self.pasteId = wxNewId()
        self.pasteLinkId = wxNewId()
        self.moveToDirId = wxNewId()
        self.copyToDirId = wxNewId()
        self.selectAllId = wxNewId()
        self.deselectAllId = wxNewId()
        self.invertSelectionId = wxNewId()
        self.refreshId = wxNewId()
        self.addBookmarkId = wxNewId()
        self.manageBookmarkId = wxNewId()
        self.goUpId = wxNewId()
        self.goBackId = wxNewId()
        self.goForwardId = wxNewId()
        self.goHomeId = wxNewId()
        self.mountId = wxNewId()
        self.umountId = wxNewId()
        self.aboutId = wxNewId()

        filemenu = wxMenu()
        filemenu.Append(self.newId, "&New item\tCtrl-N", " New item")
        filemenu.Append(self.viewId, "&View\tF3", " View selected items")
        filemenu.Append(self.openId, "&Open\tCtrl-O", " Open selected items")
        filemenu.Append(self.editId, "&Edit\tF4", " Edit selected items")
        filemenu.Append(self.openWithId, "Open &with\tCtrl-W", " Open selected items with ...")
        filemenu.AppendSeparator()
        filemenu.Append(self.propertiesId, "P&roperties\tCtrl-P", " Show properties of selected items")
        filemenu.Append(self.deleteId, "&Delete\tDELETE", self.deleteStr)
        filemenu.AppendSeparator()
        filemenu.Append(self.exitId, "E&xit\tCtrl-Q", " Terminate the program")

        editmenu = wxMenu()
        editmenu.Append(self.copyId, "&Copy\tCtrl-C", self.copyStr)
        editmenu.Append(self.cutId, "C&ut\tCtrl-X", self.cutStr)
        editmenu.Append(self.pasteId, "&Paste\tCtrl-V", self.pasteStr)
        editmenu.Append(self.pasteLinkId, "Paste &link\tCtrl-L", " Paste symbolic link")
        editmenu.AppendSeparator()
        editmenu.Append(self.moveToDirId, "&Move to directory\tCtrl-M", " Move to different direcotry")
        editmenu.Append(self.copyToDirId, "Cop&y to directory\tCtrl-N", " Copy to different direcotry")
        editmenu.AppendSeparator()
        editmenu.Append(self.selectAllId, "&Select all\tCtrl-A", " Select all items")
        editmenu.Append(self.deselectAllId, "&Deselect all\tCtrl-Z", " Deselect all items")
        editmenu.Append(self.invertSelectionId, "&Invert selection\tCtrl-I", " Invert selection")

        viewmenu = wxMenu()
        viewmenu.Append(self.refreshId, "&Refresh\tCtrl-R", self.refreshStr)
        viewmenu.AppendSeparator()

        go__menu = wxMenu()
        go__menu.Append(self.goUpId, "&Up", self.goUpStr)
        go__menu.Append(self.goBackId, "&Back\tALT-LEFT", self.goBackStr)
        go__menu.Append(self.goForwardId, "&Forward\tALT-RIGHT", self.goForwardStr)
        go__menu.Append(self.goHomeId, "&Home\tALT-HOME", self.goHomeStr)

        bookmenu = wxMenu()
        bookmenu.Append(self.addBookmarkId, "&Add\tCtrl-D", " Add bookmark")
        bookmenu.Append(self.manageBookmarkId, "&Manage", " Manage bookmarks")

        toolmenu = wxMenu()
        toolmenu.Append(self.mountId, "&Options", " Mount device")

        helpmenu = wxMenu()
        helpmenu.Append(self.aboutId, "&About", " Information about this program")

        # Creating the menubar.
        menuBar = wxMenuBar(wxMB_DOCKABLE)
        menuBar.Append(filemenu, "&File")
        menuBar.Append(editmenu, "&Edit")
        menuBar.Append(viewmenu, "&View")
        menuBar.Append(go__menu, "&Go")
        menuBar.Append(bookmenu, "&Bookmarks")
        menuBar.Append(toolmenu, "&Tools")
        menuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(menuBar) # Adding the MenuBar to the Frame content.

        # attach events to menus
        EVT_MENU(self, self.deleteId, lambda e, self=self: self.ntbook.DeleteItems(e))
        EVT_MENU(self, self.propertiesId, lambda e, self=self: self.ntbook.Properties())
        EVT_MENU(self, self.newId, lambda e, self=self: self.ntbook.NewItem())
        EVT_MENU(self, self.goUpId, lambda e, self=self: self.ntbook.HistoryGo(e, 0))
        EVT_MENU(self, self.goBackId, lambda e, self=self: self.ntbook.HistoryGo(e, -1))
        EVT_MENU(self, self.goForwardId, lambda e, self=self: self.ntbook.HistoryGo(e, +1))
        EVT_MENU(self, self.goHomeId, lambda e, self=self: self.ntbook.GoHome())
        EVT_MENU(self, self.refreshId, lambda e, self=self: self.ntbook.Refresh())
        EVT_MENU(self, self.copyId, lambda e, self=self: self.ntbook.CopyCutPaste(0))
        EVT_MENU(self, self.cutId, lambda e, self=self: self.ntbook.CopyCutPaste(1))
        EVT_MENU(self, self.pasteId, lambda e, self=self: self.ntbook.CopyCutPaste(2))
        EVT_MENU(self, self.selectAllId, lambda e, self=self: self.ntbook.SelectItems(1))
        EVT_MENU(self, self.deselectAllId, lambda e, self=self: self.ntbook.SelectItems(0))
        EVT_MENU(self, self.invertSelectionId, lambda e, self=self: self.ntbook.SelectItems(-1))
        EVT_MENU(self, self.aboutId, self.OnAbout)
        EVT_MENU(self, self.exitId, self.OnExit)

        # that doesn't work because frame doesn't get focus
        #self.SetAcceleratorTable(wxAcceleratorTable([(wxACCEL_CTRL, ord('P'), self.exitId)]))

class smApp(wxApp):
    def OnInit(self):
        wxInitAllImageHandlers()

        procMngr = self.procMngr = ProcessManager()

        paths = sys.argv[1:] or ["~"]
        width, height = 800, 600
        frame = smFrame(None, wxNewId(), "slashManager", wxDefaultPosition,
                        wxSize(width, height), procMngr, paths)
        frame.Show(true)
        self.frame = frame

        self.SetTopWindow(frame)
        return true

    def OnExit(self):
        self.procMngr.OnAppExit()

def main(argv):
    app = smApp(0)
    app.MainLoop()
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

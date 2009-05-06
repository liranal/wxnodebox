#! /usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; fill-column: 79; coding: iso-latin-1-unix -*-
#

import dircache, os, shutil, string, time

from wxPython.wx import wxNewId, false, true, EVT_LIST_ITEM_ACTIVATED, \
     EVT_LIST_ITEM_RIGHT_CLICK, EVT_RIGHT_UP, EVT_MENU, EVT_NOTEBOOK_PAGE_CHANGED, \
     EVT_LIST_BEGIN_LABEL_EDIT, EVT_LIST_END_LABEL_EDIT, EVT_LIST_ITEM_SELECTED, \
     EVT_LIST_ITEM_DESELECTED, EVT_IDLE
from wxPython.wx import wxLIST_HITTEST_ONITEMICON, wxLIST_HITTEST_ONITEMLABEL, \
     wxLIST_NEXT_ALL, wxLIST_STATE_SELECTED
from wxPython.wx import wxLC_LIST, wxLC_ALIGN_LEFT, wxLC_EDIT_LABELS, \
     wxNO_BORDER, wxSUNKEN_BORDER, \
     wxTAB_TRAVERSAL, wxART_TOOLBAR, wxIMAGE_LIST_SMALL, wxITEM_CHECK, \
     wxITEM_RADIO, wxOK, wxICON_ERROR, wxYES, wxYES_NO, wxCANCEL, wxICON_QUESTION, \
     wxICON_INFORMATION
from wxPython.wx import wxListCtrl, wxImageList, wxMenu, wxNotebook, wxMessageBox

#from wxPython.wx import wxLC_SMALL_ICON, wxLC_ICON, wxLC_ALIGN_LEFT, wxLC_REPORT, wxLC_NO_HEADER
#from wxPython.wx import wxListItem, wxLIST_FORMAT_RIGHT, wxLIST_FORMAT_LEFT, wxLIST_FORMAT_CENTRE

from art import TheArtProvider
from transfer import TransferDialog, TransferItems
from utils import IsMountPoint, PermsUserGroup, Bytes2SizeUnits, MsgOS, mtime
from properties import ShowProperties
from fsmenu import FSMenu

TheClipboard = None

class PathHistory:
    """Simple path history manager which won't append the same path twice in a row."""

    def __init__(self, empty=""):
        self.data = [empty]
        self.idx = 0

    def getNext(self):
        if self.idx + 1 >= len(self.data): return self.data[0]
        self.idx = self.idx + 1
        return self.data[self.idx]

    def getPrev(self):
        if self.idx < 2: return self.data[0]
        self.idx = self.idx - 1
        return self.data[self.idx]

    def append(self, value):
        if self.data[0] == value: return
        if self.data[self.idx] != value: # if the previous entry is not the same
            self.idx = self.idx + 1
            self.data[self.idx:] = [value]

class SelectionTracker:
    """Handles wxListCtrl selection process.

    The EVT_LIST_ITEM_SELECTED and EVT_LIST_ITEM_DESELECTED handlers are invoked for every event
    that changes selection, possibly multiple times. In a list with multiple selection, when the
    user selects multiple items, the selection event is triggered for each item. For tousands of
    items it can cause problems. Therefore, BriefFileList handles selection in idle handler and
    selection events are (virtually) ignored. The problem is that EVT_LIST_BEGIN_LABEL_EDIT is
    not triggered alone when the user starts editing a list entry. Instead, *DESELECT and *SELECT
    are triggered with the same item - such a sequence is recorded and this class reports to the
    idle handler that no selection changed. Such masquerading is necessary becuase in case that a
    non-existant file's name is edited (it's been deleted outside of control slashManager) the
    idle handler cannot update the view by removing the non-existant file from the list - it will
    cause a seg-fault. Instead, the BEGIN_EDIT handler updates the list and vetoes the editing.
    For normal selection (no editing), idle handler checks for existance of files and updates the
    view accordingly.
    """
    def __init__(self): self.selAll = self.selSub = self.selAdd = ""
    def selections(self):
        if self.selAdd == self.selSub: return []
        l = [self.selAll]
        self.selAll = self.selSub = self.selAdd = ""
        return l
    def add(self, name):
        self.selAll = self.selAdd = name
    def sub(self, name):
        self.selAll = self.selSub = name

class BriefFileList(wxListCtrl):
    SORT_NAME = 1
    SORT_DATE = 2
    SORT_SIZE = 3
    SORT_TYPE = 4
    SORT_NONE = 5
    SORT_NAME_INSENSITIVE = 6
    def __init__(self, parent, hiddenDirs, hiddenFiles, statusBar, itemFunc, showHiddenFunc,
                 sortType=1, sortReverse=0):
        #style = wxLC_REPORT 
        #style = wxLC_ICON | wxLC_ALIGN_LEFT
        #style = wxLC_SMALL_ICON | wxLC_ALIGN_LEFT
        style = wxLC_LIST
        style = style | wxLC_EDIT_LABELS | wxNO_BORDER | wxSUNKEN_BORDER | wxTAB_TRAVERSAL
        wxListCtrl.__init__(self, parent, style=style)

        # this creates cyclic dependency (points to ancestor through bound method)
        # but the enclosing wxNotebook breaks the cycle when necessary
        self.itemFunc = itemFunc
        self.showHiddenFunc = showHiddenFunc
        self.statusBar = statusBar

        self.hiddenDirs = hiddenDirs
        self.hiddenFiles = hiddenFiles

        self.sortType = sortType
        self.sortReverse = sortReverse

        self.currentPath = None
        self.history = PathHistory()
        self.beginEditName = ""

        # popup menu id's
        self.popNew = wxNewId()
        self.popView = wxNewId()
        self.popOpen = wxNewId()
        self.popEdit = wxNewId()
        self.popOpenWith = wxNewId()
        self.popCopy = wxNewId()
        self.popCut = wxNewId()
        self.popPaste = wxNewId()
        self.popEject = wxNewId()
        self.popMount = wxNewId()
        self.popUnmount = wxNewId()
        self.popProps = wxNewId()
        self.popMoveCopy = wxNewId()

        client = wxART_TOOLBAR
        self.imageList = wxImageList(16, 16)
        self.imageIDs = {}
        for name in ("FOLDER", "FOLDER_LINK", "NORMAL_FILE", "LINK"):
            d = TheArtProvider.GetBitmap(getattr(TheArtProvider, name), client, (16, 16))
            self.imageIDs[name] = self.imageList.Add(d)
        self.SetImageList(self.imageList, wxIMAGE_LIST_SMALL)

        self.fsMenu = FSMenu("", self)
        self.popMenu = wxMenu()
        popMenu = self.popMenu

        for menuItem in (
            (self.popNew, "&New item"),
            (),
            (self.popView, "&View"),
            (self.popOpen, "&Open"),
            (self.popEdit, "&Edit"),
            (self.popOpenWith, "Open &with"),
            (),
            (self.popCopy, "&Copy"),
            (self.popCut, "C&ut"),
            (self.popPaste, "&Paste"),
            (),
            (self.popEject, "E&ject"),
            (self.popMount, "&Mount"),
            (self.popUnmount, "Unmoun&t"),
            (self.popProps, "P&roperties"),
            (),
            ):
            if len(menuItem) < 1:
                popMenu.AppendSeparator()
                continue

            mid = menuItem[0]
            txt = menuItem[1]
            popMenu.Append(mid, txt)
            popMenu.Enable(mid, false)
            EVT_MENU(self, mid, self.OnPopup)

        popMenu.Enable(self.popProps, true)
        popMenu.AppendMenu(self.popMoveCopy, "Move/Copy To", self.fsMenu)

        self.selectionTracker = SelectionTracker()

        # these two methods are called for each entry that changes selection (including user GUI
        # actions such as Shift+LeftClick) and so they should not do much work
        EVT_LIST_ITEM_SELECTED(self, self.GetId(), self.OnItemSelected)
        EVT_LIST_ITEM_DESELECTED(self, self.GetId(), self.OnItemDeSelected)

        EVT_LIST_ITEM_ACTIVATED(self, self.GetId(), self.OnActivated)
        EVT_LIST_ITEM_RIGHT_CLICK(self, self.GetId(), self.OnRightClick)
        EVT_LIST_BEGIN_LABEL_EDIT(self, self.GetId(), self.OnBeginEdit)
        EVT_LIST_END_LABEL_EDIT(self, self.GetId(), self.OnEndEdit)
        #EVT_LIST_KEY_DOWN(self, self.GetId(), self.OnKeyDown)
        #EVT_LIST_ITEM_FOCUSED(self, self.GetId(), self.OnKeyDown)
        # not implemented
        #txtCtrl = self.GetEditControl()

        # wx's popups occur on UP not DOWN event
        #EVT_RIGHT_DOWN(self, self.OnRightClick)
        # this process right click outside of any item
        #FIXME: learn to interact with normal list event processing
        EVT_RIGHT_UP(self, self.OnRightClick)

        self.UpdateStatusBar("", "", 1)

        EVT_IDLE(self, self.OnIdle)

    def OnIdle(self, evt):
        #print "idle", time.time()
        for name in self.selectionTracker.selections():
            self.OnItemSelectedName(name)
        # this call allows wxWindows to call its own idle handler to refresh wxListCtrl
        evt.Skip()

    def CleanUp(self): # this cleans up mess left over by various brain-dead actions
        self.beginEditName = "" # if editing action was in progress, mark it as over

    def OnKeyDown(self, event):
        self.CleanUp()
        event.Skip() # this function doesn't process this event
        return
        keyCode = event.GetKeyCode()
        print keyCode, WXK_ESCAPE
        event.Skip() # this function doesn't handle this event - wxListCtrl does its own handling

    def HistoryGo(self, event, direction): # direction (-1, 0, 1) 0 means up
        if self.beginEditName:
            event.Skip()
            return # cannot delete during list label editing

        if   -1 == direction: path = self.history.getPrev()
        elif +1 == direction: path = self.history.getNext()
        elif  0 == direction: path = os.path.dirname(self.currentPath)
        if not path or path == self.currentPath: return
        self.GoPath(path)

    def GoPath(self, path):
        self.CleanUp()
        # if hidden dirs switched off and the path contains hidden dirs
        if not self.hiddenDirs and string.find(os.path.normpath(path), "/.") >= 0:
            self.hiddenDirs = true
            self.showHiddenFunc(true)
        self.itemFunc(path)

    def GoHome(self): self.GoPath(os.path.expanduser("~"))

    def Refresh(self):
        """Updates the list's view and preserves the selection (if any is applicable after the
        update)."""

        items = self.GetSelectedItems()
        self.populateFromPath(self.currentPath)

        # convert items to dictionary
        ditems = {}
        for item in items: ditems[item] = 1


        # select items that were previously selected (provided they still exist)
        flags = wxLIST_STATE_SELECTED
        for i in range(self.GetItemCount()):
            name = self.GetItemText(i)
            path = os.path.join(self.currentPath, name)
            if ditems.has_key(path):
                self.SetItemState(i, flags, flags)

    def NewItem(self): # FIXME: this is supposed to create dirs, files, links
        self.CleanUp()
        c = 0
        while 1:
            c = c + 1
            path = os.path.join(self.currentPath, "NewDirectory" + str(c))
            if not os.path.exists(path): break
        try:
            os.mkdir(path)
            self.Refresh()
        except OSError, ex: MsgOS(ex, self)

    def CopyCutPaste(self, cmnd): # cmnd: 0, 1, 2
        self.CleanUp()
        global TheClipboard

        if   0 == cmnd: head = TransferDialog.COPY
        elif 1 == cmnd: head = TransferDialog.CUT
        else: # paste
            if TheClipboard:
                op = TheClipboard[0]
                items = TheClipboard[1]
                destPath = self.currentPath
                TransferItems(op, items, destPath)
                """
                if not os.path.exists(destPath) or not os.path.isdir(destPath):
                    wxMessageBox("Not a valid destination: " + destPath, "I/O Error",
                                 wxOK | wxICON_ERROR)
                    return
                dlg = TransferDialog(op, items, destPath)
                dlg.ShowModal()
                dlg.Destroy()
                """
                TheClipboard = None
                self.Refresh()
            return

        items = self.GetSelectedItems()
        if items: TheClipboard = (head, items)

    def GetSelectedItems(self, prependCurrentPath=1):
        l, i = [], -1
        while 1:
            i = self.GetNextItem(i, wxLIST_NEXT_ALL, wxLIST_STATE_SELECTED)
            if i < 0: break
            name = self.GetItemText(i)
            if ".." == name: continue
            if prependCurrentPath: path = os.path.join(self.currentPath, name)
            else: path = name
            l.append(path)
        return l

    def SelectItems(self, flag): # flag: -1 flip all, 0 deselect all, 1 select all
        self.CleanUp()
        allowedFlags = wxLIST_STATE_SELECTED
        for i in range(self.GetItemCount()):
            if 1 == flag: # select all
                flags = allowedFlags
            elif -1 == flag: # flip all
                flags = self.GetItemState(i, allowedFlags)
                flags = flags ^ allowedFlags
            else: # deselect all
                flags = 0
            self.SetItemState(i, flags, allowedFlags)

    def DeleteItems(self, event):
        if self.beginEditName:
            event.Skip()
            return # cannot delete during list label editing

        deletedCount = 0
        for f in self.GetSelectedItems():
            answer = wxMessageBox("Do you really want to delete `" + f + "'?",
                                  "Deletion confirmation",
                                  wxYES_NO | wxCANCEL | wxICON_QUESTION, self)
            if wxYES == answer:
                try:
                    os.remove(f)
                    deletedCount = deletedCount + 1
                except OSError: # maybe it's a directory
                    try:
                        #os.rmdir(f) # that needs an empty directory
                        shutil.rmtree(f) # FIXME: ask again
                        deletedCount = deletedCount + 1
                    except OSError, ex: MsgOS(ex, self)
            elif wxCANCEL == answer: break
        if deletedCount > 0: self.Refresh()

    def Properties(self):
        #FIXME: show sizes of selected files/directories; show FS info with a gauge
        items = self.GetSelectedItems()
        if items:
            ShowProperties(self, items, self.currentPath)
            return

        #FIXME: use bfree for root
        blk_size, fragment_size, blocks, bfree, bavail, files, ffree, favail, flag, namemax = \
               os.statvfs(self.currentPath)

        blkSize = long(fragment_size)
        avail = bavail * blkSize
        total = blocks * blkSize
        if total > 0: percent = 100.0 * avail / total
        else: percent = 0.0
        avail, availU = Bytes2SizeUnits(avail)
        total, totalU = Bytes2SizeUnits(total)
        msg = "File system information:\n" + \
              "Free disk space: %.1f %s (%4.1f%%)\n" % (avail, availU, percent) + \
              "Total disk space: %.1f %s\n" % (total, totalU)
        wxMessageBox(msg, "File system inforamtion", wxOK | wxICON_INFORMATION)

    def OnBeginEdit(self, event):
        name = event.GetLabel()
        
        path = os.path.join(self.currentPath, name)
        # if name doesn't exist
        if not os.path.exists(path):
            self.Refresh()
            event.Veto()
            return
        # if name's mssing, or is `..' or doesn't exist
        if not name or ".." == name:
            event.Veto()
            return
        self.beginEditName = name

    def OnEndEdit(self, event):
        name = event.GetLabel()
        oldName = self.beginEditName
        # checking `name' makes sure the name is not empty
        # checking `oldName' prevents from entering OnEndEdit() twice, see below
        if not name or not oldName:
            event.Veto()
            return

        curPath = self.currentPath
        oldPath = os.path.join(curPath, oldName)
        newPath = os.path.join(curPath, name)

        self.beginEditName = "" # OnEndEdit() is called twice if wxMessageBox() is called

        if oldPath == newPath: return

        deleteIndex = 0 # says wether a file has been deleted
        if os.path.exists(newPath): # renaming to existing file
            answer = wxMessageBox("File `" + name +
                                  "' already exists.\n" +
                                  "Do you really want to raname `" + oldName +
                                  "' to `" + name + "'?",
                                  "Renaming confirmation", wxYES_NO | wxICON_QUESTION, self)
            if wxYES != answer:
                event.Veto()
                return
            deleteIndex = 1

        try:
            os.rename(oldPath, newPath)
        except OSError, ex:
            MsgOS(ex, self)
            event.Veto()
        except:
            event.Veto()
            raise
        if deleteIndex:
            # the safest way is to reload the list, but it might be slow as the directory inode
            # has changed so dircache is invalid; it is faster to delete one item

            # the new item could be deleted (rather than the old one); this allows for
            # the sorting order to remain correct but it's impossible to delete an item that is
            # being edited
            #self.DeleteItem(event.GetIndex())

            # an advantage of deleting the old item is the "user perception" - the new name won't
            # disappear suddenly from under the cursor

            # look for old item (the one being change still has the old name)
            for i in range(self.GetItemCount()):
                txt = self.GetItemText(i)
                if txt == name: idx = i
            self.DeleteItem(idx)
        self.UpdateStatusBar(name)

    def OnActivated(self, event):
        self.CleanUp()

        name = event.GetLabel()
        self.OnActivatedName(event, name)

    def OnRightClick(self, event):
        self.CleanUp()

        if hasattr(event, "GetIndex"): # if generated by ListCtrl
            idx = event.GetIndex()
            position = self.GetItemPosition(idx)
        else: # if generated by wxWindow
            idx = 0
            position = event.GetPosition()
            itemId, flags = self.HitTest(position)
            if flags & (wxLIST_HITTEST_ONITEMICON | wxLIST_HITTEST_ONITEMLABEL):
                event.Skip()
                return
            #how to get focus?
            #allowedFlags = flags = wxLIST_STATE_FOCUSED
            #self.SetItemState(idx, flags, allowedFlags)

        popMenu = self.popMenu

        popMenu.Enable(self.popNew, false)
        popMenu.Enable(self.popCut, false)
        popMenu.Enable(self.popCopy, false)
        popMenu.Enable(self.popMount, false)
        popMenu.Enable(self.popMoveCopy, false)
        popMenu.Enable(self.popUnmount, false)

        selCount = self.GetSelectedItemCount() # number of selected items
        if selCount > 0: # if at least one, get the first one selected (to weed out `..')
            name = self.GetItemText(self.GetNextItem(-1, wxLIST_NEXT_ALL, wxLIST_STATE_SELECTED))
            path = os.path.join(self.currentPath, name)

        if selCount == 0: # no items selected
            popMenu.Enable(self.popNew, true)
            global TheClipboard
            if TheClipboard: popMenu.Enable(self.popPaste, true)
        else: # one or more items
            # only one selection and not a `..' (go-up item)
            if 1 == selCount and ".." != name:
                isMounted = os.path.ismount(path) # that says if path's mounted already
                if isMounted:
                    popMenu.Enable(self.popUnmount, true)
                else:
                    if IsMountPoint(path):
                        popMenu.Enable(self.popMount, true)

            # more than one selection or single, not a `..' (go-up item)
            if selCount > 1 or ".." != name:
                popMenu.Enable(self.popMoveCopy, true)
                popMenu.Enable(self.popCopy, true)
                popMenu.Enable(self.popCut, true)

        self.PopupMenu(popMenu, position)

    def OnPopup(self, event):
        #popMenu = event.GetEventObject()
        #popMenu.Remove(self.popMoveCopy)
        mid = event.GetId()
        if   self.popNew == mid: self.NewItem()
        elif self.popProps == mid: self.Properties()
        elif self.popCopy == mid: self.CopyCutPaste(0)
        elif self.popCut == mid: self.CopyCutPaste(1)
        elif self.popPaste == mid: self.CopyCutPaste(2)
        else:
            selCount = self.GetSelectedItemCount() # number of selected items
            if selCount > 0: # if at least one, get the first one selected (to weed out `..')
                name = self.GetItemText(self.GetNextItem(-1, wxLIST_NEXT_ALL, wxLIST_STATE_SELECTED))
                if ".." != name:
                    path = os.path.join(self.currentPath, name)

                    if   self.popMount == mid: cmd = 1
                    elif self.popUnmount == mid: cmd = -1
                    else: return

                    IsMountPoint(path, cmd)

    def OnActivatedName(self, event, name):
        #FIXME: warn about inaccessible dirs
        curPath = self.currentPath
        if ".." == name:
            fullPath = os.path.dirname(curPath)
        else:
            fullPath = os.path.join(curPath, name)
        if curPath != fullPath: # if not in / (root)
            self.itemFunc(fullPath)

        # self.Refresh() is not called here; self.itemFunc() will change directory
        # in parent and the parent will come back calling self.SetPath()

    def OnItemDeSelected(self, event):
        name = event.GetLabel()
        self.selectionTracker.sub(name)

    def OnItemSelected(self, event):
        name = event.GetLabel()
        self.selectionTracker.add(name)
        # cannot determine if Control was pressed - no way to do one-click activation
        #print event.GetMask(), event.GetKeyCode(), event.GetSelection()
        #print dir(event)

    def OnItemSelectedName(self, name):
        curPath = self.currentPath
        fullPath = os.path.join(curPath, name)
        if not os.path.exists(fullPath):
            self.Refresh()
            return

        #if os.path.isdir(fullPath): size = ""
        #else: size = "Size: " + str(os.path.getsize(fullPath))

        bytes, size, unit, selFiles = self.GetFileInfo()
        if unit: sizeStr = str(bytes) + " bytes (%.1f %s)" % (size, unit)
        else: sizeStr = str(bytes) + " bytes"

        statName = ""
        if len(selFiles) == 1:
            path = selFiles[0]
            statStr = "%s  %s %s " %  (sizeStr, "[%s %s %s]" % PermsUserGroup(path), mtime(path))
            statName = name
        elif len(selFiles) > 1:
            statName = "%d items" % len(selFiles)
            statStr = sizeStr
        else: statStr = ""

        self.UpdateStatusBar(statName, statStr, 1)

    def UpdateStatusBar(self, name0="", name1="", set=0):
        if not set:
            if not name0: name0 = self.statusStrings[0]
            if not name1: name1 = self.statusStrings[1]
        else:
            self.statusStrings = (name0, name1)

        self.statusBar.SetStatusText(name0, 0)
        self.statusBar.SetStatusText(name1, 1)
        if name0 != self.statusStrings[0] or name1 != self.statusStrings[1]:
            self.statusStrings = (name0, name1)

    def GetFileInfo(self):
        if self.GetSelectedItemCount() < 1: return 0, 0.0, "", []
        items = self.GetSelectedItems()

        bytes = 0L
        for path in items:
            try:
                if not os.path.isdir(path):
                    bytes = bytes + os.path.getsize(path)
            except OSError:
                pass

        size, units = Bytes2SizeUnits(bytes)

        return bytes, size, units, items

    def GetPath(self): return self.currentPath

    def SetPath(self, path):
        #FIXME: probably a time stamp should be checked whether directory changed, but for now
        #it's OK to assume that the user will refresh manually
        if path == self.currentPath: # don't make any changes if the new path is the same as old
            return

        self.UpdateStatusBar("", "", 1)
        self.CleanUp()
        self.populateFromPath(path)
        self.history.append(path)

    def GetShowHidden(self): # hidden directories shown?
        return self.hiddenDirs

    def GetShowHiddenFiles(self): return self.hiddenFiles

    def ToggleShowHidden(self):
        self.CleanUp()

        path = self.currentPath

        # hidden dirs are shown and there are hidden dirs in the current path - don't toggle
        if self.hiddenDirs and string.find(os.path.normpath(path), "/.") >= 0: return

        self.hiddenDirs = not self.hiddenDirs
        self.showHiddenFunc(self.hiddenDirs) # notify parent about change
        self.Refresh() # refresh display

    def ToggleShowHiddenFiles(self):
        self.CleanUp()
        self.hiddenFiles = not self.hiddenFiles
        self.Refresh()

    def GetSortType(self, getReverse=0):
        if getReverse:
            return self.sortReverse
        else:
            return self.sortType

    def SetSortType(self, sortType, reverse=0):
        if sortType not in (self.SORT_NAME, self.SORT_DATE, self.SORT_SIZE, self.SORT_TYPE,
                            self.SORT_NONE, self.SORT_NAME_INSENSITIVE):
            sortType = self.sortType
        self.sortType, oldType = sortType, self.sortType
        reverse = reverse and 1 or 0
        self.sortReverse, oldReverse = reverse, self.sortReverse
        
        if oldType != sortType or oldReverse != reverse: self.Refresh()

    def populateFromPath(self, path):
        self.CleanUp()
        self.DeleteAllItems()
        showHiddenDirs = self.hiddenDirs
        showHiddenFiles = self.hiddenFiles

        # this is in case `path' was deleted
        if not os.path.exists(path):
            # keep going up the dir tree until an existing path is found
            while not os.path.exists(path): path = apply(os.path.join, os.path.split(path)[:-1])

            #FIXME
            #DirCtrlSetPath(self.dirCtrl, path)
            self.itemFunc(path)
            return

        self.currentPath = path

        # dircache keeps returning the same list (any changes to the list will
        # be carried into the future, until the content of directory changes -
        # mtime changes - when a totally new list is generated)
        pathList = dircache.listdir(path)

        pathList = pathList[:] # make a copy

        if self.SORT_NAME == self.sortType:   pathList.sort() # sort (rely on locale)
        elif self.SORT_NAME_INSENSITIVE == self.sortType:
            pathList.sort(lambda a, b: cmp(string.lower(a), string.lower(b)))
        elif self.SORT_DATE == self.sortType: pathList.sort(lambda a, b, p=path, os=os:-cmp(
                os.path.getmtime(os.path.join(p,a)),
                os.path.getmtime(os.path.join(p,b))
                ))
        elif self.SORT_SIZE == self.sortType: pathList.sort(lambda a, b, p=path, os=os:-cmp(
                os.path.getsize(os.path.join(p,a)),
                os.path.getsize(os.path.join(p,b))
                ))
        elif self.SORT_TYPE == self.sortType: pathList.sort(lambda a, b, os=os:cmp(
                (os.path.splitext(a)[1], a),
                (os.path.splitext(b)[1], b)
                ))
        #else: # leave unsorted
            #pass

        if self.sortReverse: pathList.reverse()

        idx = 0
        # if there is more than `/' (os.path.realpath() is a good idea but it's in Python 2.2)
        if not os.path.samefile(path, '/'):
            # insert `..' to go up
            iid = self.imageIDs["FOLDER"]
            self.InsertImageStringItem(0, "..", iid)
            idx = 1

        allIdx = dirIdx = idx
        for name in pathList:
            fullPath = os.path.join(path, name)
            isDir = os.path.isdir(fullPath)

            if isDir:
                if name[0] == ".":
                    if not showHiddenDirs: continue
                # FIXME: create a better icon
                if os.path.islink(fullPath): iid = self.imageIDs["FOLDER_LINK"]
                else: iid = self.imageIDs["FOLDER"]
                idx = dirIdx
                dirIdx = dirIdx + 1
            else:
                if name[0] == ".":
                    if not showHiddenFiles: continue

                if os.path.islink(fullPath): iid = self.imageIDs["LINK"]
                else: iid = self.imageIDs["NORMAL_FILE"]

                idx = allIdx

            self.InsertImageStringItem(idx, name, iid)
            allIdx = allIdx + 1

    def __del__(self): print "Deleting tab", self.currentPath

class smNotebook(wxNotebook):
    def __init__(self, parent, id, statusBar, itemFunc, showHiddenFunc, paths):
        wxNotebook.__init__(self, parent, id)

        # cyclic dependency: parent <-> child (but there is only one notebook)
        self.statusBar = statusBar
        self.itemFunc = itemFunc
        self.showHiddenFunc = showHiddenFunc

        self.menuDup = wxNewId()
        self.menuDel = wxNewId()
        self.menuHiddenDirs = wxNewId()
        self.menuHiddenFiles = wxNewId()
        self.menuSort = wxNewId()
        self.menuSname = wxNewId()
        self.menuSdate = wxNewId()
        self.menuSsize = wxNewId()
        self.menuStype = wxNewId()
        self.menuSnone = wxNewId()
        self.menuSiname = wxNewId()
        self.menuSreverse = wxNewId()
        self.menuDirs = wxNewId()
        self.menuDfirst = wxNewId()
        self.menuDfirst = wxNewId()
        self.menuDfirst = wxNewId()

        for path in paths:
            path = os.path.abspath(os.path.expanduser(path))
            if not os.path.exists(path) or not os.path.isdir(path):
                continue
            page = BriefFileList(self, false, false, statusBar, itemFunc, showHiddenFunc)
            self.AddPage(page, os.path.basename(path) or "/")
            page.SetPath(path)

        EVT_RIGHT_UP(self, self.OnRightClick)
        EVT_NOTEBOOK_PAGE_CHANGED(self, self.GetId(), self.OnPageChanged)

    # these are just wrappers for the file list methods
    def HistoryGo(self, event, direction):
        self.GetPage(self.GetSelection()).HistoryGo(event, direction)
    def GoHome(self): self.GetPage(self.GetSelection()).GoHome()
    def NewItem(self): self.GetPage(self.GetSelection()).NewItem()
    def Refresh(self): self.GetPage(self.GetSelection()).Refresh()
    def CopyCutPaste(self, cmnd): self.GetPage(self.GetSelection()).CopyCutPaste(cmnd)
    def SelectItems(self, flag): self.GetPage(self.GetSelection()).SelectItems(flag)
    def DeleteItems(self, event): self.GetPage(self.GetSelection()).DeleteItems(event)
    def Properties(self): self.GetPage(self.GetSelection()).Properties()

    # this is illegal: causes SEGFAULT (used internally by wxPython)
    # unknown attribute inquiries go to the current page
    #def __getattr__(self, name): return getattr(self.GetPage(self.GetSelection()), name)

    def SetPath(self, path):
        sel = self.GetSelection()
        self.SetPageText(sel, os.path.basename(path) or "/")
        self.GetPage(sel).SetPath(path)

    def OnPageChanged(self, event):
        # change menus to reflect hidden dirs/files, sorting order
        sel = self.GetSelection()
        curPage = self.GetPage(sel)
        curPage.UpdateStatusBar()
        path = curPage.GetPath() # path is cached locally

        # make sure that hidden files/dirs are set properly
        self.showHiddenFunc(curPage.GetShowHidden()) # this call could change curPage.GetPath()!

        self.itemFunc(path)

    def OnRightClick(self, event):
        position = event.GetPosition()
        #print self.HitTest(position) #-> 10
        #event.Skip()
        #how to get focus?
        sel = self.GetSelection()
        curPage = self.GetPage(sel)

        sortMenu = wxMenu()
        for menuItem in (
           (self.menuSname, "&Name", curPage.SORT_NAME),
           (self.menuSdate, "&Date", curPage.SORT_DATE),
           (self.menuSsize, "&Size", curPage.SORT_SIZE),
           (self.menuStype, "&Type", curPage.SORT_TYPE),
           (self.menuSiname, "&Name (case-insensitive)", curPage.SORT_NAME_INSENSITIVE),
           (self.menuSnone, "&Unsorted", curPage.SORT_NONE)):
            id, txt, c = menuItem
            sortMenu.Append(id, txt, "", wxITEM_RADIO)
            if curPage.GetSortType() == c: sortMenu.Check(id, true)
            else:
                sortMenu.Check(id, false)
                EVT_MENU(self, id,
                         lambda e,self=self,c=c:self.GetPage(self.GetSelection()).SetSortType(c))

        # add "reverse" check
        sortMenu.AppendSeparator()
        mid = self.menuSreverse
        c = curPage.GetSortType()
        t = curPage.GetSortType(1)
        sortMenu.Append(mid, "&Reverse order", "Sort in reversed order", wxITEM_CHECK)
        if t:
            sortMenu.Check(mid, true)
            t = 0
        else:
            sortMenu.Check(mid, false)
            t = 1
        EVT_MENU(self, mid,
                 lambda e,s=self,c=c, t=t:s.GetPage(s.GetSelection()).SetSortType(c, t))

        dirsMenu = wxMenu()
        for menuItem in (
           (self.menuDfirst, "&First"),
           (self.menuDfirst, "&Last"),
           (self.menuDfirst, "&Mixed")):
            mid = menuItem[0]
            txt = menuItem[1]
            dirsMenu.Append(mid, txt, "", wxITEM_RADIO)

        popMenu = wxMenu()
        for menuItem in ((self.menuDup, "&Clone tab"),
           (self.menuDel, "&Delete tab"),
           (),
           (self.menuSort, "&Sort by ...", sortMenu),
           (self.menuDirs, "D&irectories are ...", dirsMenu),
           (self.menuHiddenDirs, "Hidden di&rectories", "Toggle view of hidden directories", wxITEM_CHECK),
           (self.menuHiddenFiles, "Hidden &files", "Toggle view of hidden files", wxITEM_CHECK)):
            if len(menuItem) < 2:
                popMenu.AppendSeparator()
                continue
            mid = menuItem[0]
            txt = menuItem[1]
            if len(menuItem) == 2: popMenu.Append(mid, txt)
            elif len(menuItem) == 3:
                subMenu = menuItem[2]
                popMenu.AppendMenu(mid, txt, subMenu)
            else:
                tip = menuItem[2]
                type_ = menuItem[3]
                popMenu.Append(mid, txt, tip, type_)

        if self.GetPageCount() < 2: popMenu.Enable(self.menuDel, false)
        if curPage.GetShowHidden(): popMenu.Check(self.menuHiddenDirs, true)
        if curPage.GetShowHiddenFiles(): popMenu.Check(self.menuHiddenFiles, true)

        EVT_MENU(self, self.menuDup, self.OnDuplicate)
        EVT_MENU(self, self.menuDel, lambda e, self=self: self.DeletePage(self.GetSelection()))
        EVT_MENU(self, self.menuHiddenDirs, lambda e, self=self: self.GetPage(self.GetSelection()).ToggleShowHidden())
        EVT_MENU(self, self.menuHiddenFiles, lambda e, self=self: self.GetPage(self.GetSelection()).ToggleShowHiddenFiles())

        self.PopupMenu(popMenu, position)

    def OnDuplicate(self, event):
        sel = self.GetSelection()
        curPage = self.GetPage(sel)
        curPath = curPage.GetPath()
        newPage = BriefFileList(self, curPage.GetShowHidden(), curPage.GetShowHiddenFiles(),
                                self.statusBar, self.itemFunc, self.showHiddenFunc,
                                curPage.GetSortType(), curPage.GetSortType(1))
        path = curPage.GetPath()
        if self.AddPage(newPage, os.path.basename(path) or "/"): newPage.SetPath(path)

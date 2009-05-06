#! /usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; fill-column: 79; coding: iso-latin-1-unix -*-
#

import dircache, os

from wxPython.wx import wxNewId, false, true, wxNewId
from wxPython.wx import EVT_MENU, EVT_MENU_OPEN, EVT_MENU_CLOSE, EVT_MENU_HIGHLIGHT, EVT_MENU_HIGHLIGHT_ALL
from wxPython.wx import EVT_CLOSE, EVT_BUTTON
from wxPython.wx import wxMenu, wxFrame, wxButton, wxStaticText
from wxPython.wx import wxBoxSizer, wxHORIZONTAL, wxVERTICAL, wxEXPAND

from transfer import TransferDialog, TransferItems

class FSMenu(wxMenu):
    def __init__(self, path, ilist):
        wxMenu.__init__(self)

        self.path = path
        self.pathList = []

        # this creates circular reference but it doesn't seem to matter with wxPython
        # all is cleaned up at the end, even Python-side __del__() methods are called
        self.ilist = ilist

        self.btnMv = wxNewId()
        self.btnCp = wxNewId()
        self.btnCancel = wxNewId()

        if not path:
            self.menus = [[-1, "Home", "~"], [-1, "/", "/"]]
            for p in self.menus:
                mid = wxNewId()
                p[0] = mid
                pth = os.path.expanduser(p[2])
                p[2] = pth
                menu = FSMenu(pth, ilist)
                self.AppendMenu(mid, p[1], menu)
                p.append(menu)
        else:
            self.menus = []
            mid = wxNewId()
            self.Append(mid, "Move/Copy Here")
            self.AppendSeparator()
            EVT_MENU(self, mid, self.moveCopy)

        EVT_MENU_OPEN(self, self.OnMenuOpen)
        EVT_MENU_CLOSE(self, self.OnMenuClose)
        EVT_MENU_HIGHLIGHT(self, -1, self.OnMenuHighlight)
        EVT_MENU_HIGHLIGHT_ALL(self, self.OnMenuHighlightAll)

    def OnMenuOpen(self, event):
        print "Open"
    def OnMenuClose(self, event):
        print "Close"
    def OnMenuHighlight(self, event):
        print "Highlite"

    def OnMenuHighlightAll(self, event):
        eid = event.GetMenuId()
        #print "HighliteAll", eid

        for l in self.menus:
            mid, n, path, menu = l
            if eid == mid:
                menu.populate()

    def populate(self):
        pathList = dircache.listdir(self.path)
        if self.pathList == pathList:
            return

        for m in self.menus:
            mid = m[0] 
            self.Delete(mid)

        self.menus = []

        self.pathList = pathList

        for p in pathList:
            fullPath = os.path.join(self.path, p)
            if not os.path.isdir(fullPath) or "." == p[0]:
                continue
            nid = wxNewId()
            menu = FSMenu(fullPath, self.ilist)
            self.AppendMenu(nid, p, menu)
            self.menus.append([nid, p, fullPath, menu])

    def moveCopy(self, event):
        print "Moving"
        destPath = self.path
        frame = wxFrame(self.ilist, wxNewId(), "Move/Copy Items?")

        mSizer = wxBoxSizer(wxVERTICAL)

        frame.SetAutoLayout(true)
        frame.SetSizer(mSizer)

        count = self.ilist.GetSelectedItemCount() # number of selected items
        mSizer.Add(30, 10, 0, wxEXPAND)
        mSizer.Add(wxStaticText(frame, wxNewId(), "Move/Copy %d item(s)?" % count), 0, 0)
        mSizer.Add(30, 10, 0, wxEXPAND)

        bSizer = wxBoxSizer(wxHORIZONTAL)
        mSizer.Add(bSizer, 0, 0)
        mSizer.Add(30, 10, 0, wxEXPAND)

        btnMv = wxButton(frame, self.btnMv, "Move")
        btnCp = wxButton(frame, self.btnCp, "Copy")
        btnCancel = wxButton(frame, self.btnCancel, "Cancel")
        for b in (btnMv, btnCp, btnCancel):
            EVT_BUTTON(b, b.GetId(), self.OnButtonPress)

        bSizer.Add(btnMv, 1, 0)
        bSizer.Add(30, 10, 0, wxEXPAND)
        bSizer.Add(btnCp, 1, 0)
        bSizer.Add(30, 10, 0, wxEXPAND)
        bSizer.Add(btnCancel, 1, 0)

        frame.MakeModal(true)
        frame.Show(true)

        self.frame = frame
        EVT_CLOSE(frame, self.OnCloseWindow)

    def OnCloseWindow(self, event):
        self.frame.MakeModal(false)
        self.frame.Destroy()

    def OnButtonPress(self, event):
        btn = event.GetEventObject()
        bid = btn.GetId()

        self.frame.Close()

        if bid == self.btnCancel:
            pass
        else:
            if bid == self.btnMv:
                op = TransferDialog.CUT
            elif bid == self.btnCp:
                op = TransferDialog.COPY
            else:
                return

            items = self.ilist.GetSelectedItems()
            destPath = self.path
            TransferItems(op, items, destPath)

            # a refresh is necessary even for coping because a copy can be made in the
            # current directory in which case we have *-orig1 file created
            self.ilist.Refresh()

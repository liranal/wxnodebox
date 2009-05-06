#! /usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; fill-column: 79; coding: iso-latin-1-unix -*-
#
# Tested with Python 2.2, wxWindows 2.4.0, and wxPython 2.4.0.7

import sys
import os

from wxPython.wx import true, false, wxNewId, wxSize
from wxPython.wx import EVT_BUTTON, EVT_IDLE
from wxPython.wx import wxBoxSizer, wxButton, wxDialog, wxGauge, wxListCtrl, wxStaticText
from wxPython.wx import wxALL, wxALIGN_CENTRE, wxEXPAND, wxLEFT, wxVERTICAL
from wxPython.wx import wxCAPTION, wxSYSTEM_MENU, wxRESIZE_BORDER
from wxPython.wx import wxLC_REPORT, wxLIST_AUTOSIZE, wxLIST_FORMAT_RIGHT, wxLIST_FORMAT_LEFT
from wxPython.lib.rcsizer import RowColSizer

from utils import Bytes2SizeUnits, mtime, PermsFromPath, UserFromPath, GroupFromPath

class PropertiesDialog(wxDialog):
    def __init__(self, parent, items, prfx):
        self.items = items

        style = wxCAPTION | wxSYSTEM_MENU | wxRESIZE_BORDER
        wxDialog.__init__(self, parent, wxNewId(), "Properties " + prfx, size=wxSize(750,400),
                          style=style)

        sizer = RowColSizer()
        self.sizer = sizer
        self.SetSizer(sizer)
        self.SetAutoLayout(true)

        btn = wxButton(self, wxNewId(), "OK")
        EVT_BUTTON(self, btn.GetId(), lambda e, self=self: self.Destroy())

        bsizer = wxBoxSizer(wxVERTICAL)
        for t in ("Show MD5 sums", "Same units"):
            b = wxButton(self, wxNewId(), t)
            b.Enable(false)
            bsizer.Add(b, 0, wxEXPAND, 0)

        self.PopulateList()

        flags = wxEXPAND | wxALL
        bb = 10
        sizer.Add(self.list, row=1, col=1, flag=flags)
        sizer.Add(btn, row=3, col=1, flag=wxALIGN_CENTRE, colspan=2)

        sizer.Add(bsizer, row=1, col=2)

        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(1)

        sizer.AddSpacer(10,10, pos=(2,1))

    def PopulateList(self):
        self.list = wxListCtrl(self, wxNewId(), style=wxLC_REPORT)
        i = 0
        for t in (("Name", wxLIST_FORMAT_LEFT),
                  ("Size", wxLIST_FORMAT_RIGHT),
                  ("Size on disk", wxLIST_FORMAT_RIGHT),
                  ("Permissions", wxLIST_FORMAT_LEFT),
                  ("User", wxLIST_FORMAT_LEFT),
                  ("Group", wxLIST_FORMAT_LEFT),
                  ("Modification time", wxLIST_FORMAT_LEFT)):
            n, f = t
            self.list.InsertColumn(i, n, f)
            #self.list.SetColumnWidth(i, wxLIST_AUTOSIZE)
            i = i + 1

        for i in range(len(self.items)):
            path = self.items[i]
            name = os.path.basename(path)

            size, diskSize = self.PathSizes(path)

            self.list.InsertStringItem(i, name)
            try:
                self.list.SetStringItem(i, 1, size)
                self.list.SetStringItem(i, 2, diskSize)
                self.list.SetStringItem(i, 3, PermsFromPath(path))
                self.list.SetStringItem(i, 4, UserFromPath(path))
                self.list.SetStringItem(i, 5, GroupFromPath(path))
                self.list.SetStringItem(i, 6, mtime(path))
            except OSError:
                pass

    def PathSizes(self, path):
        bytes, diskBytes = DeepSize(path)

        size, unit = Bytes2SizeUnits(bytes)
        diskSize, diskUnit = Bytes2SizeUnits(diskBytes)

        if not unit: unit = " B"
        if not diskUnit: diskUnit = " B"

        fmt = "%.1f "
        return fmt % size + unit, fmt % diskSize + diskUnit

def ShowProperties(parent, items, prfx=""):
    dlg = PropertiesDialog(parent, items, prfx)
    dlg.Show()

def DirVisitor(sizeList, dirname, items):
    for name in items:
        fullPath = os.path.join(dirname, name)
        blkSize = sizeList[2]
        #FIXME: create a list of OS complaints and pass it on
        try:
            itemSize = os.path.getsize(fullPath)
        except OSError:
            itemSize = 0

        sizeList[0] = sizeList[0] + itemSize

        blkCount = (itemSize + blkSize - 1) / blkSize # round up
        sizeList[1] = sizeList[1] + blkCount * blkSize
        #if os.path.isdir(fullPath): continue

def DeepSize(path):
    if not os.path.exists(path): return 0L, 0L
    if not os.path.isdir(path):
        try:
            size = long(os.path.getsize(path))
        except OSError:
            size = 0
        return size, size

    blkSize = long(os.statvfs(path)[0])
    sizeList = [0L, 0L, blkSize]
    os.path.walk(path, DirVisitor, sizeList)

    return sizeList[0], sizeList[1]

from wxPython.wx import wxApp, wxFrame, wxButton, EVT_BUTTON

class TheApp(wxApp):
    def __init__(self, func, data):
        self.func = func
        self.data = data
        wxApp.__init__(self, 0)

    def OnInit(self):
        frame = wxFrame(None, wxNewId(), "wxApp")
        frame.Show(true)
        self.frame = frame
        self.SetTopWindow(frame)
        btn = wxButton(frame, wxNewId(), "Click to Start")
        EVT_BUTTON(self, btn.GetId(), self.OnClick)
        return true

    def OnClick(self, event):
        self.func(self.frame, self.data)

def main(argv):
    if len(argv) < 2: return 0

    app = TheApp(ShowProperties, argv[1:])
    app.MainLoop()

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

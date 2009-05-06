#! /usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; fill-column: 79; coding: iso-latin-1-unix -*-
#

import os, shutil

from wxPython.wx import true, false, wxNewId
from wxPython.wx import EVT_BUTTON, EVT_IDLE
from wxPython.wx import wxALL, wxALIGN_CENTRE, wxEXPAND, wxLEFT, wxVERTICAL
from wxPython.wx import wxBoxSizer, wxButton, wxDialog, wxGauge, wxStaticText
from wxPython.wx import wxOK, wxICON_ERROR, wxMessageBox

def MoveToDir(src, dst):
    if os.path.dirname(src) == dst: return
    print "Move", src, dst
    dstName = os.path.join(dst, os.path.basename(src))
    try: os.rename(src, dstName)
    except OSError:
        if os.path.isdir(src):
            shutil.copytree(src, dst, symlinks=True)
            shutil.rmtree(src)
        else:
            shutil.copy2(src,dst)
            shutil.os.unlink(src)

def CopyToDir(item, dst):
    basename = os.path.basename(item)

    if os.path.samefile(os.path.dirname(item), dst):
        if os.path.isdir(item): return #FIXME: shutil.copytree() can't do it, do it yourself
        c = 0
        while 1:
            c = c + 1
            # add a suffix `origN' (adding a prefix might put the new name away due to sorting)
            dst = os.path.join(dst, basename + "-orig%d" % c)
            if not os.path.exists(dst): break
    print "Copy", item, dst #FIXME: make copies in same dir with user permission
    if os.path.isdir(item):
        # create destination name
        dstDir = os.path.join(dst, basename)
        shutil.copytree(item, dstDir)
    else: shutil.copy(item, dst)

class TransferDialog(wxDialog):
    COPY = 1
    CUT = 2
    def __init__(self, op, fsoList, destPath):
        self.stopped = false
        self.InTransfer = false

        self.op = op
        if self.COPY == op: txt = "Copy"
        else: txt = "Move"

        self.fsoList = fsoList
        self.destPath = os.path.normpath(destPath)

        wxDialog.__init__(self, None, wxNewId(), txt + " operation")
        sizer = wxBoxSizer(wxVERTICAL)
        self.SetAutoLayout(true)
        self.SetSizer(sizer)
        self.sizer = sizer
        btn = wxButton(self, wxNewId(), "Stop")
        EVT_BUTTON(self, btn.GetId(), self.OnClick)

        self.txt1 = wxStaticText(self, wxNewId(), "Destination directory: ")
        self.txt2 = wxStaticText(self, wxNewId(), destPath)
        #self.txt = wxStaticText(self, wxNewId(), "Single object progress:")
        #self.gauge = wxGauge(self, wxNewId(), 100)
        self.txtAll = wxStaticText(self, wxNewId(), "Overall progress:")
        self.gaugeAll = wxGauge(self, wxNewId(), len(fsoList))

        flags = wxEXPAND | wxALL
        border = 0
        bb = 10
        sizer.Add(2 * bb, 2 * bb) # separator
        sizer.Add(self.txt1, 0, wxLEFT, border)
        sizer.Add(self.txt2, 0, wxLEFT, border)
        sizer.Add(bb, bb) # separator
        #sizer.Add(self.txt, 0, wxLEFT, border)
        #sizer.Add(bb, bb) # separator
        #sizer.Add(self.gauge, 0, flags, border)
        #sizer.Add(bb, bb) # separator
        sizer.Add(self.txtAll, 0, wxLEFT, border)
        sizer.Add(bb, bb) # separator
        sizer.Add(self.gaugeAll, 0, flags, border)
        sizer.Add(bb, bb) # separator
        sizer.Add(btn, 0, wxALIGN_CENTRE, border)
        sizer.Add(2 * bb, 2 * bb) # separator
        sizer.Layout()
        self.Refresh()

        EVT_IDLE(self, self.OnIdle)

    def OnIdle(self, event):
        if not self.stopped:
            if not self.InTransfer:
                self.InTransfer = true
                self.DoTransfer(None)
                self.InTransfer = false
            event.RequestMore(true)
            self.Refresh()
            return
        self.EndModal(0)

    def OnClick(self, event): self.stopped = 1

    def DoTransfer(self, event):
        while 1:
            # in case there were non-existent items on the list of items to move
            if self.stopped: return

            # move on to the next item
            v = self.gaugeAll.GetValue() + 1
            if v >= self.gaugeAll.GetRange(): self.stopped = true

            self.gaugeAll.SetValue(v)
            o = os.path.normpath(self.fsoList[v-1])
            if not os.path.exists(o): continue
            break
        try:
            if self.COPY == self.op:
                CopyToDir(o, self.destPath)
            else:
                MoveToDir(o, self.destPath)
        except OSError: pass #FIXME: issue a warning

def TransferItems(op, items, destPath):
    if not os.path.exists(destPath) or not os.path.isdir(destPath):
        wxMessageBox("Not a valid destination: " + destPath, "I/O Error",
                     wxOK | wxICON_ERROR)
        return -1
    dlg = TransferDialog(op, items, destPath)
    dlg.ShowModal()
    dlg.Destroy()
    return 0

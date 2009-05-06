#! /usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; fill-column: 79; coding: iso-latin-1-unix -*-
#

import commands, os, string

from wxPython.wx import false, true, wxHSCROLL, wxVSCROLL, wxEXPAND, wxALL, wxALIGN_CENTRE, wxVERTICAL
from wxPython.wx import wxTE_READONLY, wxTE_MULTILINE, wxTE_DONTWRAP
from wxPython.wx import wxDefaultPosition, wxDefaultSize
from wxPython.wx import wxBitmapFromImage
from wxPython.wx import wxBoxSizer, wxButton, wxEmptyImage, wxFrame, wxScrolledWindow, wxSize, \
     wxStaticBitmap, wxTextCtrl
from wxPython.html import wxHtmlWindow

from utils import MsgOS

def OpenFile(parent, path):
    #FIXME: support: svg, sgvz, svg.gz with rsvg or batik (render to temporary
    #file /tmp/<PID><time()><atime(f.svg>.png and then open a frame)

    if not os.path.exists(path) or os.path.isdir(path): return
    frame = wxFrame(parent, -1, "File view: " + path, wxDefaultPosition, wxSize(500, 400))

    handled = 0
    needFrame = 1
    lowerPath = string.lower(path)
    #for animations or to see if count is > 0:
    #wxImage_GetImageCount(path)
    if lowerPath[-3:] in ("ani", "bmp", "cur", "gif", "ico", "iff", "jpg", "pcx", "png", "pnm", \
                          "tif", "xpm") or lowerPath[-4:] in ("jpeg", "tiff"):
        #f = open(path, "rb"); data = f.read(); f.close()
        #stream = StringIO(data)
        #img = wxImageFromStream(stream)
        img = wxEmptyImage()
        img.LoadFile(path)
        bmp = wxBitmapFromImage(img)
        #wxStaticBitmap(frame, -1, bmp) #, (15, 45))

        width, height = img.GetWidth(), img.GetHeight()
        if width and height:
            sw = wxScrolledWindow(frame, -1, wxDefaultPosition, wxDefaultSize,
                                  wxHSCROLL | wxVSCROLL)
            #sw.SetScrollbars(20, 20, img.GetWidth()/20, img.GetHeight()/20)
            sw.SetVirtualSize(wxSize(width, height))
            sw.SetScrollRate(20, 20)
            wxStaticBitmap(sw, -1, bmp) #, (15, 45))
            w, h = 800, 600 #frame.GetSize()
            w, h = min(w, width), min(h, height)
            minSize, b = 100, 10
            if w < minSize: w = minSize
            if h < minSize: h = minSize
            frame.SetSize(wxSize(w+b, h+b))
            handled = 1
    elif "html" == lowerPath[-4:] or "htm" == path[-3:]:
        htmlWin = wxHtmlWindow(frame)
        htmlWin.LoadPage(path)
        handled = 1
    elif "pdf" == lowerPath[-3:]:
        for cmd in ("xpdf", "acroread"):
            #FIXME: handle names that contain spaces etc.
            status, output = commands.getstatusoutput(cmd + " " + path)
            if 0 == status:
                handled = 1
                needFrame = 0
                break
    #FIXME: mplayer cannot run in background; same goes for Python calling mplayer externally - probably stdin dependence
    elif "mpeg" == lowerPath[-4:] or \
         lowerPath[-3:] in ("asf", "avi", "mov", "mpa", "mpg", "wmv"):
        for cmd in ("mplayer -quiet",):
            #FIXME: handle names that contain spaces etc.
            status, output = commands.getstatusoutput(cmd + " " + path)
            if 0 == status:
                handled = 1
                needFrame = 0
                break

    elif "ps" == lowerPath[-2:] or "ps.gz" == lowerPath[-5:]:
        pid = os.fork()
        if 0 == pid:
            for cmd in ("ggv", "gv"):
                try:
                    os.execlp(cmd, cmd, path)
                except OSError:
                    pass
            os.exit(1)
        handled = 1
        needFrame = 0

    if not handled:
        minSize = 65536
        try:
            f = open(path, "rb"); data = f.read(minSize); f.close()
        except IOError, ex:
            MsgOS(ex)
            return None
        txt = wxTextCtrl(frame, -1, data,
                         style=wxTE_READONLY|wxTE_MULTILINE|wxTE_DONTWRAP|wxHSCROLL)
        if len(data) == minSize:
            sizer = wxBoxSizer(wxVERTICAL)
            frame.SetAutoLayout(true)
            frame.SetSizer(sizer)
            frame.sizer = sizer
            b = wxButton(frame, -1, "Show entire file")
            sizer.Add(txt, 1, wxEXPAND|wxALL, 0)
            sizer.Add(b, 0, wxALIGN_CENTRE, 0)
            sizer.Layout()
    #txt = wxStaticText(frame, -1, path, wxDefaultPosition, wxDefaultSize, wxST_NO_AUTORESIZE, data)

    if needFrame:
        frame.CenterOnScreen()
        frame.Show(True)
        return frame

#FIXME: handle child processes
class ProcessManager:
    def OpenFile(self, parent, path): OpenFile(parent, path)
    def OnAppExit(self):
        """Called on exit - should wait for children processes?"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
import wx
import wx.aui
import wx.grid
import os, sys
#----------------------------------------------------------------------------
class MyFrame(wx.Frame):
def __init__(self, parent, id=-1, title='wx.aui Test',
size=(800, 600), style=wx.DEFAULT_FRAME_STYLE):
wx.Frame.__init__(self, parent, id, title, (0,0), size, style)

self._mgr = wx.aui.AuiManager(self)
mb = wx.MenuBar()
file_menu = wx.Menu()
file_menu.Append(wx.ID_OPEN, "Open")
file_menu.Append(wx.ID_EXIT, "Exit")
mb.Append(file_menu, "File")
self.SetMenuBar(mb)

self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
self.statusbar.SetStatusWidths([-2, -3])
self.statusbar.SetStatusText("Ready", 0)
self.statusbar.SetStatusText("Welcome To wxPython!", 1)

self.tc = MyTreeCtrl(self, -1)
# create several text controls
# add the panes to the manager
self._mgr.AddPane(self.tc, wx.aui.AuiPaneInfo().
Name("test7").Caption("Client Size Reporter").

Left().Layer(1).CloseButton(True).MaximizeButton(True))

self._mgr.AddPane(self.CreateGrid(),
wx.aui.AuiPaneInfo().Name("grid_content").
CenterPane())
# tell the manager to 'commit' all the changes just made
self._mgr.Update()

self.Bind(wx.EVT_MENU, self.OpenFile, id=wx.ID_OPEN)
self.Bind(wx.EVT_CLOSE, self.OnClose)
self.Bind(wx.EVT_MENU, self.OnClose, id=wx.ID_EXIT)


def OnClose(self, event):
# deinitialize the frame manager
self._mgr.UnInit()
# delete the frame
self.Destroy()


def OpenFile(self, evt):
wildcard = "Sphinx QUE (*.que)|*.que|"\
"All files (*.*)|*.*"
self.statusbar.SetStatusText("CWD: %s\n" % os.getcwd())

dlg = wx.FileDialog(
self, message="Choose a file",
defaultDir=os.getcwd(),
defaultFile="",
wildcard=wildcard,
style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
)

if dlg.ShowModal() == wx.ID_OK:
paths = dlg.GetPaths()

self.statusbar.SetStatusText('You selected %d files:' %
len(paths))

for path in paths:
self.statusbar.SetStatusText(' %s\n' % path)

dir = os.path.split(path)[0]
file = os.path.split(path)[1]

self.statusbar.SetStatusText("%s\n" % path)
self.tc.populateTreeCtrl({})
self._mgr.Update()



def CreateGrid(self):

grid = wx.grid.Grid(self, -1, wx.Point(0, 0), wx.Size(150, 250),
wx.NO_BORDER | wx.WANTS_CHARS)
grid.CreateGrid(50, 20)

return grid

class MyTreeCtrl(wx.TreeCtrl):
def __init__(self, parent,id=wx.ID_ANY, pos=wx.DefaultPosition,
size=wx.DefaultSize,
style=wx.TR_DEFAULT_STYLE |
wx.NO_BORDER):
wx.TreeCtrl.__init__(self, parent, id, pos, size, style)
imglist = wx.ImageList(16, 16, True, 2)
imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,
wx.ART_OTHER, wx.Size(16,16)))
imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE,
wx.ART_OTHER, wx.Size(16,16)))
self.AssignImageList(imglist)

def populateTreeCtrl(self, datas):
self.datas = {'matrice':datas}
if self.datas['matrice'] == {}:
self.root = self.AddRoot("Root Demo Item")
item1 = self.AppendItem (self.root, "Item1",0)
item2 = self.AppendItem (self.root, "Item2",0)
self.Expand(self.root)
else:
pass


def TestProgram():
app = wx.App(0)
frame = MyFrame(None)
frame.Show()
app.MainLoop()

if __name__ == '__main__':
TestProgram()
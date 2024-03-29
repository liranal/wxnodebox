#!/usr/bin/python

import wx
import os
import time

ID_BUTTON=100
ID_EXIT=200
ID_SPLITTER=300

import TreeSystem
import FileSystem

class MyListCtrl(wx.ListCtrl):
    def __init__(self, parent, id, monFileSystem):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)
	
	self._cTreeRoot = monFileSystem.getBuilder().getRoots()[0]
	listElements = self._cTreeRoot.getChildrenList()
	print listElements

        #files = os.listdir('.')
        #images = ['images/empty.png', 'images/folder.png', 'images/source_py.png', 
	#	'images/image.png', 'images/pdf.png', 'images/up16.png']
        images = ['images/folder.png', 'images/folder.png', 'images/folder.png', 
		'images/folder.png', 'images/folder.png', 'images/folder.png']

        self.InsertColumn(0, 'Name')
        self.InsertColumn(1, 'Ext')
        self.InsertColumn(2, 'Size', wx.LIST_FORMAT_RIGHT)
        self.InsertColumn(3, 'Modified')

        self.SetColumnWidth(0, 220)
        self.SetColumnWidth(1, 70)
        self.SetColumnWidth(2, 100)
        self.SetColumnWidth(3, 420)

        self.il = wx.ImageList(16, 16)
        for i in images:
            self.il.Add(wx.Bitmap(i))
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

        j = 1
        self.InsertStringItem(0, '..')
        self.SetItemImage(0, 5)
	
	for element in listElements:
	    (name, ext) = ( element.getName(), "XXX")
	    size = 0
	    sec = 0
            self.InsertStringItem(j, name)
            self.SetStringItem(j, 1, ext)
            self.SetStringItem(j, 2, str(size) + ' B')
            self.SetStringItem(j, 3, time.strftime('%Y-%m-%d %H:%M', 
		time.localtime(sec)))
            if (j % 2) == 0:
                self.SetItemBackgroundColour(j, '#e6f1f5')
            j = j + 1
	    pass

        #for i in files:
        #    (name, ext) = os.path.splitext(i)
        #    ex = ext[1:]
        #    size = os.path.getsize(i)
        #    sec = os.path.getmtime(i)
        #    self.InsertStringItem(j, name)
        #    self.SetStringItem(j, 1, ex)
        #    self.SetStringItem(j, 2, str(size) + ' B')
        #    self.SetStringItem(j, 3, time.strftime('%Y-%m-%d %H:%M', 
	#	time.localtime(sec)))

        #    if os.path.isdir(i):
        #        self.SetItemImage(j, 1)
        #    elif ex == 'py':
        #        self.SetItemImage(j, 2)
        #    elif ex == 'jpg':
        #        self.SetItemImage(j, 3)
        #    elif ex == 'pdf':
        #        self.SetItemImage(j, 4)
        #    else:
        #        self.SetItemImage(j, 0)

class FileHunter(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title)

	monSysteme = FileSystem.FileManager()
	monBuilder = monSysteme.getBuilder()
	monBuilder.findRoots()
	
	
        self.splitter = wx.SplitterWindow(self, ID_SPLITTER, style=wx.SP_BORDER)
        self.splitter.SetMinimumPaneSize(50)

        p1 = MyListCtrl(self.splitter, -1, monSysteme)
        p2 = MyListCtrl(self.splitter, -1, monSysteme)
        self.splitter.SplitVertically(p1, p2)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SPLITTER_DCLICK, self.OnDoubleClick, id=ID_SPLITTER)

        self.sb = self.CreateStatusBar()
	
        filemenu= wx.Menu()
        filemenu.Append(ID_EXIT,"E&xit"," Terminate the program")
        editmenu = wx.Menu()
        netmenu = wx.Menu()
        showmenu = wx.Menu()
        configmenu = wx.Menu()
        helpmenu = wx.Menu()

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File")
        menuBar.Append(editmenu, "&Edit")
        menuBar.Append(netmenu, "&Net")
        menuBar.Append(showmenu, "&Show")
        menuBar.Append(configmenu, "&Config")
        menuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnExit, id=ID_EXIT)

        tb = self.CreateToolBar( wx.TB_HORIZONTAL | wx.NO_BORDER | 
		wx.TB_FLAT | wx.TB_TEXT)
        #tb.AddSimpleTool(10, wx.Bitmap('images/previous.png'), 'Previous')
        #tb.AddSimpleTool(20, wx.Bitmap('images/up.png'), 'Up one directory')
        #tb.AddSimpleTool(30, wx.Bitmap('images/home.png'), 'Home')
        #tb.AddSimpleTool(40, wx.Bitmap('images/refresh.png'), 'Refresh')
        #tb.AddSeparator()
        #tb.AddSimpleTool(50, wx.Bitmap('images/write.png'), 'Editor')
        #tb.AddSimpleTool(60, wx.Bitmap('images/terminal.png'), 'Terminal')
        #tb.AddSeparator()
        #tb.AddSimpleTool(70, wx.Bitmap('images/help.png'), 'Help')
        tb.AddSimpleTool(10, wx.Bitmap('images/Class.png'), 'Previous')
        tb.AddSimpleTool(20, wx.Bitmap('images/Class.png'), 'Up one directory')
        tb.AddSimpleTool(30, wx.Bitmap('images/Class.png'), 'Home')
        tb.AddSimpleTool(40, wx.Bitmap('images/Class.png'), 'Refresh')
        tb.AddSeparator()
        tb.AddSimpleTool(50, wx.Bitmap('images/Class.png'), 'Editor')
        tb.AddSimpleTool(60, wx.Bitmap('images/Class.png'), 'Terminal')
        tb.AddSeparator()
        tb.AddSimpleTool(70, wx.Bitmap('images/Class.png'), 'Help')
        tb.Realize()

        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        button1 = wx.Button(self, ID_BUTTON + 1, "F3 View")
        button2 = wx.Button(self, ID_BUTTON + 2, "F4 Edit")
        button3 = wx.Button(self, ID_BUTTON + 3, "F5 Copy")
        button4 = wx.Button(self, ID_BUTTON + 4, "F6 Move")
        button5 = wx.Button(self, ID_BUTTON + 5, "F7 Mkdir")
        button6 = wx.Button(self, ID_BUTTON + 6, "F8 Delete")
        button7 = wx.Button(self, ID_BUTTON + 7, "F9 Rename")
        button8 = wx.Button(self, ID_EXIT, "F10 Quit")

        self.sizer2.Add(button1, 1, wx.EXPAND)
        self.sizer2.Add(button2, 1, wx.EXPAND)
        self.sizer2.Add(button3, 1, wx.EXPAND)
        self.sizer2.Add(button4, 1, wx.EXPAND)
        self.sizer2.Add(button5, 1, wx.EXPAND)
        self.sizer2.Add(button6, 1, wx.EXPAND)
        self.sizer2.Add(button7, 1, wx.EXPAND)
        self.sizer2.Add(button8, 1, wx.EXPAND)

        self.Bind(wx.EVT_BUTTON, self.OnExit, id=ID_EXIT)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.splitter,1,wx.EXPAND)
        self.sizer.Add(self.sizer2,0,wx.EXPAND)
        self.SetSizer(self.sizer)

        size = wx.DisplaySize()
	size = ( size[0]-100, size[1]-100)
        self.SetSize(size)

        #self.sb = self.CreateStatusBar()
        self.sb.SetStatusText(os.getcwd())
        self.Center()
        self.Show(True)

    def OnExit(self,e):
        self.Close(True)

    def OnSize(self, event):
        size = self.GetSize()
        self.splitter.SetSashPosition(size.x / 2)
        self.sb.SetStatusText(os.getcwd())
        event.Skip()


    def OnDoubleClick(self, event):
        size =  self.GetSize()
        self.splitter.SetSashPosition(size.x / 2)

app = wx.App(0)
FileHunter(None, -1, 'File Hunter')
app.MainLoop()

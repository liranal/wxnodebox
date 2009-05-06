#! /usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; fill-column: 79; coding: iso-latin-1-unix -*-
#

import os, string

from wxPython.wx import wxNewId
from wxPython.wx import EVT_TREE_SEL_CHANGED, EVT_TREE_KEY_DOWN
from wxPython.wx import wxGenericDirCtrl
from wxPython.wx import wxDIRCTRL_EDIT_LABELS, wxDIRCTRL_DIR_ONLY, wxDIRCTRL_3D_INTERNAL, \
     wxDIRCTRL_SELECT_FIRST, wxNO_BORDER, wxSUNKEN_BORDER, wxTAB_TRAVERSAL

class smDirCtrl(wxGenericDirCtrl):
    def __init__(self, parent, hiddenDirs, dirFunc, path):
        # initialized the base class
        style = wxDIRCTRL_EDIT_LABELS | wxDIRCTRL_DIR_ONLY | \
                wxDIRCTRL_3D_INTERNAL | wxDIRCTRL_SELECT_FIRST | \
                wxNO_BORDER | wxTAB_TRAVERSAL #| wxSUNKEN_BORDER
        wxGenericDirCtrl.__init__(self, parent, wxNewId(), style=style)

        self.ShowHidden(hiddenDirs)

        # this will create a cyclic reference as `dirFunc' is likely to be a bound method with
        # reference to parent, and parent has a reference to this class. It's not vital since
        # there is only one instance of this class.
        self.dirFunc = dirFunc

        tree = self.GetTreeCtrl()
        EVT_TREE_SEL_CHANGED(self, tree.GetId(), self.OnDirSelected)

        self.SetPath(os.path.expanduser(path))

    def OnDirSelected(self, event):
        path = self.GetPath()
        if not os.path.exists(path):
            # keep going up the directory tree until `path' is valid
            while not os.path.exists(path): path = os.path.dirname(path)
            self.FixedSetPath(path)
            #event.Veto() # doesn't work with wxGenericDirCtrl

        self.dirFunc(path)

    def FixedSetPath(self, fullPath):
        """A fix for wxGenericDirCtrl
        wxGenericDirCtrl refuses to go into directories created "behind its back": if a new
        directory is created in a directory whose node is expanded it is not recognized by
        wxGenericDirCtrl (if explicitly asked to descend to it). wxGenericDirCtrl thinks that
        expanded directories never change so it needs to be collapsed and than expanded again
        to be reread from disk.
        """

        # if hidden files are disabled and path has hidden components
        if not self.GetShowHidden() and string.find(fullPath, "/.") >= 0: self.ShowHidden(true)

        self.SetPath(fullPath)
        if fullPath != self.GetPath() and os.path.exists(fullPath):
            path = fullPath
            path = apply(os.path.join, os.path.split(path)[:-1]) # parent dir
            self.SetPath(path)
            tree = self.GetTreeCtrl()
            item = tree.GetSelection()
            tree.Collapse(item)
            #tree.Expand(item)
            self.SetPath(fullPath)

"""
        # Keys are processed by the base class, and other means
        #EVT_TREE_KEY_DOWN(self, tree.GetId(), self.OnKeyDown)
    def OnKeyDown(self, event):
        if not self.keyFunc(event.GetKeyEvent()): event.Skip()
"""

from wxPython.wx import *
from VfsListing import *
from ImageList import *
import os
from PathName import *
from FilterDlg import *
from Globals import *
from BrowseHistoryList import *
from VfsSelection import *
from PathInfoCtrl import *

LST_CTRL_ID  =   11


class FileListCtrl (wxListCtrl):

    def __init__ (self, pParent):
        wxListCtrl.__init__ (self, pParent, LST_CTRL_ID, wxPoint(0, 20), wxSize(800, 600), wxLC_REPORT|wxLC_VIRTUAL|wxLC_EDIT_LABELS|wxSUNKEN_BORDER)
        #wxListCtrl.__init__ (self, pParent, -1, wxPoint(0, 20), wxSize(800, 600), wxLC_REPORT|wxLC_VIRTUAL|wxLC_HRULES|wxLC_VRULES)
        self.InsertColumn(0, _("Name"),  wxLIST_FORMAT_LEFT, 100)
        self.InsertColumn(1, _("Ext"),   wxLIST_FORMAT_LEFT,  40)
        self.InsertColumn(2, _("Size"),  wxLIST_FORMAT_RIGHT, 60)
        self.InsertColumn(3, _("Date"),  wxLIST_FORMAT_LEFT, 100)
        self.InsertColumn(4, _("Attr"),  wxLIST_FORMAT_LEFT, 100)


        self.m_bQuickSearchMode = false
        self.m_strQuickPtrn = ''
        self.m_pVfs = NULL
        self.m_pPathInfo = NULL
        self.m_pStatInfo = NULL
        self.m_lstItems = VfsListing ()
        self.m_lstHistory = BrowseHistoryList ()
        self.showdirsize = False
        self.showdirpos = 0

        entries = wxAcceleratorTable([
            (wxACCEL_CTRL,   WXK_PRIOR, CMD_UP_DIR),       #Ctrl+PageUp -> go to parent dir
            (wxACCEL_CTRL,   WXK_HOME,  CMD_ROOT_DIR),     #Ctrl+Home   -> go to root dir
            (wxACCEL_NORMAL, ord('+'),  CMD_SELECT),       #'+'         -> select
            (wxACCEL_NORMAL, ord('-'),  CMD_DESELECT)    #'-'         -> deselect
            #for testing purposes
            #,(wxACCEL_NORMAL, ord('*'),  CMD_DIR_SIZE),    #'-'         -> deselect
            #(wxACCEL_NORMAL, ord('/'),  CMD_FILTER)
            ,
            ])
        self.SetAcceleratorTable(entries)

        EVT_LIST_ITEM_ACTIVATED(self, LST_CTRL_ID, self.OnLeftDoubleClick)
        EVT_MENU(self, CMD_UP_DIR,     self.OnUpDir)
        EVT_MENU(self, CMD_ROOT_DIR,   self.OnRootDir)
        EVT_MENU(self, CMD_SELECT,     self.OnSelect)
        EVT_MENU(self, CMD_DESELECT,   self.OnDeselect)
        EVT_MENU(self, CMD_FILTER,     self.OnFilter)
        EVT_MENU(self, CMD_DIR_SIZE,   self.OnCalcDirSize)
        EVT_SET_FOCUS(self,self.OnSetFocus)
        EVT_LIST_BEGIN_LABEL_EDIT(self,LST_CTRL_ID, self.OnBeginLabelEdit)
        EVT_LIST_END_LABEL_EDIT(self,LST_CTRL_ID, self.OnEndLabelEdit)
        EVT_LIST_COL_CLICK(self,LST_CTRL_ID, self.OnHeaderClick)
        EVT_CHAR(self,self.OnChar)
        EVT_KEY_DOWN(self,self.OnKeyDown)
        EVT_LIST_ITEM_SELECTED(self,LST_CTRL_ID, self.OnSelectionChange)
        EVT_LIST_ITEM_DESELECTED(self,LST_CTRL_ID, self.OnSelectionChange)
        EVT_LIST_ITEM_FOCUSED(self,LST_CTRL_ID, self.OnSelectionChange)

    def SetDirectory (self, strDir, bAddToHistory = true):
        #wxLogDebug('StrDir = %s' + strDir)

        self.m_pVfs.SetDir(strDir)

        self.RefreshPathInfo()
        self.RefreshList()


        if bAddToHistory:
            #remember history
            self.m_lstHistory.Push(strDir);

        #ensure item focus exists
        if (self.m_lstItems.GetCount()>0):
            self.SetItemFocus(0);

        return true;

    def SetItemFocus(self, nIdx):
        self.SetItemState(nIdx, wxLIST_STATE_FOCUSED, wxLIST_STATE_FOCUSED)
        self.EnsureVisible(nIdx)


    #bool FileListCtrl::GetSelection(VfsSelection &sel)
    def GetSelection(self, sel):
        #remove old content
        sel.Clear()

        #fill selection object with selected items
        item = self.GetNextItem(-1, wxLIST_NEXT_ALL, wxLIST_STATE_SELECTED)
        while(item != -1):
            #store selected item
            sel.m_lstRootItems.append(self.m_lstItems.GetAt(item))

            #get next item
            item = self.GetNextItem(item, wxLIST_NEXT_ALL, wxLIST_STATE_SELECTED)

        #if nothing selected, store focused item
        if(len (sel.m_lstRootItems) == 0):
            item = self.GetNextItem(-1, wxLIST_NEXT_ALL, wxLIST_STATE_FOCUSED)
            if(item != -1):
                sel.m_lstRootItems.append(self.m_lstItems.GetAt(item))
        return True


    def RefreshList(self):
        self.ClearSelection()
        self.ClearFocus()

        #TOFIX
        bAbort = false

        # normale Liste
        self.m_pVfs.ListDir(self.m_lstItems, bAbort)
        self.m_lstItems.Sort()
        self.m_lstItems.FilterList()

        #calculate icons (also for invisible/filtered items)
        #TOMAKEBETTER:
        #noch zu frueh
        #pFrm = wxGetApp().GetFrame()
        imglist = CImageList()
        for i in range (self.m_lstItems.GetCountRaw()):
        #    #pFrm.m_objIconList.CalcIconIndex(self.m_lstItems.GetAtRaw(i))
             imglist.CalcIconIndex(self.m_lstItems.GetAtRaw(i))
        #    #print

        #refresh list control
        self.SetItemCount(self.m_lstItems.GetCount());
            #self.SetItemCount(self.m_lstItems.GetCount())
            #self.SetItemCount(1)
            #self.SetItemState(0, 1, wxLIST_STATE_SELECTED);
            #self.SetItemState(1, 1, wxLIST_STATE_SELECTED);

        self.RefreshStatusInfo()
        #print 'after:', self.m_lstItems.m_List[0].m_strName
        #end to do

    def ClearSelection(self):
        item = self.GetNextItem(-1, wxLIST_NEXT_ALL, wxLIST_STATE_SELECTED);
        while(item != -1):
            #remove item selection
            self.SetItemState(item, 0, wxLIST_STATE_SELECTED);
            item = self.GetNextItem(item, wxLIST_NEXT_ALL, wxLIST_STATE_SELECTED);

    def ClearFocus(self):
        #find and remove focus from item
        item = self.GetNextItem(-1, wxLIST_NEXT_ALL, wxLIST_STATE_FOCUSED)
        if (item != -1):
            self.SetItemState(item, 0, wxLIST_STATE_FOCUSED)

    def RefreshStatusInfo(self):
        #print 'refresh status info'
        #TOFIX support multiple colored text (black/red)
        #update stat info (selection, filter, quick search)
        if(self.m_bQuickSearchMode):
            #//set bold font
            font = self.m_pStatInfo.GetFont();
            font.SetWeight(wxBOLD);
            self.m_pStatInfo.SetFont(font);
            self.m_pStatInfo.SetForegroundColour(wxRED)
            strInfo = _("Search: %s") % self.m_strQuickPtrn
        else:
            #//TOFIX use wxGetDiskSpace ...

            #//set normal font
            font = self.m_pStatInfo.GetFont()
            font.SetWeight(wxNORMAL)
            self.m_pStatInfo.SetFont(font)
            self.m_pStatInfo.SetForegroundColour(wxBLACK)
            Statuslist = VfsSelection()
            self.GetSelection(Statuslist)

            nTotalCount     = self.m_lstItems.GetCount()
            nTotalSelCount  = Statuslist.GetTotalCount()

            #//format total selected size
            nTotalSelSize = Statuslist.GetTotalSize()
            strSize = FormatSizeUnits(nTotalSelSize);

            strInfo = _("%d of %d file(s) selected (%s)") % (nTotalSelCount, nTotalCount, strSize)

            #//TOFIX draw this part only in red color!??
            if self.m_lstItems.GetFilter() != '':
                strInfo += _("  Filter: %s") % self.m_lstItems.GetFilter().GetDescription()


        self.m_pStatInfo.SetLabel(strInfo)
        #//FIX: needed for GTK (TOFIX report as BUG)
        self.m_pStatInfo.Refresh()

    def OnGetItemText(self, item, col):
        isdir = self.m_lstItems.GetAt(item).IsDir()

        #isdir = os.path.isdir(os.path.join(self.m_pVfs.m_strCurDir, self.m_lstItems.m_List[item].m_strName))
        #ev. auch auf extpos abfragen (-1)
        #0 ... name

        if col == 0:
            #if (self.m_lstItems.m_List[item].m_strName == '..'):
            #if (self.m_lstItems.GetAt(item).GetName() == '..'):
            #koenne auch gettitle sein (getname ist das ganze(
            if (self.m_lstItems.GetAt(item).GetName() == '..'):
                return '..'
            else:
                #if not isdir:
                    #return os.path.splitext(self.m_lstItems.m_List[item].m_strName)[0]
                return self.m_lstItems.GetAt(item).GetTitle()
                #else:
                #    return self.m_lstItems.GetAt(item).GetName()
        #1 ... ext
        elif col==1:
            #1: wegen Punkt am Anfang
            if not isdir:
                #return os.path.splitext(self.m_lstItems.m_List[item].m_strName)[1][1:]
                return self.m_lstItems.GetAt(item).GetExt()
            else:
                return ""
        elif col==2:
            #print self.showdirsize, self.showdirpos, item
            if self.showdirsize and self.showdirpos == item:
                return self.strSize
            #self.SetStringItem(nPos, SIZE_COL, self.strSize)
            else:
                #if os.path.isdir(os.path.join(self.m_pVfs.m_strCurDir, self.m_lstItems.m_List[item].m_strName)):
                #TODO: beneath it is not always right
                if isdir:
                    return _("<DIR>")
                else:
                    return self.m_lstItems.GetAt(item).GetSize()
                    #return self.m_lstItems.m_List[item].m_nSize
        elif col==3:
            return self.m_lstItems.GetAt(item).GetDate()
            #return self.m_lstItems.m_List[item].GetDate () #m_List[item].m_nLastModDate
        elif col==4:
            #return self.m_lstItems.m_List[item].GetAttr () #m_List[item].m_nLastModDate
            return self.m_lstItems.GetAt(item).GetAttr()


    def OnGetItemImage(self, item):
        #print self.m_lstItems.GetAt(item).m_nIconIdx
        #return 2
        #return self.m_lstItems.GetAt(item).m_nIconIdx
        if self.m_lstItems.GetAt(item).IsDir():
        #if os.path.isdir(os.path.join(self.m_pVfs.m_strCurDir, self.m_lstItems.m_List[item].m_strName)):
            if self.m_lstItems.m_List[item].m_strName == '..':
                return 0
            else:
                return 1
        else:
            return 2

    #TOMAKEBETTER: necessary?
    #def OnGetItemAttr(self, item):
    #    return None

    #def OnLeftDoubleClick(wxListEvent& event)
    def OnLeftDoubleClick(self, event, index = -1):

        #print 'OnLeftDoubleClick'
        #ensure quick search exited
        #//ensure quick search exited
        self.QuickSearchExit()
        #get clicked item
        if index != -1:
           i = index
        else:
            i = event.GetIndex()
        #print i
        entry = self.m_lstItems.GetAt(i).GetName()
        #print 'ent:', entry
        #handle the action
        if(self.m_lstItems.GetAt(i).IsDots()):
        #if(1):
            #remember dir before changes

            #gibt es nicht in wxpython
            #path = wxFileName (self.m_pVfs.GetDir())
            olddir = self.m_pVfs.GetDir()
            #print olddir
            olddir = PathName.EnsureNotTerminated(PathName(), olddir);
            #print 'hier', self.m_pVfs.GetDir()
            #print olddir
            olddir = os.path.basename(olddir)
            #print olddir
            evDummy = wxMenuEvent ()
            self.OnUpDir(evDummy)

            #select the directory name we just got out from
            #nPos = self.m_lstItems.FindItem(path.GetFullName())
            #nPos = self.m_lstItems.FindItem(self.m_pVfs.GetDir())
            nPos = self.m_lstItems.FindItem(olddir)
            if nPos > 0:
                self.SetItemFocus(nPos)

        elif (self.m_lstItems.GetAt(i).IsDir()):
            #prepare full path of the item clicked
            strPath = self.m_pVfs.GetDir()
            #print 'dir', strPath, entry
            strPath = os.path.join (strPath, entry)
            #wxChar cSeparator = wxFileName::GetPathSeparator()
            #if(strPath.Right(1) != cSeparator)
            #    strPath += cSeparator;
            #strPath += entry;
            self.SetDirectory(strPath)
        else:
            if (wxGetApp().GetFrame().g_VfsManager.CheckForSubVfs(self, self.m_pVfs, self.m_lstItems.GetAt(i))):
                self.RefreshList()
                self.RefreshPathInfo()
            else:
                self.m_pVfs.Execute(entry)

        event.Skip()

    #bool FileListCtrl::QuickSearchExit()
    def QuickSearchExit(self):
        #exit quick search
        if(self.m_bQuickSearchMode):
            #print 'set false'
            self.m_bQuickSearchMode = false
            self.RefreshStatusInfo()
            return true
        return false

    #void FileListCtrl::OnUpDir(wxMenuEvent &event)
    def OnUpDir (self, event):
        #print 'onupdir', self.m_pVfs.GetDir(), self.m_pVfs
        #print 'self:', self
        if(self.m_pVfs.IsRootDir()):
            #we are inside root of current Vfs, go up in the Vfs stack?

            if (wxGetApp().GetFrame().g_VfsManager.CheckForUpVfs(self, self.m_pVfs)):
                RefreshList()
                RefreshPathInfo()
                #print 'in root'
                m_lstHistory.Push(self.m_pVfs.GetDir())
        else:
            #we are not in root of current Vfs, go up directory
            #self.SetDirectory(PathName::GetParentDirPath(m_pVfs->GetDir()))
            self.SetDirectory(PathName.GetParentDirPath(PathName(), self.m_pVfs.GetDir()))

    def OnRootDir (self, event):
        strPath = os.path.splitdrive(self.m_pVfs.GetDir())[0]
        #print strPath
        #wxString strPath = path.GetVolume();
        if(strPath == ''):
            strPath = '/';
        else:
            strPath += '\\';
        #print strPath
        self.SetDirectory(strPath);

    def OnSelect (self, event):
        #print 'on select'
        dlg = CFilterDlg(self)
        dlg.m_strTitle = _("Select files")
        #ifdef __WXMSW__
        dlg.m_strValue = '*.*'
        #else
        #    dlg.m_strValue = '*';
        #endif


        if(wxOK == dlg.ShowModal()):
            #TOFIX use full filter here
            filter = FilterDesc ()
            #print 'd:', dlg.m_strValue
            filter.SetNameGroup (dlg.m_strValue, '')

            #if item matches pattern then select it
            for i in range (self.m_lstItems.GetCount()):
                if(filter.Match(self.m_lstItems.GetAt(i))):
                    self.SetItemState(i, wxLIST_STATE_SELECTED, wxLIST_STATE_SELECTED)

    def SelectAll (self, event):
        #if item matches pattern then deselect it
        for i in range(self.m_lstItems.GetCount()):
            self.SetItemState(i, wxLIST_STATE_SELECTED, wxLIST_STATE_SELECTED)

    def InvertSelection (self, event):
        for i in range(self.m_lstItems.GetCount()):
            nState = self.GetItemState(i, wxLIST_STATE_SELECTED)
            if (nState & wxLIST_STATE_SELECTED):
                self.SetItemState(i, 0, wxLIST_STATE_SELECTED)
            else:
                self.SetItemState(i, wxLIST_STATE_SELECTED, wxLIST_STATE_SELECTED)

    def OnDeselect (self, event):

        dlg = CFilterDlg(self)
        dlg.m_strTitle = _("Deselect files")
        #ifdef __WXMSW__
        dlg.m_strValue = '*.*'
        #else
        #    dlg.m_strValue = '*';
        #endif


        if(wxOK == dlg.ShowModal()):
            #TOFIX use full filter here
            filter = FilterDesc ()
            #print 'd:', dlg.m_strValue
            filter.SetNameGroup (dlg.m_strValue, '')

            #if item matches pattern then select it
            for i in range (self.m_lstItems.GetCount()):
                if(filter.Match(self.m_lstItems.GetAt(i))):
                    self.SetItemState(i, 0, wxLIST_STATE_SELECTED);


    def OnFilter (self, event):
        dlg = CFilterDlg(self)
        dlg.m_strTitle = _("Filter Files")

        if(wxOK == dlg.ShowModal()):
            #TOFIX use full filter here
            filter = FilterDesc ()

            filter.SetNameGroup (dlg.m_strValue, '')
            #do not remove dirs
            filter.AddGroupFlags(FILTER_SkipDirMatch)
            self.m_lstItems.SetFilter(filter)
            self.RefilterList()

    def RefilterList(self):
        self.m_lstItems.FilterList()
        #print 'c:', self.m_lstItems.GetCount()
        self.SetItemCount(self.m_lstItems.GetCount())
        self.RefreshStatusInfo()
        self.Refresh()

    #int FileListCtrl::GetItemFocus()
    def GetItemFocus(self):
        return self.GetNextItem(-1, wxLIST_NEXT_ALL, wxLIST_STATE_FOCUSED)


    #void FileListCtrl::SelectItem(int nIdx)
    def SelectItem(self, nIdx):
        self.SetItemState(nIdx, wxLIST_STATE_SELECTED, wxLIST_STATE_SELECTED)

    #void FileListCtrl::DeselectItem(int nIdx)
    def DeselectItem(self, nIdx):
        self.SetItemState(nIdx, 0, wxLIST_STATE_SELECTED)

    def SelectFilesOnly(self, bUnselectOther = True):
        if(bUnselectOther):
            self.ClearSelection()

        nFileCnt = 0
        for i in range (self.m_lstItems.GetCount()):
            #if(self.m_lstItems.GetAt(i).IsDir() == False):
            #oder so:
            if not self.m_lstItems.GetAt(i).IsDir():
                nFileCnt += 1;
                self.SelectItem(i)
        return nFileCnt

    def OnCalcDirSize(self):
        #print 'OnCalcDirSize'
        #TOFIX escape press can abort the operation
        #SHORT wState = GetAsyncKeyState(VK_ESCAPE);

        wait = wxBusyCursor ()

        nPos = self.GetItemFocus()
        if(nPos < 0):
            return

        item = self.m_lstItems.GetAt(nPos)
        if (not self.m_lstItems.GetAt(nPos).IsDir() or
            self.m_lstItems.GetAt(nPos).IsDots()):
            #not a valid directory
            return

        itemSel = VfsSelectionItem (item)
        sel = VfsSelection ()
        sel.m_lstRootItems.append(itemSel)

        bAbort = False
        self.m_pVfs.ExpandSelection(sel, bAbort)
        nSize = sel.GetTotalSize()

        #print nSize
        #store result back into the item
        #nSize = 100000
        self.m_lstItems.GetAt(nPos).m_nSize = nSize

        SIZE_COL = 2

        self.strSize = FormatSize(nSize, ',')
        self.showdirpos = nPos
        self.showdirsize = True
        self.RefreshItem(nPos)
        #self.showdirsize = False

        #TOFIX trigger instant redraw
        #self.SetStringItem(nPos, SIZE_COL, self.strSize)
        ##SetItem(nPos, SIZE_COL, strSize);
        #self.DeselectItem(nPos)
        #self.SelectItem(nPos)


        #war auch beim urspruenglichen auskommentiert
        #//self.Update()


    def OnSetFocus(self, event):
        #print 'OnSetFocus'
        pPanel = self.GetParent()
        if(pPanel):
           pPanel.Activate(True)
        #continue processing event in base class
        event.Skip()

    def OnBeginLabelEdit(self, event):
        #print 'OnBeginLabelEdit'
        nFocus = self.GetItemFocus();
        if(nFocus >= 0):
            #set full file name to be edited in the edit box
            self.SetItemText(nFocus, self.m_lstItems.GetAt(nFocus).GetName());
            #ifdef __WXMSW__
            ctrl = self.GetEditControl()
            if(ctrl):
                ctrl.SetValue(self.m_lstItems.GetAt(nFocus).GetName())
            #endif
        event.Skip();

    def OnEndLabelEdit(self, event):
        #print 'OnEndLabelEdit'
        nFocus = self.GetItemFocus()
        if(nFocus >= 0):
            #//must append extension
            strExt = self.m_lstItems.GetAt(nFocus).GetExt()
            strOld = self.GetItemText(nFocus);
            if(strExt != ''):
                strExt = '.' + strExt
                strOld += strExt

            strNew = event.GetText()
            if(strNew == ''):
                wxMessageBox(_("Name must not be empty!"))
                event.Veto()
                return

            if(strNew != strOld):
                #//TOFIX path creation class
                strDir = self.m_pVfs.GetDir()
                if(strDir[-1] != '/' and strDir[-1] != '\\'):
                    #//ensure terminated with /
                    strDir += '/';

                if(not self.m_pVfs.Rename(strDir + strOld, strDir + strNew)):
                    wxMessageBox(_("Failed to rename!"))
                    #ifdef __WXMSW__
                    #event.Veto();
                    #endif
                    return

            #//refresh internal list
            self.m_lstItems.GetAt(nFocus).SetName(strNew)

            #//TOFIX only 1 item needs to be redrawn
            #//Refresh();
            #//TOFIX trigger instant redraw RedrawItem(from, to) ?
            self.DeselectItem(nFocus)
            self.SelectItem(nFocus)

            event.Skip()

    def OnHeaderClick(self, event):
        #//TOFIX dynamic mapping (table)
        #//map column index to the column data type
        nColumnType = ST_NONE
        nCol = event.GetColumn()
        if (nCol == 0):
            nColumnType = ST_NAME
        elif (nCol == 1):
            nColumnType = ST_EXT
        elif (nCol == 2):
            nColumnType = ST_SIZE
        elif (nCol == 3):
            nColumnType = ST_DATE
        elif (nCol == 4):
            nColumnType = ST_ATTR

        #//TOFIX some types can have different default value for asc param than true (date?)
        bAsc = True

        #//if the same header was clicked twice, revert previous sort order
        if(self.m_lstItems.GetSortCol() == nColumnType):
            bAsc = not self.m_lstItems.GetSortAsc()

        self.m_lstItems.SetSort(nColumnType, bAsc)
        self.m_lstItems.Sort()
        self.Refresh()
        event.Skip()

    def OnChar(self, event):
        #print 'OnChar'

        #//TOFIX add quick search processing here
        nKey = event.GetKeyCode()
        if (nKey > 31 and nKey < 256 and not event.HasModifiers()):
            if self.m_bQuickSearchMode:
                #//continue with quick search
                self.m_strQuickPtrn += chr(nKey)
                #print self.m_strQuickPtrn

                #//quick search restarts from 0 since user could be above matching items
                nPos   = self.m_lstItems.FindPartial(self.m_strQuickPtrn, 0, true)
                if(nPos >= 0):
                    self.SetItemFocus(nPos)
                else:
                    wxBell()
                    self.m_strQuickPtrn = self.m_strQuickPtrn[:len (self.m_strQuickPtrn)-1:]

                self.RefreshStatusInfo()
            else:
                #//needed by command line to catch key presses
                self.GetParent().ProcessEvent(event)
            return

        event.Skip()

    def OnSelectionChange(self, event):
        #print 'OnSelectionChange'
        #if user triggered this event using mouse click - close quick search mode
        #TOFIX detect if mouse click caused this?
        #war urspruenglich ausgesternt
        #//QuickSearchExit();

        self.RefreshStatusInfo();

    #VfsListing  &GetListing(){ return m_lstItems; }
    def GetListing(self):
        return self.m_lstItems

    def SetListing(self, lst):
        self.m_lstItems = lst
        self.RefreshPathInfo()
        self.RefreshList()

    #void FileListCtrl::OnKeyDown(wxKeyEvent& event)
    def OnKeyDown(self, event):
        #print 'onkeydown in Filelistctrl'
        #print self.m_bQuickSearchMode

        #ifdef __WXMSW__
        #//if inside label editing
        if(NULL != self.GetEditControl()):
            event.Skip()
            #print '1'
            return
        #endif

        #//RETURN processing - pass to command line if not empty (eating event here)
        nKey = event.GetKeyCode()
        if(nKey == WXK_RETURN):
            #print '2'
            self.QuickSearchExit()

            pFrm = wxGetApp().GetFrame()
            if(pFrm and pFrm.ExecuteCmdLine()):
                return

            #ifdef __WXMSW__
            #//TOFIX test and report as wx BUG!!!
            #//FIX: wx does not fire event when item is focused, but not selected!!!!
            nPos = self.GetItemFocus()
            if(nPos >= 0):
                #print nPos
                dummy = wxListEvent ()
                #dummy = wxListEvent (id = nPos)
                #dummy.m_itemIndex = nPos
                self.OnLeftDoubleClick(dummy, index = nPos)
                #//eat event once it is consumed
                return
            #endif

        #//if (!m_bQuickSearchMode && nKey > 31 && nKey < 256 && event.AltDown()) //Alt+Key starts quick search
        #//Alt+Q starts quick search
        if (not self.m_bQuickSearchMode and nKey == ord('Q') and event.AltDown()):
            #//start quick search mode
            self.m_bQuickSearchMode = True
            #print '3'

            self.m_strQuickPtrn = ''
            #//m_strQuickPtrn += nKey;
            #//int nPos = m_lstItems.FindPartial(m_strQuickPtrn, 0, true);
            #//if(nPos >= 0)
            #//  SetItemFocus(nPos);
            #//else{
            #//  wxBell();
            #//  m_bQuickSearchMode = false; //failed to find initial pattern
            #//}

            self.RefreshStatusInfo()
            return

        if(nKey == WXK_ESCAPE):
            #print '4'
            #//quit if inside quick search mode
            if(self.QuickSearchExit()):
                #//eat event
                return

            #//else, clear command line if not empty
            pFrm = wxGetApp().GetFrame()
            if(pFrm and pFrm.ClearCmdLine()):
                return

        if(not self.m_bQuickSearchMode and nKey == WXK_SPACE):
            #print '5'
            self.OnCalcDirSize()
            return
        #print nKey, WXK_DOWN
        if(self.m_bQuickSearchMode and nKey == WXK_DOWN):
            #print '6'
            #//restrict moving to matching items only
            nFocus = self.GetItemFocus()
            nPos = self.m_lstItems.FindPartial(self.m_strQuickPtrn, nFocus+1, True)
            if(nPos >= 0):
                self.SetItemFocus(nPos)
            else:
                wxBell()
            #//eat event
            return

        if(self.m_bQuickSearchMode and nKey == WXK_UP):
            #//restrict moving to matching items only
            #print '7'
            nFocus = self.GetItemFocus();
            nPos = self.m_lstItems.FindPartial(self.m_strQuickPtrn, nFocus-1, False)
            if(nPos >= 0):
                self.SetItemFocus(nPos)
            else:
                wxBell()
            #//eat event
            return

        if(self.m_bQuickSearchMode and nKey == WXK_BACK):
            #//remove last pattern character
            #print '8'
            nLen = len (self.m_strQuickPtrn)
            if(nLen > 0):
                self.m_strQuickPtrn = self.m_strQuickPtrn[:nLen-1]
                nPos = self.m_lstItems.FindPartial(self.m_strQuickPtrn, 0, True)
                if(nPos >= 0):
                    self.SetItemFocus(nPos)
                else:
                    wxBell()
            else:
                wxBell()
            #//eat event
            return

        event.Skip()

    def RefreshPathInfo(self):
        #calculate and show path title

        #GetMainFrame verwenden
        #geht zu diesem Zeitpunkt noch nicht, das mainframe in wxpyatol noch nicht gesetzt ist
        #wird im konstruktor aufgerufen
        strTitle = self.GetParent().GetParent().GetParent().g_VfsManager.GetPathTitle (self)
        #print strTitle

        self.m_pPathInfo.SetLabel(strTitle);
        #FIX: needed for GTK (TOFIX report as BUG)

        self.m_pPathInfo.Refresh()

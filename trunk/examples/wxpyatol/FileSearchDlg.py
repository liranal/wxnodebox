from wxPython.wx import *
from FilterDesc import *
from DatePickerDlg import *
from FileSearchThread import *
from VfsListing import *

BTN_OK        = 1
BTN_CANCEL    = 2
CHK_SUBDIR    = 3
CHK_CASE      = 4
CHK_DATE_AGE  = 5
CHK_DATE_FROM = 6
CHK_DATE_TO   = 7
CHK_SIZE      = 8
CHK_ATTR      = 9
BTN_GOTO      = 10
BTN_PICK_FROM = 11
BTN_PICK_TO   = 12

TAB_WIDTH     = 300
TAB_HEIGTH    = 150

class CFileSearchDlg (wxDialog):
    def __init__(self, pParent):
        wxDialog.__init__ (self, pParent, -1, _("File search"), wxDefaultPosition, wxDefaultSize, wxCAPTION)
        #wxDialog.__init__ (self, pParent, -1, 'File search', wxDefaultPosition, (500, 500), wxCAPTION)
        self.m_pThread = NULL
        self.m_bResultsVisible = false
        self.m_bRecursive = false
        self.m_strDirPattern = ''
        self.m_objSearchDesc = FilterDesc ()
        self.m_lstResult = VfsListing ()
        self.m_wndTabCtrl = wxNotebook(self, -1, wxDefaultPosition, wxDefaultSize)
        #self.m_wndTabCtrl = wxNotebook(self, -1, wxDefaultPosition, (450, 450))

        #self.m_wndNamePg = wxNotebookPage(self.m_wndTabCtrl, -1, wxDefaultPosition, (450, 450))#wxDefaultSize)
        self.m_wndNamePg = wxNotebookPage(self.m_wndTabCtrl, -1)
        self.m_wndContentPg = wxNotebookPage(self.m_wndTabCtrl, -1)
        self.m_wndDatePg= wxNotebookPage(self.m_wndTabCtrl, -1)
        self.m_wndSizePg= wxNotebookPage(self.m_wndTabCtrl, -1)
        self.m_wndAttrPg= wxNotebookPage(self.m_wndTabCtrl, -1)

        self.m_wndOkBtn = wxButton (self, BTN_OK, _("Search"),  wxPoint(0,0))
        self.m_wndCancelBtn  = wxButton (self, BTN_CANCEL, _("Cancel"),  wxPoint(0,0))
        self.m_wndGotoBtn  = wxButton (self, BTN_GOTO,   _("Go to"), wxPoint(0,0))
        self.m_wndResultList  = wxListCtrl (self, -1, wxDefaultPosition, wxDefaultSize, wxLC_REPORT|wxSUNKEN_BORDER )#wxLC_VIRTUAL|

        self.m_wndResultList.InsertColumn(0, _("Name"),  wxLIST_FORMAT_LEFT, 130);
        self.m_wndResultList.InsertColumn(1, _("Ext"),   wxLIST_FORMAT_LEFT,  50);
        self.m_wndResultList.InsertColumn(2, _("Path"),  wxLIST_FORMAT_LEFT, 50);
        self.m_wndResultList.InsertColumn(3, _("Size"),  wxLIST_FORMAT_RIGHT, 50);
        self.m_wndResultList.InsertColumn(4, _("Date"),  wxLIST_FORMAT_LEFT, 100);
        self.m_wndResultList.InsertColumn(5, _("Attr"),  wxLIST_FORMAT_LEFT, 100);

        self.m_wndTabCtrl.SetDimensions(0, 0, TAB_WIDTH, TAB_HEIGTH)
        #wxSize( nWidth, nHeight-21 )

        #add tab pages
        self.m_wndTabCtrl.AddPage(self.m_wndNamePg, _("File"))
        self.m_wndTabCtrl.AddPage(self.m_wndContentPg, _("Content"))
        self.m_wndTabCtrl.AddPage(self.m_wndDatePg, _("Date"))
        self.m_wndTabCtrl.AddPage(self.m_wndSizePg, _("Size"))
        self.m_wndTabCtrl.AddPage(self.m_wndAttrPg, _("Attributes"))
        self.m_wndTabCtrl.SetSelection(0)

        self.m_wndOkBtn      .SetDimensions(TAB_WIDTH + 10, 22, 80, 22)
        self.m_wndCancelBtn  .SetDimensions(TAB_WIDTH + 10, 47, 80, 22)
        self.m_wndResultList .SetDimensions(0, 0, 0, 0)
        self.m_wndResultList .Show(false)
        self.m_wndGotoBtn    .Show(false)

        #create tab controls
        self.m_wndFileNameEdit   = wxTextCtrl (self.m_wndNamePg, -1, '',  wxPoint(0,0))
        self.m_wndFileNameEdit.SetDimensions(50, 10, TAB_WIDTH-70, 22)
        self.m_wndFileNameLabel = wxStaticText (self.m_wndNamePg, -1, _("Name:"),  wxPoint(0,0))
        self.m_wndFileNameLabel.SetDimensions( 5, 13, 40, 22)
        self.m_wndFilePathEdit   = wxTextCtrl (self.m_wndNamePg, -1, '',  wxPoint(0,0))
        self.m_wndFilePathEdit.SetDimensions(50, 35, TAB_WIDTH-70, 22)
        self.m_wndFilePathLabel  = wxStaticText (self.m_wndNamePg, -1, _("Look in:"),  wxPoint(0,0))
        self.m_wndFilePathLabel.SetDimensions( 5, 38, 40, 22)
        self.m_wndSearchSubdirChk = wxCheckBox (self.m_wndNamePg, CHK_SUBDIR, _("Search subdirectories"))
        self.m_wndSearchSubdirChk.SetDimensions(50, 60, TAB_WIDTH-70, 22)

        self.m_wndFileTextEdit = wxTextCtrl (self.m_wndContentPg, -1, '',  wxPoint(0,0))
        self.m_wndFileTextEdit.SetDimensions(50, 10, TAB_WIDTH-70, 22)
        self.m_wndFileTextLabel = wxStaticText (self.m_wndContentPg, -1, '',  wxPoint(0,0))
        self.m_wndFileTextLabel.SetDimensions( 5, 13, 40, 22)
        self.m_wndCaseSensitiveChk = wxCheckBox (self.m_wndContentPg, CHK_CASE, _("Case sensitive"))
        self.m_wndCaseSensitiveChk.SetDimensions( 5, 38, 100, 22)

        self.m_wndDateAgeChk = wxCheckBox (self.m_wndDatePg, CHK_DATE_AGE, _("Age"))
        self.m_wndDateAgeChk.SetDimensions(5, 10, 45, 22)

        self.m_wndAgeRelationCbo = wxComboBox (self.m_wndDatePg, -1, choices=[], style=wxCB_READONLY)
        self.m_wndAgeRelationCbo.SetDimensions( 80, 10, 40, 22)
        self.m_wndAgeValueEdit = wxTextCtrl (self.m_wndDatePg, -1)
        self.m_wndAgeValueEdit.SetDimensions(125, 10, 50, 22)
        self.m_wndAgeUnitCbo = wxComboBox (self.m_wndDatePg, -1, choices=[], style=wxCB_READONLY)
        self.m_wndAgeUnitCbo.SetDimensions(180, 10, 100, 22)
        self.m_wndDateFromChk = wxCheckBox (self.m_wndDatePg, CHK_DATE_FROM, _("From date"))
        self.m_wndDateFromChk.SetDimensions(  5, 35, 70, 22)
        self.m_wndDateFromEdit = wxTextCtrl (self.m_wndDatePg, -1, '', wxDefaultPosition, wxDefaultSize, wxTE_READONLY)
        self.m_wndDateFromEdit.SetDimensions( 80, 35, 100, 22)
        self.m_wndDateFromPickBtn  = wxButton (self.m_wndDatePg, BTN_PICK_FROM, '...',  wxPoint(0,0))
        self.m_wndDateFromPickBtn.SetDimensions(180, 35, 20, 22)
        self.m_wndDateToChk  = wxCheckBox (self.m_wndDatePg, CHK_DATE_TO, _("To date"))
        self.m_wndDateToChk.SetDimensions(  5, 60, 70, 22)
        self.m_wndDateToEdit = wxTextCtrl (self.m_wndDatePg, -1, '', wxDefaultPosition, wxDefaultSize, wxTE_READONLY)
        self.m_wndDateToEdit.SetDimensions( 80, 60, 100, 22)
        self.m_wndDateToPickBtn = wxButton (self.m_wndDatePg, BTN_PICK_TO, '...',  wxPoint(0,0))
        self.m_wndDateToPickBtn.SetDimensions(180, 60, 20, 22)

        self.m_wndSizeChk = wxCheckBox(self.m_wndSizePg, CHK_SIZE, _("Size"))
        self.m_wndSizeChk.SetDimensions(5, 10,  45, 22)
        self.m_wndSizeRelationCbo = wxComboBox (self.m_wndSizePg, -1, choices=[], style=wxCB_READONLY)
        self.m_wndSizeRelationCbo.SetDimensions( 80, 10,  40, 22)
        self.m_wndSizeValueEdit = wxTextCtrl(self.m_wndSizePg, -1)
        self.m_wndSizeValueEdit.SetDimensions(125, 10,  50, 22)
        self.m_wndSizeUnitCbo = wxComboBox(self.m_wndSizePg, -1, choices=[], style=wxCB_READONLY)
        self.m_wndSizeUnitCbo.SetDimensions(180, 10, 100, 22)

        self.m_wndAttrChk = wxCheckBox(self.m_wndAttrPg, CHK_ATTR, _("Attributes"))
        self.m_wndAttrChk.SetDimensions(5, 10, 100, 22)
        #ifdef __WXMSW__
        self.m_wndAttrDOSArchiveChk = wxCheckBox(self.m_wndAttrPg, -1, _("Archive"))
        self.m_wndAttrDOSArchiveChk.SetDimensions(  25, 35,  60, 22)
        self.m_wndAttrDOSHiddenChk = wxCheckBox(self.m_wndAttrPg, -1, _("Hidden"))
        self.m_wndAttrDOSHiddenChk.SetDimensions( 100, 35,  60, 22)
        self.m_wndAttrDOSSystemChk = wxCheckBox(self.m_wndAttrPg, -1, _("System"))
        self.m_wndAttrDOSSystemChk.SetDimensions( 170, 35,  60, 22)
        self.m_wndAttrDOSDirectoryChk= wxCheckBox(self.m_wndAttrPg, -1, _("Directory"))
        self.m_wndAttrDOSDirectoryChk.SetDimensions(  25, 60,  60, 22)
        self.m_wndAttrDOSReadOnlyChk = wxCheckBox (self.m_wndAttrPg, -1, _("Read only"))
        self.m_wndAttrDOSReadOnlyChk.SetDimensions( 100, 60, 100, 22)
        #else
        #todolinux
        '''
        m_wndAttrUNXOwnLabel    = new wxStaticText;
        m_wndAttrUNXOwnLabel  ->Create(m_wndAttrPg, -1, _("Owner"))
        m_wndAttrUNXOwnLabel    ->SetSize( 25, 35, 60, 22);
        m_wndAttrUNXGrpLabel    = new wxStaticText;
        m_wndAttrUNXGrpLabel  ->Create(m_wndAttrPg, -1, _("Group"));
        m_wndAttrUNXGrpLabel    ->SetSize(110, 35, 60, 22);
        m_wndAttrUNXOthLabel    = new wxStaticText;
        m_wndAttrUNXOthLabel  ->Create(m_wndAttrPg, -1, _("Other"));
        m_wndAttrUNXOthLabel    ->SetSize(190, 35, 60, 22);
        m_wndAttrUNXOwnReadChk  = new wxCheckBox;
        m_wndAttrUNXOwnReadChk  ->Create(m_wndAttrPg, -1, _("Read"));
        m_wndAttrUNXOwnReadChk  ->SetSize( 25, 55, 60, 22);
        m_wndAttrUNXGrpReadChk  = new wxCheckBox;
        m_wndAttrUNXGrpReadChk  ->Create(m_wndAttrPg, -1, _("Read"));
        m_wndAttrUNXGrpReadChk  ->SetSize(110, 55, 60, 22);
        m_wndAttrUNXOthReadChk  = new wxCheckBox;
        m_wndAttrUNXOthReadChk  ->Create(m_wndAttrPg, -1, _("Read"));
        m_wndAttrUNXOthReadChk  ->SetSize(190, 55, 60, 22);
        m_wndAttrUNXOwnWriteChk = new wxCheckBox;
        m_wndAttrUNXOwnWriteChk ->Create(m_wndAttrPg, -1, _("Write"));
        m_wndAttrUNXOwnWriteChk ->SetSize( 25, 78, 60, 22);
        m_wndAttrUNXGrpWriteChk = new wxCheckBox;
        m_wndAttrUNXGrpWriteChk ->Create(m_wndAttrPg, -1, _("Write"));
        m_wndAttrUNXGrpWriteChk ->SetSize(110, 78, 60, 22);
        m_wndAttrUNXOthWriteChk = new wxCheckBox;
        m_wndAttrUNXOthWriteChk ->Create(m_wndAttrPg, -1, _("Write"));
        m_wndAttrUNXOthWriteChk ->SetSize(190, 78, 60, 22);
        m_wndAttrUNXOwnExecChk  = new wxCheckBox;
        m_wndAttrUNXOwnExecChk  ->Create(m_wndAttrPg, -1, _("Execute"));
        m_wndAttrUNXOwnExecChk  ->SetSize( 25,100, 60, 22);
        m_wndAttrUNXGrpExecChk  = new wxCheckBox;
        m_wndAttrUNXGrpExecChk  ->Create(m_wndAttrPg, -1, _("Execute"));
        m_wndAttrUNXGrpExecChk  ->SetSize(110,100, 60, 22);
        m_wndAttrUNXOthExecChk  = new wxCheckBox;
        m_wndAttrUNXOthExecChk  ->Create(m_wndAttrPg, -1, _("Execute"));
        m_wndAttrUNXOthExecChk  ->SetSize(190,100, 60, 22);
        #endif
        '''
        self.m_wndAgeRelationCbo.Append('<')
        self.m_wndAgeRelationCbo.Append('=')
        self.m_wndAgeRelationCbo.Append('>')
        self.m_wndAgeRelationCbo.SetSelection(0)
        self.m_wndAgeUnitCbo.Append('hours')
        self.m_wndAgeUnitCbo.Append('days')
        self.m_wndAgeUnitCbo.Append('weeks')
        self.m_wndAgeUnitCbo.Append('months')
        self.m_wndAgeUnitCbo.Append('years')
        self.m_wndAgeUnitCbo.SetSelection(0)
        self.m_wndSizeRelationCbo.Append('<')
        self.m_wndSizeRelationCbo.Append('=')
        self.m_wndSizeRelationCbo.Append('>')
        self.m_wndSizeRelationCbo.SetSelection(0)
        self.m_wndSizeUnitCbo.Append('bytes')
        self.m_wndSizeUnitCbo.Append('kB')
        self.m_wndSizeUnitCbo.Append('MB')
        self.m_wndSizeUnitCbo.Append('GB')
        self.m_wndSizeUnitCbo.SetSelection(0)

        self.SetDimensions(0, 0, TAB_WIDTH + 100, TAB_HEIGTH + 25);
        self.Centre();
        dummy = wxCommandEvent ()
        self.OnDateAgeChk(dummy)
        self.OnDateFromChk(dummy)
        self.OnDateToChk(dummy)
        self.OnSizeChk(dummy)
        self.OnAttrChk(dummy)

        self.m_wndOkBtn.SetDefault()
        self.m_wndFileNameEdit.SetFocus()

        EVT_BUTTON(self, BTN_OK,          self.OnOk)
        EVT_BUTTON(self, BTN_CANCEL,      self.OnCancel)
        EVT_BUTTON(self, BTN_GOTO,        self.OnGoto)
        EVT_BUTTON(self, BTN_PICK_FROM,   self.OnPickFromDate)
        EVT_BUTTON(self, BTN_PICK_TO,     self.OnPickToDate)
        EVT_CHECKBOX(self, CHK_SUBDIR,    self.OnSubdirChk)
        EVT_CHECKBOX(self, CHK_CASE,      self.OnCaseChk)
        EVT_CHECKBOX(self, CHK_DATE_AGE,  self.OnDateAgeChk)
        EVT_CHECKBOX(self, CHK_DATE_FROM, self.OnDateFromChk)
        EVT_CHECKBOX(self, CHK_DATE_TO,   self.OnDateToChk)
        EVT_CHECKBOX(self, CHK_SIZE,      self.OnSizeChk)
        EVT_CHECKBOX(self, CHK_ATTR,      self.OnAttrChk)

    def SetPathDefault (self, strDir):
        self.m_strDirPattern = strDir
        self.m_wndFilePathEdit.SetValue(self.m_strDirPattern)

    def OnOk (self, event):
        #print 'def OnOk (self, event):'
        #resize dialog to 'drop' list control with results
        self.m_bResultsVisible = False
        self.SwapGuiMode()

        #stop if search thread already started
        if(NULL != self.m_pThread and self.m_pThread.m_bDone == False and self.m_pThread.IsRunning()):
            self.m_pThread.Abort()
            if(self.m_pThread.m_bDone == False and self.m_pThread.IsRunning()):
                #wait for termination
                #TODO
                pass
                #self.m_pThread.Wait()

            #delete m_pThread;
            #m_pThread = NULL;
            return

        self.m_wndOkBtn.SetLabel(_("Stop"))
        self.m_wndResultList.DeleteAllItems()

        #store search values
        self.m_bRecursive = self.m_wndSearchSubdirChk.IsChecked()
        self.m_objSearchDesc.Clear()
        #TOFIX support for 'do not show files'
        self.m_objSearchDesc.SetNameGroup(self.m_wndFileNameEdit.GetValue(), '')
        self.m_objSearchDesc.SetContentsGroup(self.m_wndFileTextEdit.GetValue(), self.m_wndCaseSensitiveChk.IsChecked())
        if(self.m_wndAttrChk.IsChecked()):
            nAttrShow = 0
            nAttrHide = 0
            #ifdef __WXMSW__
            if(self.m_wndAttrDOSArchiveChk.IsChecked()):
                nAttrShow = nAttrShow | ATTR_ARCH;
            if(self.m_wndAttrDOSHiddenChk.IsChecked()):
                nAttrShow = nAttrShow | ATTR_HIDDEN;
            if(self.m_wndAttrDOSSystemChk.IsChecked()):
                nAttrShow = nAttrShow | ATTR_SYSTEM;
            if(self.m_wndAttrDOSReadOnlyChk.IsChecked()):
                nAttrShow = nAttrShow | ATTR_RONLY;
            if(self.m_wndAttrDOSDirectoryChk.IsChecked()):
                nAttrShow = nAttrShow | ATTR_DIR;
            #else
            '''
            nAttrShow |= ATTR_UNIX;
            if(m_wndAttrUNXOwnReadChk->IsChecked())     nAttrShow |= ATTR_R_USR;
            if(m_wndAttrUNXOwnWriteChk->IsChecked())        nAttrShow |= ATTR_W_USR;
            if(m_wndAttrUNXOwnExecChk->IsChecked())     nAttrShow |= ATTR_X_USR;
            if(m_wndAttrUNXGrpReadChk->IsChecked())     nAttrShow |= ATTR_R_GRP;
            if(m_wndAttrUNXGrpWriteChk->IsChecked())        nAttrShow |= ATTR_W_GRP;
            if(m_wndAttrUNXGrpExecChk->IsChecked())     nAttrShow |= ATTR_X_GRP;
            if(m_wndAttrUNXOthReadChk->IsChecked())     nAttrShow |= ATTR_R_OTH;
            if(m_wndAttrUNXOthWriteChk->IsChecked())        nAttrShow |= ATTR_W_OTH;
            if(m_wndAttrUNXOthExecChk->IsChecked())     nAttrShow |= ATTR_X_OTH;
            '''
            #endif
            self.m_objSearchDesc.SetAttrGroup(nAttrShow, nAttrHide)

        if(self.m_wndSizeChk.IsChecked()):
            #TOFIX? 64 bit support atoi?
            if len (self.m_wndSizeValueEdit.GetValue()) > 0:
                nSize = int (self.m_wndSizeValueEdit.GetValue())
                nRelation   = self.m_wndSizeRelationCbo.GetSelection()
                nUnit       = self.m_wndSizeUnitCbo.GetSelection()
                #print nSize, nRelation, nUnit
                self.m_objSearchDesc.SetSizeGroup(nSize, nRelation, nUnit)

        if(self.m_wndDateAgeChk.IsChecked() and len(self.m_wndAgeValueEdit.GetValue()) > 0):
            self.m_objSearchDesc.AddDateGroup( FILTER_DateAge,
                    int (self.m_wndAgeValueEdit.GetValue()),
                    self.m_wndAgeRelationCbo.GetSelection(),
                    self.m_wndAgeUnitCbo.GetSelection())

        if(self.m_wndDateFromChk.IsChecked() and len (self.m_wndDateFromEdit.GetValue()) > 0):
            self.m_objSearchDesc.AddDateGroup(FILTER_DateFrom, self.m_dateFrom.GetTicks(), 0, 0)

        if(self.m_wndDateToChk.IsChecked() and len (self.m_wndDateToEdit.GetValue()) > 0):
            self.m_objSearchDesc.AddDateGroup(FILTER_DateTo, self.m_dateFrom.GetTicks(), 0, 0)

        #prepare and start search thread
        self.m_pThread = FileSearchThread()
        self.m_pThread.m_bAbort = False
        self.m_pThread.m_pWnd = self
        self.m_pThread.m_objInfo = self.m_objSearchDesc
        self.m_pThread.m_strDirectory = self.m_wndFilePathEdit.GetValue()
        self.m_pThread.m_pResultLst = self.m_lstResult
        self.m_pThread.Create()
        #self.m_pThread.Run()
        #TODO: remove this later
        #self.m_pThread.Entry ()

    def OnCancel(self, event):
        #print 'def OnCancel(self, event):'
        #stop if search thread already started
        if(NULL != self.m_pThread and self.m_pThread.m_bDone == False and self.m_pThread.IsRunning()):
            self.m_pThread.Abort()
            if(self.m_pThread.m_bDone == False and self.m_pThread.IsRunning()):
                #wait for termination
                #TODO
                pass
                #self.m_pThread.Wait()
            #delete m_pThread
            #m_pThread = NULL

        self.EndModal(wxCANCEL)

    def OnGoto(self, event):
        nItem = self.m_wndResultList.GetNextItem(-1, wxLIST_NEXT_ALL, wxLIST_STATE_FOCUSED)
        if(nItem >= 0):
            item = VfsItem()
            item = self.m_lstResult.GetAtRaw(nItem)

            #TOFIX move to Vfs manager, allow for other Vfs than Vfs_Local
            #DECLARE_APP(AtolApp)
            #AtolApp &App = wxGetApp();
            #MainFrame *pFrm = App.GetFrame();
            #App = wxGetApp()
            #pFrm = App.GetFrame()
            pFrm = wxGetApp().GetFrame()
            if(pFrm):
                pFrm.GetActivePanel().m_pFileList.SetDirectory(item.m_strPath)
                pFrm.GetActivePanel().m_pFileList.ClearSelection()
                nPos = pFrm.GetActivePanel().m_pFileList.GetListing().FindItem(item.GetName())
                if(nPos >= 0):
                    nStyle = wxLIST_STATE_FOCUSED|wxLIST_STATE_SELECTED
                    pFrm.GetActivePanel().m_pFileList.SetItemState(nPos, nStyle, nStyle)
                    pFrm.GetActivePanel().m_pFileList.EnsureVisible(nPos)

            self.EndModal(wxOK);
        else:
            wxMessageBox(_("No file selected!"))

    def OnPickFromDate(self, event):
        x, y = self.m_wndDateFromPickBtn.GetPosition()

        dlg = CDatePickerDlg (self)
        #dlg.m_x = x
        #dlg.m_y = y
        dlg.SetSizePos (x, y)
        if wxOK == dlg.ShowModal():
            self.m_dateFrom = dlg.m_date
            #TODO:dlg.m_date.FormatISODate() wirft error heraus
            self.m_wndDateFromEdit.SetValue(dlg.m_date.FormatISODate())
            #print dlg.m_date, self.m_dateFrom
            #self.m_wndDateFromEdit.SetValue(dlg.m_date)

    def OnPickToDate(self, event):
        x, y = self.m_wndDateFromPickBtn.GetPosition()
        dlg = CDatePickerDlg (self)
        dlg.SetSizePos (x, y)
        if wxOK == dlg.ShowModal():
            self.m_dateTo = dlg.m_date
            #TODO:dlg.m_date.FormatISODate() wirft error heraus
            #print dlg.m_date
            #print self.m_dateTo
            #TODO: wieder heraus
            dlg.m_date = wxDateTime_Now()
            self.m_wndDateToEdit.SetValue(dlg.m_date.FormatISODate())
            #print dlg.m_date, self.m_dateFrom
            #self.m_wndDateFromEdit.SetValue(dlg.m_date)

    def OnSubdirChk(self, event):
        pass
        #print 'def OnSubdirChk(self, event):'

    def OnCaseChk(self, event):
        pass
        #print 'def OnCaseChk(self, event):'

    def OnDateAgeChk(self, event):
        #print 'def OnDateAgeChk(self, event):'
        bCheck = self.m_wndDateAgeChk.IsChecked()
        self.m_wndAgeRelationCbo.Enable(bCheck)
        self.m_wndAgeValueEdit.Enable(bCheck)
        self.m_wndAgeUnitCbo.Enable(bCheck)

    def OnDateFromChk(self, event):
        #print 'def OnDateFromChk(self, event):'
        bCheck = self.m_wndDateFromChk.IsChecked()
        self.m_wndDateFromEdit.Enable(bCheck)
        self.m_wndDateFromPickBtn.Enable(bCheck)

    def OnDateToChk(self, event):
        #print 'def OnDateToChk(self, event):'
        bCheck = self.m_wndDateToChk.IsChecked()
        self.m_wndDateToEdit.Enable(bCheck)
        self.m_wndDateToPickBtn.Enable(bCheck)

    def OnSizeChk(self, event):
        #print 'def OnSizeChk(self, event):'
        bCheck = self.m_wndSizeChk.IsChecked()
        self.m_wndSizeRelationCbo.Enable(bCheck)
        self.m_wndSizeValueEdit.Enable(bCheck)
        self.m_wndSizeUnitCbo.Enable(bCheck)

    def OnAttrChk(self, event):
        #print 'def OnAttrChk(self, event):'
        bCheck = self.m_wndAttrChk.IsChecked()
        #ifdef __WXMSW__
        #//if 0
        self.m_wndAttrDOSArchiveChk.Enable(bCheck);
        self.m_wndAttrDOSHiddenChk.Enable(bCheck);
        self.m_wndAttrDOSSystemChk.Enable(bCheck);
        self.m_wndAttrDOSReadOnlyChk.Enable(bCheck);
        self.m_wndAttrDOSDirectoryChk.Enable(bCheck);
        '''
        #else
            m_wndAttrUNXOwnReadChk  ->Enable(bCheck);
            m_wndAttrUNXOwnWriteChk ->Enable(bCheck);
            m_wndAttrUNXOwnExecChk  ->Enable(bCheck);
            m_wndAttrUNXGrpReadChk  ->Enable(bCheck);
            m_wndAttrUNXGrpWriteChk ->Enable(bCheck);
            m_wndAttrUNXGrpExecChk  ->Enable(bCheck);
            m_wndAttrUNXOthReadChk  ->Enable(bCheck);
            m_wndAttrUNXOthWriteChk ->Enable(bCheck);
            m_wndAttrUNXOthExecChk  ->Enable(bCheck);
        #endif
        '''

    def SwapGuiMode(self):
        #print 'swap'
        self.m_bResultsVisible = ~self.m_bResultsVisible
        self.m_wndResultList.Show(self.m_bResultsVisible)
        self.m_wndGotoBtn.Show(self.m_bResultsVisible)

        x, y = self.GetPositionTuple()

        if(self.m_bResultsVisible):
            self.SetDimensions(x, y, TAB_WIDTH + 100, TAB_HEIGTH + 175);
            self.m_wndResultList.SetDimensions(3, TAB_HEIGTH+3, TAB_WIDTH, 147)
            self.m_wndGotoBtn.SetDimensions(TAB_WIDTH + 10, TAB_HEIGTH+3, 80, 22)
        else:
            self.SetDimensions(x, y, TAB_WIDTH + 100, TAB_HEIGTH + 25)
            self.m_wndResultList.SetSize(0, 0, 0, 0)

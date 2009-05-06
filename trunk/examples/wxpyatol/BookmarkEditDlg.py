from wxPython.wx import *
from BrowseBookmarkList import *

#include 'BookmarkEditDlg.h'

ID_OK_BTN        =  10001
ID_CANCEL_BTN    =  10002
ID_ADD_BTN       =  10003
ID_DELETE_BTN    =  10004
ID_LIST          =  10005

class BookmarkEditDlg (wxDialog):
    def __init__ (self):
        wxDialog.__init__(self, NULL, -1, _("Bookmark manager"), wxDefaultPosition, wxDefaultSize, wxCAPTION)
        self.m_wndBookList = wxListBox (self, ID_LIST)
        self.m_wndAddBtn = wxButton (self, ID_ADD_BTN, _("Add"), wxPoint(0,0))
        self.m_wndDeleteBtn = wxButton (self, ID_DELETE_BTN, _("Delete"), wxPoint(0,0))
        self.m_wndOkBtn = wxButton (self, ID_OK_BTN, _("OK"), wxPoint(0,0))
        self.m_wndCancelBtn = wxButton (self, ID_CANCEL_BTN, _("Cancel"), wxPoint(0,0))
        self.m_wndTitleEdit = wxTextCtrl (self, -1)
        self.m_wndPathEdit = wxTextCtrl (self, -1)
        self.m_wndTitleLabel = wxStaticText (self, -1, _("Title:"), wxPoint(0,0))
        self.m_wndPathLabel = wxStaticText (self, -1, _("Path"), wxPoint(0,0))
        self.m_lstBooks = BrowseBookmarkList ()

        self.m_wndBookList   .SetDimensions(   0,   5, 250, 102)
        self.m_wndAddBtn     .SetDimensions( 260,   5,  80,  22)
        self.m_wndDeleteBtn  .SetDimensions( 260,  30,  80,  22)
        self.m_wndOkBtn      .SetDimensions( 260,  60,  80,  22)
        self.m_wndCancelBtn  .SetDimensions( 260,  86,  80,  22)
        self.m_wndTitleEdit  .SetDimensions(  50, 120, 200,  22)
        self.m_wndPathEdit   .SetDimensions(  50, 145, 200,  22)
        self.m_wndTitleLabel .SetDimensions(   5, 125,  45,  22)
        self.m_wndPathLabel  .SetDimensions(   5, 150,  45,  22)

        self.SetDimensions(0, 0, 350, 200)
        self.Centre()

        self.m_wndOkBtn.SetDefault();

        self.m_lstBooks.Load();
        self.RebuildList();

        EVT_BUTTON(self, ID_OK_BTN,       self.OnOk)
        EVT_BUTTON(self, ID_CANCEL_BTN,   self.OnCancel)
        EVT_BUTTON(self, ID_ADD_BTN,      self.OnAdd)
        EVT_BUTTON(self, ID_DELETE_BTN,   self.OnDelete)
        EVT_LISTBOX(self, ID_LIST,        self.OnListSelection)


    def OnOk(self, event):
        self.m_lstBooks.Save()
        self.EndModal(wxOK)

    def OnCancel(self, event):
        self.EndModal(wxOK)

    def OnAdd(self, event):

        strTitle = self.m_wndTitleEdit.GetValue()
        strPath  = self.m_wndPathEdit.GetValue()

        if(strTitle == '' or strPath == ''):
            wxMessageBox(_("Both title and path must be filled!"))
            return

        nPos = self.m_lstBooks.FindBookByTitle(strTitle)
        if(nPos >= 0):
            nRes = wxMessageBox(_("This will overwrite existing bookmark with same title!\nProceed?"), _("Warning"), wxYES_NO)
            if(wxYES != nRes):
                return
            self.m_lstBooks.Remove (nPos)

        self.m_lstBooks.Insert(strTitle, strPath)
        self.RebuildList()

    def OnDelete(self, event):
        nPos = self.m_wndBookList.GetSelection()
        if(nPos >= 0):
            strTitle = self.m_wndBookList.GetString(nPos);
            if(strTitle != ''):
                nPos = self.m_lstBooks.FindBookByTitle(strTitle)
                if(nPos >= 0):
                    self.m_lstBooks.Remove (nPos)
            self.RebuildList();

    def OnListSelection(self, event):
        #wxpython (wxwindows direct access to member m_commandInt)
        strTitle = self.m_wndBookList.GetString(event.GetInt())
        if(strTitle != ''):
            nPos = self.m_lstBooks.FindBookByTitle(strTitle)
            if(nPos >= 0):
                self.m_wndTitleEdit.SetValue(self.m_lstBooks.GetBookTitle(nPos))
                self.m_wndPathEdit.SetValue(self.m_lstBooks.GetBookPath(nPos))

    def RebuildList(self):
        self.m_wndBookList.Clear()
        for i in range (self.m_lstBooks.GetCount()):
            self.m_wndBookList.Append(self.m_lstBooks.GetBookTitle(i))

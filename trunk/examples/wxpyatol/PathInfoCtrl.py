from wxPython.wx import *
#from IniFile import *
from PathName import *
from BrowseBookmarkList import *
from PopupMenu import *
from NameInputDlg import *
from BookmarkEditDlg import *
from StaticText import *

class PathInfoCtrl (CStaticText):
    def __init__(self, pParent, id, str, ptr, size, param):
        CStaticText.__init__ (self, pParent, id, str, ptr, size, param)
        EVT_LEFT_DCLICK(self, self.OnLMouseDClick)
  #void OnLMouseDClick(wxMouseEvent &event);

  #DECLARE_EVENT_TABLE() // wxWindows event table

    #def OnLMouseDClick(wxMouseEvent &event)
    def OnLMouseDClick(self, event):
        books = BrowseBookmarkList ()
        books.Load()

        pParent = self.GetParent()
        strCurDir = pParent.m_pFileList.m_pVfs.GetDir()

        #show popup menu with forward browsing history items
        menu = CPopupMenu ()

        nBookCount = books.GetCount()
        for i in range(nBookCount):
            menu.AppendCheckItem(i+1, books.GetBookTitle(i))

            if(strCurDir == books.GetBookPath(i)):
                menu.Check(i+1, True)

        menu.AppendSeparator();
        menu.Append(nBookCount+1, _("Add current dir"))
        menu.Append(nBookCount+2, _("Configure"))

        #wxPython
        self.PopupMenuXY(menu, event.m_x, event.m_y)#/*20*/);

        #execute
        nCmdID = menu.GetSelectedID()
        if (nCmdID <= 0):
            return;

        if(nCmdID == nBookCount+1):
            #wxFileName file(strCurDir);
            #add current directory
            dlg = CNameInputDlg ()
            dlg.SetTitle(_("Set entry title"))
            #dlg.m_strValue = file.GetName();
            if(wxOK == dlg.ShowModal()):
                if(books.Insert(dlg.m_strValue, strCurDir)):
                    books.Save()
                else:
                    wxMessageBox(_("Failed to add bookmark!"))
        elif(nCmdID == nBookCount+2):
            #configure
            dlg = BookmarkEditDlg ()
            dlg.ShowModal()
        else:
            strPath = books.GetBookPath(nCmdID-1)
            pParent.m_pFileList.SetDirectory(strPath, True)

    '''
    #TODO
    #ifdef __WXGTK__
    def SetBackgroundColour(self, colour):
        st = CStaticText ()
        st.SetBackgroundColour(colour)

    def SetForegroundColour(self, colour):
        st = CStaticText ()
        st.SetForegroundColour(colour)
    #endif
    '''


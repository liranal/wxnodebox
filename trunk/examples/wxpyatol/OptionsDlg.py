from wxPython.wx import *
from IniFile import *
from PathName import *
from OptionsStartupDlg import *
from OptionsGUIDlg import *
from OptionsOperationDlg import *
#include 'wx/button.h'
#include 'wx/treectrl.h'
#include 'OptionsDlg.h'
#include 'OptionsStartupDlg.h'
#include 'OptionsOperationDlg.h'
#include 'OptionsGUIDlg.h'

#include 'wx/msgdlg.h'
#include 'wx/intl.h'

#ifdef __WXMSW__
#support to start application at boot time
#include 'wxutil.h'
from Globals import *

from BootStart import *
BOOT_KEY = 'Atol'
#endif

BTN_OK      = 1
BTN_CANCEL  = 2
ID_TREE     = 3

PAGE_COUNT  = 3

#classe (auch intern wie vfslisting)
class PAGE_DATA:
    def __init__ (self):
        self.pPageWnd = None                     #    wxWindow *pPageWnd
        nID = -1                                 #    wxTreeItemId nID

class COptionsDlg(wxDialog):
    def __init__ (self, pParent = None):
        wxDialog.__init__ (self, pParent, -1, _("Program settings"), wxDefaultPosition, wxDefaultSize, wxCAPTION)

        self.m_wndOptionsTree = wxTreeCtrl(self, ID_TREE, wxPoint(0,0), wxDefaultSize, wxTR_HAS_BUTTONS|wxTR_HIDE_ROOT|wxTR_LINES_AT_ROOT|wxTR_SINGLE)
        self.m_wndOkBtn = wxButton (self, BTN_OK,   _("OK"), wxPoint(0,0))
        self.m_wndCancelBtn = wxButton (self, BTN_CANCEL, _("Cancel"), wxPoint(0,0))

        self.m_wndOptionsTree.SetDimensions(10, 10,  140, 120)
        self.m_wndOkBtn      .SetDimensions(10, 150,  80, 22)
        self.m_wndCancelBtn  .SetDimensions(95, 150,  80, 22)
        self.m_pCurPage = None

        self.SetDimensions(0, 0, 300, 200)
        self.Centre()

        nRootID = self.m_wndOptionsTree.AddRoot('')
        self.m_arPages = []
        for i in range (PAGE_COUNT):
            self.m_arPages.append(PAGE_DATA())
        self.m_arPages[0].nID = self.m_wndOptionsTree.AppendItem(nRootID, _("Startup"))
        self.m_arPages[1].nID = self.m_wndOptionsTree.AppendItem(nRootID, _("Operation"))
        self.m_arPages[2].nID = self.m_wndOptionsTree.AppendItem(nRootID, _("GUI"))

        self.m_wndOkBtn.SetFocus()
        self.m_wndOkBtn.SetDefault()

        #load preferences
        p = PathName ()
        strFile = p.GetIniDirectory()
        #print strFile
        #TOFIX
        strFile += '/atol.ini'

        self.m_iniFile = IniFile ()
        self.m_iniFile.Load(strFile)

        #TOFIX select last used branch?
        self.m_wndOptionsTree.SelectItem(self.m_arPages[0].nID)
        #sonst wird dialog nicht aufgemacht
        self.OnTreeSelChanged (None)



        EVT_BUTTON(self, BTN_OK,      self.OnOk)
        EVT_BUTTON(self, BTN_CANCEL,  self.OnCancel)
        EVT_TREE_SEL_CHANGED(self, ID_TREE, self.OnTreeSelChanged)



    def OnOk(self, event):
        #update data
        #print 'OnOk'

        #Startup page
        if(None != self.m_arPages[0].pPageWnd):

            pPage = self.m_arPages[0].pPageWnd

            if (pPage.m_wndSingleInstChk.IsChecked()):
                nValue = 1
            else:
                nValue = 0
            self.m_iniFile.SetValue('Default', 'SingleInstance', nValue)

            if (pPage.m_wndShowSplashChk.IsChecked()):
                nValue = 1
            else:
                nValue = 0
            self.m_iniFile.SetValue('Default', 'ShowSplash', nValue)

            if (pPage.m_wndShowTipsChk.IsChecked()):
                nValue = 1
            else:
                nValue = 0
            self.m_iniFile.SetValue('Default', 'ShowTips', nValue)

            if (pPage.m_wndRestorePathsChk.IsChecked()):
                nValue = 1
            else:
                nValue = 0
            self.m_iniFile.SetValue('Default', 'RestorePaths', nValue)

            #ifdef __WXMSW__
            bSet = pPage.m_wndStartAtBootChk.IsChecked()
            #if(!RunProgramAtBoot(BOOT_KEY, GetExecutablePath(), bSet))
            #    wxMessageBox(_('Failed to register Atol to be started at boot time!'))
            #endif

        self.m_iniFile.Save()
        self.EndModal(wxOK)

    def OnCancel(self, event):
        self.EndModal(wxCANCEL)

    def OnTreeSelChanged(self, event = None):
        #TOFIX swap to another page

        #find page info slot
        nPos = -1
        if event == None:
            nID = self.m_arPages[0].nID
        else:
            nID = event.GetItem()
        for i in range(PAGE_COUNT):
            if(self.m_arPages[i].nID == nID):
                nPos = i
                break

        #//hide previous selected page
        if(self.m_pCurPage):
            self.m_pCurPage.Show(False)

        #set new dialog page
        if(nPos >= 0):
            if(None == self.m_arPages[nPos].pPageWnd):
                self.m_arPages[nPos].pPageWnd = self.DialogPageFactory(nPos)

            if(None != self.m_arPages[nPos].pPageWnd):
                self.m_pCurPage = self.m_arPages[nPos].pPageWnd
                self.m_arPages[nPos].pPageWnd.SetDimensions(150, 10, 150, 120)
                self.m_arPages[nPos].pPageWnd.Show()

    def DialogPageFactory (self, nSlot):
        if (nSlot == 0):

            pPage = COptionsStartupDlg(self)

            #init data
            nValue = int (self.m_iniFile.GetValue('Default', 'SingleInstance', 0))
            if(nValue > 0):
                pPage.m_wndSingleInstChk.SetValue(true)
            nValue = int (self.m_iniFile.GetValue('Default', 'ShowSplash', 0))
            if(nValue > 0):
                pPage.m_wndShowSplashChk.SetValue(true)
            nValue = int (self.m_iniFile.GetValue('Default', 'ShowTips', 1))
            if(nValue > 0):
                pPage.m_wndShowTipsChk.SetValue(true)
            nValue = int (self.m_iniFile.GetValue('Default', 'RestorePaths', 0))
            if(nValue > 0):
                pPage.m_wndRestorePathsChk.SetValue(true)

            #TODO
            #ifdef __WXMSW__
            #if(IsBootKeySet(BOOT_KEY))
            #    ((COptionsStartupDlg *)pPage).m_wndStartAtBootChk.SetValue(true)
            #endif
        elif (nSlot == 1):
            pPage = COptionsOperationDlg(self)
        elif (nSlot == 2):
            pPage = COptionsGUIDlg(self)

        return pPage


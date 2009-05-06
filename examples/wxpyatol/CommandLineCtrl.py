from wxPython.wx import *
from Vfs import *
from WxUtil import *

class CommandLineCtrl(wxComboBox):
    def __init__ (self, pParent):
        wxComboBox.__init__(self, pParent, -1, '')#, style=wxCB_DROPDOWN|wxPROCESS_ENTER)
        self.nMaxCommandsCached = 20

        EVT_COMBOBOX(self, -1, self.OnComboSelection)
        EVT_TEXT_ENTER(self, -1, self.OnComboExecute)


    def AppendString(self, strData):
        self.SetValue(self.GetValue() + strData)

        #//ensure we get focus
        self.SetFocus();
        self.SetInsertionPoint(len (self.GetValue()))


    def DoCreate(self, pParent):
        #wxComboBox.Create(self, pParent, -1)
        #wxComboBox.Create(self, pParent, -1)
        pass


    def ClearCmd(self):
        if len (self.GetValue()) > 0:
            self.SetValue('')
            return True

        return False

    def OnComboSelection (self, event):
        event.Skip()

    def OnComboExecute(self, event):
        self.ExecuteCmd()

    #bool CommandLineCtrl::ExecuteCmd()
    def ExecuteCmd(self):
        #print 'execute command'
        strContent = self.GetValue()
        #print strContent
        if len (strContent) > 0:
            pFrame = self.GetParent()
            #Vfs *pVfs = pFrame->GetActivePanel()->m_pFileList->m_pVfs;
            pVfs = pFrame.GetActivePanel().m_pFileList.m_pVfs
            strDir  = pVfs.GetDir()

            #//TOFIX send to current VFS for execution (might block!!! - COp)
            if(pVfs.GetType() == VFS_LOCAL):
                ExecuteFile (strContent, NULL, strDir, pFrame.GetHandle())

            #//clear the combo box
            self.SetValue('')

            #//refresh command history
            nPos = self.FindString(strContent)
            if nPos >= 0:
                #//delete string copy from combo
                self.Delete(nPos)

            self.Append(strContent)

            #//ensure cache is not overgrown
            nCount = self.GetCount()
            if(nCount > self.nMaxCommandsCached):
                for i in range (nCount-nMaxCommandsCached):
                    self.Delete(0)
            return True

        return False

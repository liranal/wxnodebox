from wxPython.wx import *
from MainFrame import *

g_SingleInstanceChecker = None

class WxPyAtolApp(wxApp):
    def OnInit(self):
        wxInitAllImageHandlers()
        if not self.CheckSingleInstance():
            return False

        self.m_MainFrame = MainFrame()
        #print self.GetAppName()

        self.m_MainFrame.Show()
        self.SetTopWindow(self.m_MainFrame)
        return True

    def GetFrame (self):
        #print g_SingleInstanceChecker
        return self.m_MainFrame

    def CheckSingleInstance(self):
        #//read INI file to see if single instance check set
        p = PathName ()
        strFile = p.GetIniDirectory()
        #//TOFIX
        strFile += '/atol.ini'

        ini = IniFile ()
        if ini.Load(strFile):
            nValue = int (ini.GetValue('Default', "SingleInstance", 0))
            if nValue > 0:
                #//check if we have multiple instances of this application
                global g_SingleInstanceChecker
                g_SingleInstanceChecker = wxSingleInstanceChecker ("wxPyAtol")
                #print g_SingleInstanceChecker
                if g_SingleInstanceChecker.IsAnotherRunning():
                    #mit _("text") geht es zu diesem Zeitpunkt noch nicht
                    wxLogDebug ("Another Atol instance detected, aborting.")
                    #wxLogError(_("Another Atol instance detected, aborting."))
                    return False

        return True

def main():
    application = WxPyAtolApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()

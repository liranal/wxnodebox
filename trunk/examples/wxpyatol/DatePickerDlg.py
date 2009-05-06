from wxPython.wx import *
from wxPython.calendar import *

CAL_CTRL  =  1

class CDatePickerDlg(wxDialog):
    def __init__ (self, pParent):
        wxDialog.__init__ (self, pParent, -1, _("Choose date"), wxDefaultPosition, wxDefaultSize, wxCAPTION|wxSYSTEM_MENU)
        self.m_wndCalendarCtrl = wxCalendarCtrl (self, CAL_CTRL, wxDateTime_Now(), wxDefaultPosition, wxDefaultSize, wxCAL_MONDAY_FIRST|wxRAISED_BORDER)

        self.m_wndCalendarCtrl.SetDimensions(0, 0, 180, 135);
        self.SetDimensions(0, 0, 190, 160)
        self.Centre()
        self.m_date = 150
        #EVT_INIT_DIALOG(CDatePickerDlg::OnInitDialog)
        EVT_CALENDAR(self, CAL_CTRL, self.OnDaySelected)

    def SetSizePos (self, x, y):
        self.m_x = x
        self.m_y = y
        self.SetDimensions(self.m_x, self.m_y, 190, 160)

    #CDatePickerDlg::OnDaySelected(wxCalendarEvent& event)
    def OnDaySelected(self, event):
        self.m_date = event.GetDate()
        #TODO: francesco: m_date ist hier richtig, in Fileserachdlg aber 1.1.70 (0)
        #print self.m_date
        #print "1", self.m_date
        self.EndModal(wxOK)


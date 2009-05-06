from wxPython.wx import *

class CStaticText(wxWindow):
    def __init__ (self, pParent, id, str, ptr, size, param):
        wxWindow.__init__ (self, pParent, id, ptr, size, param, str)
        self.m_strLabel = ''
        self.m_rgbBkg = wxColour (128,128,128)
        self.m_rgbFg = wxBLACK
        EVT_PAINT(self, self.OnPaint)

    def SetLabel(self, strText):
        self.m_strLabel = strText

    #ifdef __WXGTK__
    '''
    def SetBackgroundColour(self, colour):
    self.m_rgbBkg = colour
    void SetForegroundColour(self,  colour):
    self.m_rgbFg = colour
    '''
    #endif

    #def OnPaint(self,wxPaintEvent& evt);
    def OnPaint(self, evt):
        width, height = self.GetSizeTuple()

        dc = wxPaintDC(self)
        dc.BeginDrawing()
        #ifdef __WXMSW__
        pen = wxPen (dc.GetBackground().GetColour(), 1, wxSOLID)
        dc.SetPen(pen)
        dc.SetBrush(dc.GetBackground())
        dc.DrawRectangle(0, 0, width, height)

        dc.SetTextForeground(self.GetForegroundColour())
        dc.DrawText(self.m_strLabel, 0, 0)
        #//dc.SetBrush(wxNullBrush);
        '''
        #TODOLINUX
        #else

            wxPen pen(m_rgbBkg, 1, wxSOLID);
            dc.SetPen(pen);
            wxBrush brush(m_rgbBkg, wxSOLID);
            dc.SetBrush(brush);
            dc.DrawRectangle(0, 0, width, height);

            dc.SetTextForeground(m_rgbFg);
                dc.DrawText(m_strLabel, 0, 0);

            dc.SetBrush(wxNullBrush);
            dc.SetPen(wxNullPen);

        #endif
        '''
        dc.EndDrawing()


    '''
    void CStaticText::SetLabel(const wxString &strText)
    {
        m_strLabel = strText;
    }

    #ifdef __WXGTK__
    void CStaticText::SetBackgroundColour(wxColour colour)
    {
        m_rgbBkg = colour;
    }

    void CStaticText::SetForegroundColour(wxColour colour)
    {
        m_rgbFg  = colour;
    }
    #endif
    '''

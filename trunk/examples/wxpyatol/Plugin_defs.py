from wxPython.wx import *

#// archiver can create new archives
PK_CAPS_NEW      =  1
#// can modify exisiting archives
PK_CAPS_MODIFY   =  2
#// archive can contain multiple files
PK_CAPS_MULTIPLE =  4
#// archiver can delete files
PK_CAPS_DELETE   =  8
#// archiver has options dialog
PK_CAPS_OPTIONS  = 16
#// we can destroy original file after compressing it
PK_CAPS_MOVE     = 32


class tArchiveEntry:
    def __init__(self):
        #self.szPath = 220 * 'u'+ 10 *'a'
        #self.szPath = 259 * ' '
        self.szPath = ' '
        self.nPackSize = 0
        self.nUnpSize = 0
        self.bDir = True
        self.dwAttribs = 0
        self.dwFileCRC = 0
        #wxDateTime_Now()
        #wxDateTime::GetTicks
        #i = wxDateTime (0)
        i = wxDateTimeFromTimeT (0)
        self.tmModified = i.GetTicks()
        #self.tmModified = 16#i.GetTicks()
        #wxDateTime_GetTicks()
        #tmModified = time_t ()

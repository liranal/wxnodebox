import sys
import os
from ctypes import *

startDir = os.getcwd()
_winDir = os.path.join(startDir, '_win')
sys.path.insert(1, _winDir)

APP_VER_STR = '1.1'

CMD_REFRESH            = 1000
CMD_COPY               = 1001
CMD_MOVE               = 1002
CMD_NEXT_PANEL         = 1003
CMD_LDRIVE_MENU        = 1004
CMD_RDRIVE_MENU        = 1005
CMD_DELETE             = 1006
CMD_MKDIR              = 1007
CMD_RENAME             = 1008
CMD_SELECT             = 1109
CMD_DESELECT           = 1110
CMD_FILTER             = 1111
CMD_SELECT_ALL         = 1112
CMD_SELECT_NONE        = 1113
CMD_SELECT_INVERT      = 1114
CMD_FILE_SEARCH        = 1115
CMD_HISTORY_PREV       = 1116
CMD_HISTORY_PREV_POPUP = 1117
CMD_HISTORY_NEXT       = 1118
CMD_HISTORY_NEXT_POPUP = 1119
CMD_OPEN_PROMPT        = 1120
CMD_FILE_EDIT          = 1121
CMD_CMDLINE_ADD_PATH   = 1122
CMD_CMDLINE_ADD_NAME   = 1123
CMD_ABOUT_BOX          = 1124
CMD_TIP_OF_DAY         = 1125
CMD_SWAP_PANELS        = 1126
CMD_EQUAL_PANELS       = 1127
CMD_COMPARE_DIRS       = 1128
CMD_UP_DIR             = 1129
CMD_ROOT_DIR           = 1130
CMD_DIR_SIZE           = 1131
CMD_OPTIONS            = 1132
CMD_SHOW_HIDDEN_FILES  = 1133
CMD_COMPRESS_FILES     = 1134
CMD_LANGUAGE_FIRST     = 1135
CMD_LANGUAGE_LAST      = 1160
CMD_NEXT               = 1161

FILTER_MatchName      =  0x0001
FILTER_MatchSize      =  0x0002
FILTER_MatchDate      =  0x0004
FILTER_MatchAttr      =  0x0008
FILTER_MatchContents  =  0x0020

#additional flags
FILTER_SkipDirMatch   =  0x0040
FILTER_DateFrom       =  0x0080
FILTER_DateTo         =  0x0100
FILTER_DateAge        =  0x0200


#common flags
ATTR_DIR    = 0x0002
ATTR_LINK   = 0x0004

#UNIX only flags
ATTR_R_USR  = 0x0008
ATTR_W_USR  = 0x0010
ATTR_X_USR  = 0x0020
ATTR_R_GRP  = 0x0040
ATTR_W_GRP  = 0x0080
ATTR_X_GRP  = 0x0100
ATTR_R_OTH  = 0x0200
ATTR_W_OTH  = 0x0400
ATTR_X_OTH  = 0x0800

#MSDOS only flags
ATTR_RONLY  = 0x0008
ATTR_ARCH   = 0x0010
ATTR_HIDDEN = 0x0020
ATTR_SYSTEM = 0x0040

#// mask for temporary flags
OPF_TMP_FLAGS_MASK             =  0x007F

#//single file operation settings
OPF_OK                         =  0x0001
OPF_ABORT                      =  0x0002
OPF_SKIP                       =  0x0004
OPF_OVERWRITE                  =  0x0008
OPF_CPY_RENAME                 =  0x0010
OPF_CPY_APPEND                 =  0x0020
OPF_CPY_RESUME                 =  0x0040
OPF_DELETE                     =  0x0080

#//multiple file operation settings
#// TOFIX not used? skip deleting all non-empty dirs ('Dir is not empty?')
OPF_DEL_SKIP_ALL_DIRS          =  0x0100
#// delete all non-empty dirs without asking ('Dir is not empty?')
OPF_DEL_ALL_DIRS               =  0x0200
#// delete all read-only files without asking
OPF_DEL_ALL_RO_FILES           =  0x0400
OPF_CPY_OVERWRITE_ALL          =  0x0800
OPF_CPY_SKIP_ALL               =  0x1000
OPF_CPY_OVERWRITE_ALL_OLDER    =  0x2000

FS_CASE_INSENSITIVE            =  1

g_strTitle = ""
g_strResult = ""
#//TOFIX if we allow multiple ops simultaneously one flag will not be enough
g_nGuiResult = 0

#//NOTE: part of the code flags are ment for current file only
#//      and the others are ment for all files forward inside the same file operation
#// mask for temporary flags
OPF_TMP_FLAGS_MASK  =    0x007F

#//single file operation settings
OPF_OK              =   0x0001
OPF_ABORT           =   0x0002
#//
OPF_SKIP            =   0x0004
#//
OPF_OVERWRITE       =   0x0008
OPF_CPY_RENAME      =   0x0010
OPF_CPY_APPEND      =   0x0020
OPF_CPY_RESUME      =   0x0040
OPF_DELETE          =   0x0080

#//multiple file operation settings
#// TOFIX not used? skip deleting all non-empty dirs ("Dir is not empty?")
OPF_DEL_SKIP_ALL_DIRS       = 0x0100
#// delete all non-empty dirs without asking ("Dir is not empty?")
OPF_DEL_ALL_DIRS            = 0x0200
#// delete all read-only files without asking
OPF_DEL_ALL_RO_FILES        = 0x0400
#//
OPF_CPY_OVERWRITE_ALL       = 0x0800
#//
OPF_CPY_SKIP_ALL            = 0x1000
OPF_CPY_OVERWRITE_ALL_OLDER = 0x2000

VFS_UNKNOVN = 0
VFS_LOCAL = 1
#//Win32 net / SMB
VFS_NET = 2
VFS_ARCHIVE = 3
VFS_FTP = 4
VFS_SFTP = 5
VFS_SITEMAN = 6


MAX_PATH = 260
HICON = c_int

SHGFI_ICON              = 0x000000100
SHGFI_DISPLAYNAME       = 0x000000200
SHGFI_TYPENAME          = 0x000000400
SHGFI_ATTRIBUTES        = 0x000000800
SHGFI_ICONLOCATION      = 0x000001000
SHGFI_EXETYPE           = 0x000002000
SHGFI_SYSICONINDEX      = 0x000004000
SHGFI_LINKOVERLAY       = 0x000008000
SHGFI_SELECTED          = 0x000010000
SHGFI_ATTR_SPECIFIED    = 0x000020000
SHGFI_LARGEICON         = 0x000000000
SHGFI_SMALLICON         = 0x000000001
SHGFI_OPENICON          = 0x000000002
SHGFI_SHELLICONSIZE     = 0x000000004
SHGFI_PIDL              = 0x000000008
SHGFI_USEFILEATTRIBUTES = 0x000000010

class SHFILEINFO(Structure):
    _fields_ = [("hIcon", HICON),
                ("iIcon", c_int),
                ("dwAttributes", c_uint),
                ("szDisplayName", c_char * MAX_PATH),
                ("szTypeName", c_char * 80)]

shfileinfo = SHFILEINFO()


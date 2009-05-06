#! /usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; fill-column: 79; coding: iso-latin-1-unix -*-
#

import commands, grp, pwd, os, shutil, stat, string, time

from wxPython.wx import wxNewId, false, true
from wxPython.wx import wxICON_ERROR, wxOK
from wxPython.wx import wxMessageBox

def IsMountPoint(path, tryMount=0): # tryMount: 0 - don't, 1 - mount, -1 - unmount
    fstabPath = "/etc/fstab"
    path = os.path.normpath(path)
    if not os.path.exists(path) or not os.path.exists(fstabPath): return 0
    f = open(fstabPath)
    while 1:
        l = f.readline()
        if not l: break
        if l[0] != "/": continue
        fspath, mpath = string.split(l)[:2]
        if path in (mpath, fspath):
            f.close()
            if 0 == tryMount: return 1
            elif +1 == tryMount: cmd = "mount"
            elif -1 == tryMount: cmd = "umount"
            status, output = commands.getstatusoutput(cmd + " " + path)
            if status:
                wxMessageBox("Cannot " + cmd + " `" + path + "': " + output, "I/O Error",
                             wxOK | wxICON_ERROR)
                return 0
            return 1
    f.close()
    return 0

def Perms(st):
    fullMode = st[stat.ST_MODE]
    permMode = stat.S_IMODE(fullMode)
    if   stat.S_ISDIR(fullMode):  l = ["d"]
    elif stat.S_ISCHR(fullMode):  l = ["c"]
    elif stat.S_ISBLK(fullMode):  l = ["b"]
    elif stat.S_ISFIFO(fullMode): l = ["p"]
    elif stat.S_ISLNK(fullMode):  l = ["l"]
    elif stat.S_ISSOCK(fullMode): l = ["s"]
    else: l = ["-"]
    i = 0
    for bit in (stat.S_IRUSR, stat.S_IWUSR, stat.S_IXUSR,
                stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP,
                stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH):
        if bit & permMode: ch = "rwx"[i]
        else: ch = "-"
        l.append(ch)
        i = (i + 1) % 3
    if stat.S_ISUID & permMode: l[3] = stat.S_IXUSR & permMode and "s" or "S"
    if stat.S_ISGID & permMode: l[6] = stat.S_IXGRP & permMode and "s" or "S"
    if stat.S_ISVTX & permMode: l[9] = stat.S_IXOTH & permMode and "t" or "T"
    perms = string.join(l, "")
    return perms

def User(st):
    uid = st[stat.ST_UID]
    # for networked systems: local /etc/passwd might not be enough
    try: usr = pwd.getpwuid(uid)[0]
    except KeyError: usr = str(uid)
    return usr

def Group(st):
    gid = st[stat.ST_GID]
    # for networked systems: local /etc/passwd might not be enough
    try: gp = grp.getgrgid(gid)[0]
    except KeyError: gp = str(gid)
    return gp

def PermsUserGroup(path):
    st = os.lstat(path)
    return Perms(st), User(st), Group(st)

def PermsFromPath(path):
    st = os.lstat(path)
    return Perms(st)

def UserFromPath(path):
    st = os.lstat(path)
    return User(st)

def GroupFromPath(path):
    st = os.lstat(path)
    return Group(st)

def Bytes2SizeUnits(bytes):
    """Translates number of bytes into human readable size and units.

    Returns a float and a string. The float is the input value translated
    into more readable units. The string represents the units and is either
    empty or has length two:
    ("KB", "MB", ...) -> ("kilo Bytes", "Mega Bytes", ...)
    """
    size = float(bytes)
    i = 0
    units = ("", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    kb = 1024.0
    # while there are some units left and the size is not human-readable
    # human-readable means: it has 4 or less digits
    while i + 1 < len(units) and size >= 1e4:
        i = i + 1
        size = size / kb
    return size, units[i]

def MsgOS(ex, parent=None):
    #ex.strerror, ex.errno
    msg = "Error message: " + ex.strerror
    label = "OSError"
    flags = wxOK | wxICON_ERROR
    if parent: wxMessageBox(msg, label, flags, parent)
    else:      wxMessageBox(msg, label, flags)

def mtime(path):
    t = time.localtime(os.path.getmtime(path))
    return time.strftime(" %Y/%m/%d %H:%M:%S", t)

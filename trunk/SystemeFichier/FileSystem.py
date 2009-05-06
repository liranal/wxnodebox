#!/usr/bin/python
# -*- coding: latin1 -*-
# - * - c o d i n g : iso-8859-1 - * - 

# les includes
import TreeSystem
import os
import re


class FileManager (TreeSystem.Manager):
    "File System"
    def __init__ (self):
        TreeSystem.Manager.__init__(self)
    def computeBuilder(self):
        return FileBuilder(self)
    def getBuilder (self):
        return self._cBuilder


class FileBuilder (TreeSystem.Builder):
    " File builder"
    def __init__ (self, filesystem):
        TreeSystem.Builder.__init__(self)
        self._cTreeManager = filesystem
    def findRoots (self):
        ### TO DO
        self._listRoot = []
        #uPath = os.getcwdu()
        uPath = "C:\\"
        root = Root( uPath)
        listNewRoot = [ root]
        self._listRoot += listNewRoot
        return listNewRoot
    def returnCurrentDirectory (self):
        """Return a unicode string representing the current working directory.
        Entry: None
        Return: Unicode String
        """
        return os.getcwdu()
    def isDirectory (self, szPath):
        """Test whether a path is a directory
        ##os.stat( os.getcwdu())
        Entry: Unicode String
        Return: Boolean
        """
        #szPath = szPath.strip()
        return os.path.isdir( szPath)
    def isFile (self, szPath):
        """
        Test whether a path is a regular file
        Entry: Unicode String
        Return: Boolean
        """
        return os.path.isfile( szPath)
    def isMount (self, szPath):
        """Test whether a path is a mount point (defined as root of drive)
        Entry: Unicode String
        Return: Boolean
        """
        return os.path.ismount( szPath)
    def baseName ( self, szPath):
        """Returns the final component of a pathname
        Entry: Unicode String
        Return: Unicode String
        """
        return os.path.basename( szPath)
    def computeChildren( self, Node):
        """
        Entry: FileElement
        Return: Liste of FileElements
        """
        listChildren = None
        #listElements = os.listdir( Node._uPath)
        #for elem in listElements:
        #    if os.path.isdir( elem):
        #        child = DirectoryNode( self, elem)
        #    elif os.path.isfile( elem):
        #        child = FileLeaf( self, elem)
        #    self._listChildren.append( child)
        return self._listChildren

class Root (TreeSystem.Node):
    "Root of a file system"
    def __init__ (self, uPath):
        TreeSystem.Node.__init__ (self, uPath, None)
    def getTypeName (self):
        return u"ROOT"
    def computeChildren (self):
        """
        Entry: None
        Return: List of Children
        """
        self._listChildren = []
        listElements = os.listdir( self._uIdName)
        for elem in listElements:
            uChildIdName = self._uIdName + os.sep + elem
            if os.path.isdir( uChildIdName):
                child = Directory( uChildIdName, self)
            elif os.path.isfile( uChildIdName):
                child = File( uChildIdName, self)
            self._listChildren.append( child)
        return self._listChildren
    def computeAttribs (self):
        """
        Entry: None
        Return: Dictionnary of Attribs
        """
        self._dAttribs = {}
        return self._dAttribs

class File (TreeSystem.Node):
    "File Element"
    def __init_ (self, uPath, parent):
        TreeSystem.Node.__init__ (self, uPath, parent)
    def getTypeName (self):
        return u"FILE"
    def computeChildren (self):
        return None
    def computeAttribs (self):
        """
        Entry: None
        Return: Dictionnary of Attribs
        """
        # absolute name = name with path and extension
        self.absolutename = self._uIdName
        # extension
        self.extension = ""
        self.extensionWithDot = ""
        regexp = re.search("\.[0-9a-zA-Z_$]*$", self.absolutename)
        if regexp != None:
            self.extension = regexp.group(0)[1::]
            self.extensionWithDot = regexp.group(0)
        # relative name = name with extension only
        self.relativename = ""
        regexp = [ element for element in self.absolutename.split(os.sep) if element != ""]
        if len(regexp) > 0:
            self.relativename = regexp[-1]
        # relative name withour extention
        self.relativenamewithoutext = self.relativename[0:-len(self.extensionWithDot)]
        info = os.stat( self.absolutename)
        self.mode = info[0]
        self.ino = info[1]
        self.dev = info[2]
        self.nlink = info[3]
        self.uid = info[4]
        self.gid = info[5]
        self.sizeKb = info[6]
        self.atime = info[7] #last acces time
        self.mtime = info[8] #last modify time
        self.ctime = info[9] #create time
        
        self._dAttribs = ("absolutename", "extension", "relativename", "relativenamewithoutext", "mode", "ino", "dev", "nlink", "uid", "gid", "sizeKb", "atime", "mtime", "ctime")
        return self._dAttribs

class Directory (TreeSystem.Node):
    "Directory Element"
    def __init_ (self, parent):
        TreeSystem.Node.__init__ (self, uPath, parent)
    def getTypeName (self):
        return u"DIRECTORY"
    def computeChildren (self):
        # Find included directory and files
        self._listChildren = []
        listElements = os.listdir( self._uIdName)
        for elem in listElements:
            uChildIdName = self._uIdName + os.sep + elem
            if os.path.isdir( uChildIdName):
                child = Directory( uChildIdName, self)
            elif os.path.isfile( uChildIdName):
                child = File( uChildIdName, self)
            else:
                child = None
            self._listChildren.append( child)
        return self._listChildren
    
    def computeAttribs (self):
        """
        Entry: None
        Return: Dictionnary of Attribs
        """
        # absolute name = name with path and extension
        self.absolutename = self._uIdName
        if self.absolutename[-1] == "_" and self.absolutename[0] == "_":
            print 'test'
        # extension
        self.extention = ""
        self.extensionWithDot = ""
        regexp = re.search("\.[a-zA-Z]*$", self.absolutename)
        if regexp != None:
            self.extention = regexp.group(0)[1::]
            self.extensionWithDot = regexp.group(0)
        # relative name = name with extension only
        self.relativename = ""
        regexp = [ element for element in self.absolutename.split(os.sep) if element != ""]
        if len(regexp) > 0:
            self.relativename = regexp[-1]
        # relative name withour extention
        self.relativenamewithoutext = self.relativename[0:-len(self.extensionWithDot)]
        info = os.stat( self.absolutename)
        self.mode = info[0]
        self.ino = info[1]
        self.dev = info[2]
        self.nlink = info[3]
        self.uid = info[4]
        self.gid = info[5]
        self.sizeKb = info[6]
        self.atime = info[7] #last acces time
        self.mtime = info[8] #last modify time
        self.ctime = info[9] #create time
        
        self._dAttribs = ("absolutename", "extension", "relativename", "relativenamewithoutext", "mode", "ino", "dev", "nlink", "uid", "gid", "sizeKb", "atime", "mtime", "ctime")
        return self._dAttribs

#    def getName (self):
#        return self._uPath   
    
   
class FileSystemObject:
    OBJECT_TYPES = [ 'NOINIT', 'DIRECTORY', 'FILE', 'UNKNOWN']
    _iType = 0
    _sType = 'NOINIT'
    _uName = u''
    _uPath = u''
    _uBasename = u''
    def __init__ (self, uName):
        """
        Entry: Unicode String
        """
        self._uName = uPath;
        
    def getType (self):
        """
        Entry: None
        Return: Unicode String
        """
        self.computeType()
        return self._sType;

    def getIdType (self):
        """
        Entry: None
        Return: Integer
        """
        self.computeType()
        return self._iType;
        
    def computeType (self):
        """
        Entry: None
        Return: None
        """
        if self._iType == 0:
            if FileSystem.isDirectory( self._uName) == True:
                self._iType = 1
            elif FileSystem.isFile( self._uName) == True:
                self._iType = 2
            else:
                self._iType = 3
        self._sType = OBJECT_TYPES[self._iType]
        return
        
if __name__ == '__main__':
    print "Begin"
    print "Test"
    print "End"



        
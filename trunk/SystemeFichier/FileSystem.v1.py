#!/usr/bin/python
# -*- coding: latin1 -*-
# - * - c o d i n g : iso-8859-1 - * - 

# les includes
import TreeSystem
import os


class FileManager (TreeSystem.TreeManager):
    "File System"
    def __init__ (self):
        TreeSystem.TreeManager.__init__(self)
        self._cBuilder = FileBuilder( self)
        print "céci est un test"
        return
    def getBuilder (self):
        return self._cBuilder


class FileBuilder (TreeSystem.Builder):
    " File builder"
    def __init__ (self, filesystem):
        TreeSystem.Builder.__init__(self)
        self._cTreeManager = filesystem
    def findRoots (self):
        ### TO DO
        uPath = os.getcwdu()
        root = FileRoot( self._cTreeManager, uPath)
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
        listChildren = []
        listElements = os.listdir( Node._uPath)
        for elem in listElements:
            if os.path.isdir( elem):
                child = DirectoryNode( self, elem)
            elif os.path.isfile( elem):
                child = FileLeaf( self, elem)
            self._listChildren.append( child)
        return self._listChildren
    
class FileElement (TreeSystem.Node):
    def __init__ (self, uPath):
        TreeSystem.Node.__init_(self)
        self._uPath = uPath
    def getName(self):
        """
        Entry: None
        Return: Unicode String
        """
        return self._uPath
    pass

class FileLeaf (TreeSystem.Leaf):
    def __init__ (self, parent, uPath):
        TreeSystem.Leaf.__init__( self, parent)
        self._uPath = uPath
    def getName (self):
        return self._uPath
        
class FileRoot (TreeSystem.Root):
    ""
    #def __init__ (self, treesystem, uPath):
    def __init__ (self, treesystem, uPath):
        TreeSystem.Root.__init__(self, treesystem)
        self._uPath = uPath
        pass
    def computeChildren( self):
        """
        Entry: FileElement
        Return: Liste of FileElements
        """
        self._listChildren = []
        listElements = os.listdir( self._uPath)
        for elem in listElements:
            if os.path.isdir( elem):
                child = DirectoryNode( self, elem)
            elif os.path.isfile( elem):
                child = FileLeaf( self, elem)
            self._listChildren.append( child)
        return self._listChildren
    def getName (self):
        return self._uPath

class DirectoryNode (TreeSystem.Node):
    def __init__ (self, parent, uPath):
        TreeSystem.Node.__init__( self, parent)
        self._uPath = uPath
    def computeChildren (self):
        self._listChildren = []
        listElements = os.listdir( self._uPath)
        for elem in listElements:
            if os.path.isdir( elem):
                child = DirectoryNode( self, elem)
            elif os.path.isfile( elem):
                child = FileLeaf( self, elem)
            self._listChildren += child
        return self._listChildren
    def getName (self):
        return self._uPath
    pass



    

    
    
    
    
   
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



        
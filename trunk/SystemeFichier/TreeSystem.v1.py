#!/usr/bin/python
# -*- coding: latin1 -*-
# - * - c o d i n g : iso-8859-1 - * - 


class TreeManager:
    "Tree Manager"
    def __init__ (self):
        pass
    pass

class Builder:
    "Builder of the tree system. It contains all actions"    
    def __init__ (self):
        self._listRoot = []
        pass
    def findRoots (self):
        """Find new root of this system
        Entry: None
        Return: List of new root
        """
        listNewRoot = []
        listNewRoot.append( u"C:\\")
        self._listRoot += listNewRoot
        return listNewRoot
    def getRoots (self):
        """
        Entry: None
        Return: List of new root
        """
        return self._listRoot
    pass

class TreeElement:
    def getName( self):
        """
        Entry: None
        Return: Unicode String
        """
        return u"TreeElement"
    
class Node (TreeElement):
    "A node of the tree"
    def __init__ (self, parent):
        self._parent = parent
        self._listChildren = []
    def computeChildren (self):
        """
        Entry: None
        Return: List of Children
        """
        #return self._listChildren
        return []
    def getParent (self):
        """Return the unique parent
        Entry: None
        Return: Root or Node Instance
        """
        return self._parent
    def getChildrenList (self):
        self.computeChildren()
        return self._listChildren

class Root (Node):
    "a root of the treesystem"
    def __init__ (self, treesystem):
        Node.__init__( self, None)
        self._treesystem = treesystem
    
class Leaf (TreeElement):
    "A leaf of the tree"
    def __init__ (self, parent):
        self._parent = parent
    def getParent (self):
        """Return the unique parent
        Entry: None
        Return: Root or Node Instance
        """
        return self._parent


if __name__ == '__main__':
    print "Begin"
    print "Test"
    print "End"

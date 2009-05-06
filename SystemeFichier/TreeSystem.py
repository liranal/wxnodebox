#!/usr/bin/python
# -*- coding: latin1 -*-
# - * - c o d i n g : iso-8859-1 - * - 

class Manager:
    "Tree Manager"
    def __init__ (self):
        self._cBuilder = self.computeBuilder()
    def computeBuilder(self):
        return Builder(self)
    def getBuilder (self):
        return self._cBuilder
    pass


class Builder:
    "Builder of the tree system. It contains all actions"    
    def __init__ (self):
        self._listRoots = []
        pass
    def findRoots (self):
        """Find new root of this system
        Entry: None
        Return: List of new root
        """
        listNewRoot = []
        #listNewRoot.append( u"C:\\")
        self._listRoot += listNewRoot
        return listNewRoot
    def getRoots (self):
        """
        Entry: None
        Return: List of new root
        """
        return self._listRoot
    pass


class Node:
    "A node of the tree"
    def __init__ (self, uIdName, parent):
        self._parent = parent
        self._uIdName = uIdName
        self._listChildren = None
    def computeChildren (self):
        """
        Entry: None
        Return: List of Children
        """
        self._listChildren = None
        return self._listChildren
    def computeAttribs (self):
        """
        Entry: None
        Return: Dictionnary of Attribs
        """
        self._dAttribs = {}
        return self._dAttribs
    def getParent (self):
        """Return the unique parent
        Entry: None
        Return: Root or Node Instance
        """
        return self._parent
    def getChildrenList (self):
        self.computeChildren()
        return self._listChildren
    def getIdName (self):
        return self._uIdName
    def getTypeName (self):
        return u"NODE"
    def getAttribs (self):
        self.computeAttribs()
        return self._dAttribs


if __name__ == '__main__':
    print "Begin"
    print "Test"
    print "End"

#!/usr/bin/env python3

class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

class PluginNode(Node):
    def __init__(self, name, uri, parent=None):
        super(PluginNode, self).__init__(name, parent)
        self.uri = uri

class CategoryNode(Node):
    def __init__(self, name, children=[], parent=None):
        super(CategoryNode, self).__init__(name, parent)
        self.children = children

    def __iter__(self):
        for child in self.children:
            yield child

    def __len__(self):
        return len(self.children)

    def add(self, node):
        node.parent = self
        self.children.append(node)

    def remove(self, node):
        """ I don't thinks this actually works """ 
        node.parent = None
        self.children.remove(node)

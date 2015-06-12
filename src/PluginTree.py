#!/usr/bin/env python3

class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

class PluginNode(Node):
    def __init__(self, name, uri, parent=None):
        super(PluginNode, self).__init__(name, parent)
        self.uri = uri

    def recursePluginTypes(self, category):
        types = [category.name]
        if category.parent:
            types += self.recursePluginTypes(category.parent)
        return types

    def types(self):
        if not self.parent:
            return "no parents wtf"
        return self.recursePluginTypes(self.parent)

class CategoryNode(Node):
    def __init__(self, name, children=[], parent=None):
        super(CategoryNode, self).__init__(name, parent)
        self.children = []
        self.children = list(map(self.add, children)) if children else []

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

    def recursePlugins(self, node):
        plugins = []
        if node:
            for child in node:
                if type(child) == PluginNode:
                    plugins.append(child)
                else:
                    plugins += self.recursePlugins(child)
        return plugins

    def getAllPlugins(self):
        return self.recursePlugins(self)

#!/usr/bin/env python3

class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

    def __str__(self):
        return self.name

    def _recurseTypes(self, category):
        types = [category.name]
        if category.parent:
            types += self._recurseTypes(category.parent)
        return types

    def types(self):
        if not self.parent:
            return [self] # this should only be root
        return self._recurseTypes(self.parent)

class PluginNode(Node):
    def __init__(self, name, uri, author, parent=None):
        super(PluginNode, self).__init__(name, parent)
        self.uri = uri
        self.author = author if author else ''
        #self.project = project

class CategoryNode(Node):
    def __init__(self, name, children=[], parent=None, uncategorized=False):
        super(CategoryNode, self).__init__(name, parent)
        self.children = []
        for child in children:
            self.add(child)
        #self.children = list(map(self.add, children)) if children else []
        self.uncategorized = uncategorized

    def __iter__(self):
        for child in self.children:
            yield child

    def __getitem__(self, i):
        return self.children[i]

    def __len__(self):
        return len(self.children)
    
    def add(self, node):
        if not self.uncategorized: node.parent = self
        self.children.append(node)

    def remove(self, node, keep_parent=True):
        if not keep_parent: node.parent = None
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


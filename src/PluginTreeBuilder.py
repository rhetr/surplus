#!/usr/bin/env python3

import sys
import lilv
from PyQt4 import QtGui, QtCore

from PluginTree import *

class PluginTreeBuilder:
    ''' this is a terrible class '''
    def __init__(self):
        world = lilv.World()
        world.load_all()
        all_plugins = list(world.get_all_plugins())
        self.root = None
        for a in all_plugins:
            if not a.get_class().get_parent_uri().is_uri():
                if not self.root:
                    self.root = CategoryNode(str(a.get_class().get_uri()))
                plugin = PluginNode(str(a.get_name()), str(a.get_uri()))
                self.root.add(plugin)
                all_plugins.remove(a)
        self.build_tree(all_plugins, self.root)

        uncat = CategoryNode('Uncategorized', uncategorized=True)
        i = 0
        while i < len(self.root):
            child = self.root[i]
            if type(child) == PluginNode:
                self.root.remove(child, True)
                uncat.add(child)
            else:
                i += 1

        self.root.add(uncat)

    def build_tree(self, plugin_list, root=None):
        unsorted_plugins = []
        if not root:
            pass
        else:
            for a in plugin_list:
                if str(a.get_class().get_uri()) == root.name:
                    plugin = PluginNode(str(a.get_name()), str(a.get_uri()))
                    root.add(plugin)
                elif str(a.get_class().get_parent_uri()) == root.name:
                    node = str(a.get_class().get_uri())
                    children = map(lambda y: y.name, filter(lambda x: type(x) == CategoryNode, root.children))
                    if node not in children:
                        plugin = PluginNode( str(a.get_name()), str(a.get_uri()))
                        category = CategoryNode(node)
                        category.add(plugin)
                        root.add(category)
                    else:
                        for i in range(len(root.children)):
                            if type(root.children[i] == CategoryNode) and root.children[i].name == node:
                                plugin = PluginNode(str(a.get_name()),str(a.get_uri()))
                                root.children[i].add(plugin)
                                break
                else:
                    unsorted_plugins.append(a)
            for child in root.children:
                if type(child) == CategoryNode:
                    self.build_tree(unsorted_plugins, child)


if __name__ == '__main__':
    from PluginList import *
    app = QtGui.QApplication(sys.argv)
    build = PluginTreeBuilder()
    root = build.root
    manipete = PluginList(root)
    manipete.setWindowFlags(QtCore.Qt.Dialog)
    manipete.show()
    sys.exit(app.exec_())

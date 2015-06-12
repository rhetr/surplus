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
                self.root.add(PluginNode(str(a.get_name()), str(a.get_uri())))
                all_plugins.remove(a)

        self.build_tree(all_plugins, self.root)
        newlist = []
        uncat = []
        for child in self.root:
            if type(child) == PluginNode:
                uncat.append(child)
            else:
                newlist.append(child)

        self.root.children = newlist
        self.root.add(CategoryNode('Uncategorized', uncat))

    def build_tree(self, plugin_list, root=None):
        unsorted_plugins = []
        if not root:
            pass
        else:
            for a in plugin_list:
                if str(a.get_class().get_uri()) == root.name:
                    root.add(PluginNode(str(a.get_name()), str(a.get_uri())))
                elif str(a.get_class().get_parent_uri()) == root.name:
                    node = str(a.get_class().get_uri())
                    children = map(lambda y: y.name, filter(lambda x: type(x) == CategoryNode, root.children))
                    if node not in children:
                        root.add( CategoryNode( node, [PluginNode( str(a.get_name()), str(a.get_uri()))]) ) 
                    else:
                        for i in range(len(root.children)):
                            if type(root.children[i] == CategoryNode) and root.children[i].name == node:
                                root.children[i].add(PluginNode(str(a.get_name()),str(a.get_uri())))
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

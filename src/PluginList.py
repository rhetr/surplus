#!/usr/bin/env python3

import os
from PyQt4 import QtGui, QtCore

from PluginTree import *
from BaseList import *


class PluginListItem(BaseListItem):
    def __init__(self, node):
        is_single = (type(node) == PluginNode)
        text = node.name if is_single else node.name.strip('<').strip('>').split('#')[-1]

        if not is_single and 'linuxdsp' in text: # why can't linuxdsp just use normal categories?
            text = os.path.basename(text)
        super(PluginListItem, self).__init__(text, is_single)
        self.node = node
        self.name = node.name

class PluginList(BaseList):
    def __init__(self, model, parent=None):
        super(PluginList, self).__init__(parent)
        self.model = model
        self.plugins = self.model.getAllPlugins()
        self.cwd = self.model
        self.updateList(self.model)

    def mimeData(self, item):
        mimeData = QtCore.QMimeData()
        mimeData.setUrls([QtCore.QUrl(item[0].node.uri)])
        return mimeData

    def _keyEvents(self, event):
        if event.key() == QtCore.Qt.Key_Return \
                or event.key() == QtCore.Qt.Key_Space:
            if not self.current_item.is_single:
                self.updateList(self.current_item.node)
            else:
                print(self.current_item.node.types())
        elif event.key() == QtCore.Qt.Key_Right \
                or event.key() == QtCore.Qt.Key_Semicolon:
            if not self.current_item.is_single:
                self.updateList(self.selectedItems()[0].node)

    def drawContents(self, curr_index=1):
        for entry in self.cwd_dirs:
            entry_item = PluginListItem(entry)
            self.addItem(entry_item)
        for entry in self.cwd_items:
            entry_item = PluginListItem(entry)
            self.addItem(entry_item)

        if not self.selectedItems():
            self.setCurrentRow(curr_index)
            self.current_item = self.item(curr_index)

    def getContents(self):
        '''sort into categories and plugins'''
        cat_list = []
        plug_list = []
        for entry in self.cwd:
            if type(entry) == CategoryNode:
                cat_list.append(entry)
            else:
                plug_list.append(entry)
        cat_list.sort(key=lambda x: x.name)
        plug_list.sort(key=lambda x: x.name)

        return cat_list, plug_list

    def updateList(self, dest):
        if dest == "..":
            if not self.cwd == self.model:
                self.cwd = self.cwd.parent
        else:
            self.cwd = dest
        self.clear()
        self.cwd_dirs, self.cwd_items = self.getContents()
        index = 1
        #parent = os.path.basename(os.getcwd()) \
        #        if os.path.abspath(dest) == os.path.dirname(os.getcwd()) \
        #        else None
        #index = self.cwd_dirs.index(parent) \
        #        if parent \
        #        else 1
        self.drawContents(index)

    def parseInput(self, text):
        results = list(
                filter(lambda x: 
            str(text.lower()) in x.name.lower() or
            any(str(text.lower()) in cat.lower() for cat in x.types()), self.plugins))
        self.showSearch(results)

    def showSearch(self, results):
        self.clear()
        self.cwd_dirs = []
        self.cwd_items = results
        self.drawContents()

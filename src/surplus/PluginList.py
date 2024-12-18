import os
from PyQt6.QtCore import Qt, QUrl, QMimeData

from .PluginTree import CategoryNode, PluginNode
from .BaseList import BaseListItem, BaseList


class PluginListItem(BaseListItem):
    def __init__(self, node):
        is_single = (type(node) is PluginNode)
        text = node.name if is_single else node.name.strip('<>').split('#')[-1]
        # why can't linuxdsp just use normal categories?
        if not is_single and 'linuxdsp' in text:
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
        if item[0].is_single:
            mimeData = QMimeData()
            mimeData.setUrls([QUrl(item[0].node.uri)])
            return mimeData

    # just a thought
    def mouseDoubleClickEvent(self, event):
        import subprocess
        if self.current_item.is_single:
            subprocess.Popen(
                    (
                        "jalv.gtk",
                        self.current_item.node.uri.strip('<>')
                        )
                    )
            print(self.current_item.node.parent)
        super(PluginList, self).mouseDoubleClickEvent(event)

    def _keyEvents(self, event):
        if event.key() == Qt.Key.Key_Return \
                or event.key() == Qt.Key.Key_Space:
            if not self.current_item.is_single:
                self.updateList(self.current_item.node)
            else:
                print(self.current_item.node.types())
        elif event.key() == Qt.Key.Key_Right \
                or event.key() == Qt.Key.Key_Semicolon:
            if not self.current_item.is_single:
                self.updateList(self.selectedItems()[0].node)

    def activatePressed(self, item):
        if self.select_flag:
            self.select_flag = False
        elif not self.current_item.is_single:
            self.updateList(self.current_item.node)

    def drawContents(self, curr_index=1):
        super(PluginList, self).drawContents(curr_index, PluginListItem)

    def getContents(self):
        '''sort into categories and plugins'''
        cat_list = []
        plug_list = []
        for entry in self.cwd:
            if type(entry) is CategoryNode:
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
        # parent = os.path.basename(os.getcwd()) \
        #         if os.path.abspath(dest) == os.path.dirname(os.getcwd()) \
        #         else None
        # index = self.cwd_dirs.index(parent) \
        #         if parent \
        #         else 1
        self.drawContents(index)

    def parseInput(self, text):
        results = list(
                filter(
                    lambda x:
                    str(text.lower()) in x.name.lower() or
                    any(
                        str(text.lower()) in cat.lower()
                        for cat in x.types()
                        ) or
                    str(text.lower()) in x.author.lower(),
                    self.plugins
                    )
                )
        self.showSearch(results)

    def showSearch(self, results):
        self.clear()
        self.cwd_dirs = []
        self.cwd_items = results
        self.drawContents()

#!/usr/bin/env python3

import os
from PyQt4 import QtGui, QtCore

class BaseListItem(QtGui.QListWidgetItem):
    def __init__(self, text, is_single):
        QtGui.QListWidgetItem.__init__(self)
        self.is_single = is_single
        self.text = text
        self.text += '/' if not is_single else ''
        self.setText(self.text)

class BaseList(QtGui.QListWidget):
    tab_pressed = QtCore.pyqtSignal()
    slash_pressed = QtCore.pyqtSignal()
    path_updated = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        QtGui.QListWidget.__init__(self, parent)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setDragDropMode(QtGui.QAbstractItemView.DragOnly)
        self.parent = parent

        self.current_item = None
        self.select_flag = False

        self.currentRowChanged.connect(self.itemSelected)

    def updateRecent(self, path):
        if path in config['Recent']: config['Recent'].remove(path)
        config['Recent'].append(path)
        if len(config['Recent']) > 50: config['Recent'].pop(0)

    def _keyEvents(self, event):
        '''reimplement'''
        pass

    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent:
            #if event.key() == QtCore.Qt.Key_Tab: #not working
            #    self.tab_pressed.emit()
            #    return 1
            if event.key() == QtCore.Qt.Key_Slash:
                self.slash_pressed.emit()
            elif event.key() == QtCore.Qt.Key_K:
                event = QtGui.QKeyEvent(event.type(), QtCore.Qt.Key_Down, QtCore.Qt.NoModifier)
            elif event.key() == QtCore.Qt.Key_L:
                event = QtGui.QKeyEvent(event.type(), QtCore.Qt.Key_Up, QtCore.Qt.NoModifier)
            elif event.key() == QtCore.Qt.Key_Left \
                    or event.key() == QtCore.Qt.Key_J:
                self.updateList('..')
            self._keyEvents(event)
        QtGui.QListWidget.keyPressEvent(self, event)

    def itemSelected(self, row):
        self.current_item = self.item(row)
        self.select_flag = True

    def updateList(self, dest):
        '''should be reimplemented'''
        pass

    def showSearch(self, results):
        '''should be reimplemented'''
        pass

    def drawContents(self, curr_index=1):
        for entry in self.cwd_dirs:
            entry_item = BaseListItem(entry, False)
            self.addItem(entry_item)
        for entry in self.cwd_items:
            entry_item = BaseListItem(entry, True)
            self.addItem(entry_item)

        if not self.selectedItems():
            self.setCurrentRow(curr_index)
            self.current_item = self.item(curr_index)

    def getContents(self):
        ''' should be reimplemented'''

    def activatePressed(self, item):
        if self.select_flag:
            self.select_flag = False
        elif self.current_item:
            self.updateList(self.current_item.text)

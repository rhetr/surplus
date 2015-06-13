#!/usr/bin/env python3

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
        self.itemClicked.connect(self.activatePressed)

    def updateRecent(self, path):
        if path in config['Recent']: config['Recent'].remove(path)
        config['Recent'].append(path)
        if len(config['Recent']) > 50: config['Recent'].pop(0)

    def event(self, event):
        if type(event) == QtGui.QKeyEvent \
                and event.key() == QtCore.Qt.Key_Tab:
                    self.tab_pressed.emit()
                    return True
        else:
            return super(BaseList, self).event(event)

    def _keyEvents(self, event):
        '''should be reimplemented'''
        pass

    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent:
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

    def parseInput(self, text):
        '''should be reimplemented'''
        pass

    def updateList(self, dest):
        '''should be reimplemented'''
        pass

    def showSearch(self, results):
        '''should be reimplemented'''
        pass

    def drawContents(self, curr_index=1, list_item_type=BaseListItem):
        assert issubclass(list_item_type, BaseListItem)
        for entry in self.cwd_dirs:
            entry_item = list_item_type(entry, False)
            self.addItem(entry_item)
        for entry in self.cwd_items:
            entry_item = list_item_type(entry, True)
            self.addItem(entry_item)

        if not self.selectedItems():
            self.setCurrentRow(curr_index)
            self.current_item = self.item(curr_index)

    def getContents(self):
        ''' should be reimplemented'''

    def activatePressed(self, item):
        ''' should be reimplemented '''

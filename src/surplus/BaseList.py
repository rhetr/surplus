from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QAbstractItemView, QListWidget, QListWidgetItem


class BaseListItem(QListWidgetItem):
    def __init__(self, text, is_single):
        QListWidgetItem.__init__(self)
        self.is_single = is_single
        self.text = text
        self.text += '/' if not is_single else ''
        self.setText(self.text)


class BaseList(QListWidget):
    tab_pressed = pyqtSignal()
    slash_pressed = pyqtSignal()
    path_updated = pyqtSignal(str)

    def __init__(self, parent=None):
        QListWidget.__init__(self, parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff) # noqa
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)
        self.parent = parent

        self.current_item = None
        self.select_flag = False

        self.currentRowChanged.connect(self.itemSelected)
        self.itemClicked.connect(self.activatePressed)

    def event(self, event):
        if type(event) is QKeyEvent and event.key() == Qt.Key.Key_Tab:
            self.tab_pressed.emit()
            return True
        else:
            return super(BaseList, self).event(event)

    def _keyEvents(self, event):
        '''should be reimplemented'''
        pass

    def keyPressEvent(self, event):
        if type(event) is QKeyEvent:
            if event.key() == Qt.Key.Key_Slash:
                self.slash_pressed.emit()
            elif event.key() == Qt.Key.Key_K:
                event = QKeyEvent(
                        event.type(),
                        Qt.Key.Key_Down, Qt.KeyboardMofifier.NoModifier
                        )
            elif event.key() == Qt.Key.Key_L:
                event = QKeyEvent(
                        event.type(),
                        Qt.Key.Key_Up, Qt.KeyboardModifier.NoModifier
                        )
            elif event.key() == Qt.Key.Key_Left \
                    or event.key() == Qt.Key.Key_J:
                self.updateList('..')
            self._keyEvents(event)
        QListWidget.keyPressEvent(self, event)

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

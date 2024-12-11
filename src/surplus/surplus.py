import sys
import os
import yaml
import subprocess
from PyQt6.QtCore import QEvent, Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFontMetrics, QKeyEvent
from PyQt6.QtWidgets import QComboBox, QWidget, QStackedWidget, QTabBar, \
        QScrollBar, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QCheckBox

# from PluginTreeBuilder import *
# from PluginList import *
from .FileList import FileList
from .WaveViewer import WaveViewer

from .config import config


def handler(*args):
    '''saves the config and kills play before exiting'''
    subprocess.call(['pkill', 'play'])
    print('caught exit signal')
    if not config:
        print('error, config not saved')
    else:
        config.save()
    print('exiting')
    sys.exit(0)


class InputWidget(QComboBox):
    path_updated = pyqtSignal(str)
    tab_pressed = pyqtSignal()
    esc_pressed = pyqtSignal()

    def __init__(self):
        QComboBox.__init__(self)
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.addItems(config.settings['Places'])
        self.addItem('Recent')
        self.resize()
        self.activated.connect(self.updatePath)

    def updatePath(self, index):
        self.path_updated.emit(self.currentText())

    def event(self, event):
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Tab:
                self.tab_pressed.emit()
                return True
            elif event.key() == Qt.Key.Key_Escape:
                self.setEditText(self.prev_text)
                self.esc_pressed.emit()
                return True
        return QComboBox.event(self, event)

    def keyPressEvent(self, event):
        QComboBox.keyPressEvent(self, event)
        if event.key() == Qt.Key.Key_Return:
            if os.path.isdir(self.currentText()):
                self.path_updated.emit(self.currentText())
            self.esc_pressed.emit()

    def focusInEvent(self, event):
        self.prev_text = self.currentText()
        QComboBox.focusInEvent(self, event)

    def resize(self):
        font = QFontMetrics(self.font())
        max_width = 0
        for place in config.settings['Places']:
            width = 0
            for p in place:
                width += font.boundingRect(p).width()
            if width > max_width:
                max_width = width
        max_width += 40
        self.view().setMinimumWidth(max_width)


class Surplus(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        # self.setAttribute(Qt.WA_AcceptTouchEvents)
        # self.setWindowFlags(Qt.Dialog)
        self.setWindowTitle('Surplus')

        self._initWidgets()
        self._initFilesTab()
        self._initPluginsTab()
        self._initMainLayout()

        self.addTab(self.tab1, "browser")
        # self.addTab(self.tab2, "plugins")

        self._initConnections()
        self.files.setFocus()
        self.inputBox.editTextChanged.connect(self.parseInput)

    def _initWidgets(self):
        self.widgetStack = QStackedWidget()

        self.tabBar = QTabBar()
        self.tabBar.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.tabBar.currentChanged.connect(self.switchTabs)
        self.tabBar.setShape(QTabBar.Shape.RoundedWest)
        self.tabBar.updateGeometry()

        self.scrollBar = QScrollBar()
        self.scrollBar.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.scrollBar.rangeChanged.connect(self.scrollHide)
        self.blank = QWidget(parent=self)
        self.blank.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.blank.hide()

        self.placesButton = QPushButton("+")
        self.placesButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.placesButton.sizeHint = self.placesButtonSizeHint

        self.tabLayoutBox = QVBoxLayout()
        self.tabLayoutBox.setContentsMargins(0, 0, 0, 0)
        self.tabLayoutBox.setSpacing(0)
        # self.tabLayoutBox.setMargin(0) # doesn't appear available in PyQt6?
        self.tabLayoutBox.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.tabLayoutBox.addWidget(self.placesButton)
        self.tabLayoutBox.addWidget(self.tabBar)
        self.tabLayoutBox.addWidget(self.scrollBar)
        self.tabLayoutBox.addWidget(self.blank)

    def _initMainLayout(self):
        mainHBox = QHBoxLayout()
        mainHBox.setContentsMargins(0, 0, 0, 0)
        # mainHBox.setMargin(0)
        mainHBox.setSpacing(0)
        mainHBox.addLayout(self.tabLayoutBox)
        mainHBox.addWidget(self.widgetStack)

        mainVBox = QVBoxLayout()
        mainVBox.addWidget(self.inputBox)
        mainVBox.addLayout(mainHBox)
        self.setLayout(mainVBox)

    def _initFilesTab(self):
        self.tab1 = QWidget()
        self.inputBox = InputWidget()
        self.inputBox.setFrame(QFrame.Shape.NoFrame)
        self.files = FileList(config.settings['Default Folder'])
        self.files.setVerticalScrollBar(self.scrollBar)
        self.tab1.parseInput = self.files.parseInput

        self.playCheck = QCheckBox()
        self.waveRect = WaveViewer()
        self.waveRect.setMaximumHeight(20)
        self.waveRect.setFrameShape(QFrame.Shape.NoFrame)
        hBox = QHBoxLayout()
        hBox.addWidget(self.playCheck)
        hBox.addWidget(self.waveRect)

        tab1Layout = QVBoxLayout()
        tab1Layout.setContentsMargins(0, 0, 0, 0)
        tab1Layout.setSpacing(0)
        # tab1Layout.setMargin(0)
        tab1Layout.addWidget(self.files)
        tab1Layout.addLayout(hBox)
        self.tab1.setLayout(tab1Layout)

    def _initPluginsTab(self):
        pass
        # build = PluginTreeBuilder()
        # self.tab2 = PluginList(build.root)
        # self.tab2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def _initConnections(self):
        self.files.tab_pressed.connect(self.switchTabs)
        self.files.slash_pressed.connect(self.focusPath)
        self.inputBox.tab_pressed.connect(self.switchTabs)
        self.inputBox.esc_pressed.connect(self.focusList)

        self.files.path_updated.connect(self.updatePath)
        self.inputBox.path_updated.connect(self.updateList)
        self.files.path_updated.emit(config.settings['Default Folder'])

        self.files.sample_selected.connect(self.waveRect.loadFile)
        self.playCheck.stateChanged.connect(self.files.enablePlayback)

        # self.tab2.tab_pressed.connect(self.switchTabs)
        # self.tab2.slash_pressed.connect(self.focusPath)

        if config.settings['Play']:
            self.playCheck.setChecked(True)
            # self.playCheck.stateChanged.emit()  # Qt.CheckState.Checked)
        else:
            self.playCheck.setChecked(False)
            # self.playCheck.stateChanged.emit()  # Qt.CheckState.Unchecked)

        self.placesButton.clicked.connect(self.modifyPlaces)

    def parseInput(self, text):
        self.widgetStack.currentWidget().parseInput(text)

    def updateButton(self, text):
        if (
                os.path.realpath(os.path.abspath(text)) ==
                os.path.realpath(
                    os.path.abspath(config.settings['Default Folder'])
                    ) or
                text == 'Recent'
                ):
            self.placesButton.setEnabled(False)
            return
        self.placesButton.setEnabled(True)
        path = os.path.realpath(os.path.abspath(text))
        places = (os.path.realpath(sym) for sym in config.settings['Places'])
        text = '-' if path in places else '+'
        self.placesButton.setText(text)

    def modifyPlaces(self):
        path = os.getcwd()
        removed = config.modifyPlaces(path)
        if removed:
            self.inputBox.removeItem(config.getPlacesIndex(path))
            self.placesButton.setText('+')
        else:
            self.inputBox.insertItem(config.getPlacesIndex(path), path)
            self.placesButton.setText('-')
        self.inputBox.resize()

    def scrollHide(self, a, b):
        if a == b and not self.scrollBar.isHidden():
            self.scrollBar.hide()
            self.blank.show()
        elif self.scrollBar.isHidden():
            self.scrollBar.show()
            self.blank.hide()

    def addTab(self, widget, name):
        self.widgetStack.addWidget(widget)
        self.tabBar.addTab(name)

    def sizeHint(self):
        return QSize(220, 500)

    def placesButtonSizeHint(self):
        return QSize(20, 20)

    def event(self, event):
        if type(event) is QKeyEvent \
                and event.key() == Qt.Key.Key_Tab:
            return True
        else:
            return super(Surplus, self).event(event)

    def switchTabs(self, index=None):
        if not index:
            index = (self.widgetStack.currentIndex()+1) % self.widgetStack.count() # noqa
        self.tabBar.setCurrentIndex(index)
        self.widgetStack.setCurrentIndex(index)
        # have to move scrollbar too

    def focusList(self):
        self.widgetStack.currentWidget().setFocus(Qt.ShortcutFocusReason) # noqa

    def focusPath(self):
        self.inputBox.setFocus(Qt.ShortcutFocusReason)

    def updatePath(self, text):
        self.inputBox.setEditText(text)
        self.updateButton(str(text).strip())

    def updateList(self, text):
        self.files.updateList(str(text).strip())
        self.updateButton(str(text).strip())

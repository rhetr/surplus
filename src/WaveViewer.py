#!/usr/bin/env python3

from PyQt4 import QtGui, QtCore

from peaks import *
from config import *

class WaveViewer(QtGui.QGraphicsView):
    def __init__(self):
        QtGui.QGraphicsView.__init__(self)
        self.setBackgroundBrush(QtGui.QColor(34, 34, 34))
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.thread = None
        self.scene = QtGui.QGraphicsScene(self)
        self.rect = QtGui.QGraphicsRectItem(0, 0, 100, 20)
        self.rect.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0)))
        self.scene.addItem(self.rect)
        self.setScene(self.scene)
        self.setAlignment(QtCore.Qt.AlignLeft)

        self.waveform = None

    def resizeEvent(self, event):
        self.fitInView(self.rect)
        QtGui.QGraphicsView.resizeEvent(self, event)

    def mil(self, length):
        return length.hour*3.6e6 + \
            length.minute * 6e4 + \
            length.second * 1000 + \
            length.microsecond * .001

    def loadFile(self, a_file):
        if config['Show Waveform']:
            if self.thread:
                self.thread.active = False
                self.thread.quit()
                self.thread.wait()
            if self.waveform:
                self.scene.clear()
                self.waveform = None
            if a_file:
                waveform = WavePathItem()
                self.thread = WaveThread(a_file, waveform)
                self.thread.finished.connect(self.loadWave)
                self.thread.start()

    def loadWave(self, waveform):
        self.scene.clear()
        wave_pen = QtGui.QPen(QtGui.QColor(70, 122, 100, 150))
        waveform.setPen(wave_pen)
        self.scene.addItem(waveform)
        self.waveform = waveform

    def animate(self):
        self.tl.start()

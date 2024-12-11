
from .peaks import WaveThread, WavePathItem
from .config import config

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem


class WaveViewer(QGraphicsView):
    def __init__(self):
        QGraphicsView.__init__(self)
        self.setBackgroundBrush(QColor(34, 34, 34))
        self.setVerticalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOff
                )
        self.setHorizontalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOff
                )

        self.thread = None
        self.scene = QGraphicsScene(self)
        self.rect = QGraphicsRectItem(0, 0, 100, 20)
        self.rect.setPen(QPen(QColor(0, 0, 0, 0)))
        self.scene.addItem(self.rect)
        self.setScene(self.scene)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.waveform = None

    def resizeEvent(self, event):
        self.fitInView(self.rect)
        QGraphicsView.resizeEvent(self, event)

    def mil(self, length):
        return length.hour*3.6e6 + \
            length.minute * 6e4 + \
            length.second * 1000 + \
            length.microsecond * .001

    def loadFile(self, a_file):
        if config.settings['Show Waveform']:
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
        wave_pen = QPen(QColor(70, 122, 100, 150))
        waveform.setPen(wave_pen)
        self.scene.addItem(waveform)
        self.waveform = waveform

    def animate(self):
        self.tl.start()

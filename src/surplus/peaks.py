import subprocess as sp
import numpy as np
import sys
import os
import pickle

from PyQt6.QtGui import QPainterPath
from PyQt6.QtCore import QThread, QPointF, pyqtSignal
from PyQt6.QtWidgets import QGraphicsPathItem


class WaveThread(QThread):
    finished = pyqtSignal(object)

    def __init__(self, audio_file, wave_item):
        QThread.__init__(self)
        self.audio_file = audio_file
        self.wave_item = wave_item

    def run(self):
        self.active = True
        pf = self.audio_file + '.pf'
        try:
            wave = pickle.load(open(pf, 'rb')) \
                    if os.path.exists(pf) \
                    else self.makeWave(self.audio_file)
        except UnicodeDecodeError:
            wave = self.makeWave(self.audio_file)
        self.wave_item.loadWave(wave)
        if self.active:
            self.finished.emit(self.wave_item)

    def makeWave(self, audio_file):
        height = 10
        width = 120
        command = [
                FFMPEG_BIN,
                '-i', audio_file,
                '-f', 's16le',
                '-c:a', 'pcm_s16le',
                '-ar', '44100',
                '-ac', '1',
                '-'
                ]
        ppipe = sp.Popen(
                command,
                stdout=sp.PIPE,
                stderr=open(os.devnull, 'wb'),
                bufsize=10**8
                )
        raw_audio = ppipe.communicate()[0]
        audio_array = np.fromstring(raw_audio, dtype="int16").astype(float)
        scale = 10**(int(np.log10(audio_array.size))/2)
        if audio_array.size > 1e6:
            audio_array = audio_array[1::scale]
        audio_array *= (height/float(np.amax(audio_array)))
        audio_array += height
        size = audio_array.size
        # print(size)
        t = np.linspace(0, width, size)
        wave = np.array((audio_array, t))
        pickle.dump(wave, open(audio_file + '.pf', 'wb'), protocol=2)
        # print('finished making {}'.format(audio_file))
        return wave


class WavePathItem(QGraphicsPathItem):
    def __init__(self, wave=None):
        QGraphicsPathItem.__init__(self)
        if wave:
            self.loadWave(wave)

    def loadWave(self, wave):
        first = QPointF(wave[1, 0], wave[0, 0])
        path = QPainterPath(first)
        for i in range(1, wave.shape[1]):
            path.lineTo(wave[1, i], wave[0, i])
        self.setPath(path)


# needs ffmpeg
def which(program):
    import os

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


if which('ffmpeg'):
    FFMPEG_BIN = 'ffmpeg'
else:
    print('ffmpeg not installed')
    sys.exit()

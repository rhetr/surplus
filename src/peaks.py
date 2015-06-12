#!/usr/bin/env python3
#filename: peaks.py

import subprocess as sp
import numpy as np
import sys
import os
import pickle
from PyQt4 import QtGui, QtCore
import datetime

class Test(QtGui.QGraphicsView):
    def __init__(self):
        QtGui.QGraphicsView.__init__(self)
        self.scene = QtGui.QGraphicsScene()
        self.setScene(self.scene)

        audio_file = '/media/Data/audio/sounds/drum sounds/[99Sounds] 99 Drum Samples/Samples/kick-slapback.wav'
        audio_file = '/media/Data/audio/cats/Portamento Electro.m4a'
        print(os.path.exists(audio_file))
        thread = waveThread(audio_file)
        thread.finished.connect(self.load)
        thread.start()

    def load(self, wave):
        path = waveForm(wave)
        self.scene.addItem(path)


class waveThread(QtCore.QThread):
    finished = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, audio_file):
        QtCore.QThread.__init__(self)
        self.audio_file = audio_file

    def __del__(self):
        self.wait()

    def run(self):
        pf = self.audio_file + '.pf'
        #self.wave = pickle.load(open(pf, 'rb')) if os.path.exists(pf) else self.makeWave(self.audio_file)
        self.wave = self.makeWave(self.audio_file)
        self.finished.emit(self.wave)

    def makeWave(self, audio_file):
        height = 10
        width = 120
        command = [ FFMPEG_BIN,
                '-i', audio_file,
                '-f', 's16le',
                '-c:a', 'pcm_s16le',
                '-ar', '44100', 
                '-ac', '1', 
                '-']
        ppipe = sp.Popen(command, stdout=sp.PIPE, stderr=open(os.devnull,'wb'), bufsize=10**8)
        raw_audio = ppipe.communicate()[0]
        audio_array = np.fromstring(raw_audio, dtype="int16").astype(np.float)
        scale = 10**(int(np.log10(audio_array.size))/2)
        if audio_array.size > 1e6:
            audio_array = audio_array[1::scale]
        audio_array *= (height/float(np.amax(audio_array)))
        audio_array += height
        size = audio_array.size
        print(size)
        t = np.linspace(0,width,size)
        wave = np.array((audio_array,t))
        pickle.dump(wave, open(audio_file + '.pf', 'wb'), protocol=2)
        print('finished making wave')
        return wave


class waveForm(QtGui.QGraphicsPathItem):
    def __init__(self, wave=None):
        QtGui.QGraphicsPathItem.__init__(self)
        first = QtCore.QPointF(wave[1,0],wave[0,0])
        s = datetime.datetime.now()
        #x = [(wave[1,i], wave[0,i]) for i in range(1, wave.shape[1])]
        path = QtGui.QPainterPath(first)
        for i in range(1, wave.shape[1]):
            path.lineTo(wave[1,i],wave[0,i])
        x = datetime.datetime.now() - s
        print((x.seconds, x.microseconds))

        self.setPath(path)


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
elif which('avconv'):
    FFMPEG_BIN = 'avconv'
else:
    print('ffmpeg or avconv not installed')
    sys.exit()


if __name__ == '__main__':

    example = QtGui.QApplication(sys.argv)
    test2 = Test()
    test2.show()
    sys.exit(example.exec_())

#!/usr/bin/env python
#filename: peaks.py

import subprocess as sp
import numpy as np
import sys
import os
import cPickle as pickle
from PyQt4 import QtGui, QtCore

class Test(QtGui.QGraphicsView):
    def __init__(self):
        QtGui.QGraphicsView.__init__(self)
        self.scene = QtGui.QGraphicsScene()
        self.setScene(self.scene)

        audio_file = '/media/Data/audio/sounds/drum sounds/[99Sounds] 99 Drum Samples/Samples/kick-slapback.wav'
        path = waveForm(audio_file)

        self.scene.addItem(path)


class waveForm(QtGui.QGraphicsPathItem):
    def __init__(self, audio_file=None):
        QtGui.QGraphicsPathItem.__init__(self)
        if audio_file:

            pf = audio_file + '.pf'
            wave = pickle.load(open(pf, 'rb')) if os.path.exists(pf) else self.makeWave(audio_file)
            first = QtCore.QPointF(wave[1,0],wave[0,0])
            path = QtGui.QPainterPath(first)
            for i in range(1, wave.shape[1]):
                path.lineTo(QtCore.QPointF(wave[1,i],wave[0,i]))

            self.setPath(path)

    def makeWave(self, audio_file):
        print 'making waves'
        height = 10
        width = 200
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
        audio_array *= (height/float(np.amax(audio_array)))
        audio_array += height
        size = audio_array.size
        t = np.linspace(0,width,size)
        wave = np.array((audio_array,t))
        pickle.dump(wave, open(audio_file + '.pf', 'wb'), protocol=2)
        return wave

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
    print 'ffmpeg or avconv not installed'
    sys.exit()


if __name__ == '__main__':

    example = QtGui.QApplication(sys.argv)
    test2 = Test()
    test2.show()
    sys.exit(example.exec_())


#!/usr/bin/env python3

import os
import subprocess
import signal
from PyQt4 import QtGui, QtCore

from BaseList import *
from peaks import *
from config import *

exts = ['wav', 'mp3', 'ogg', 'flac', 'm4a']
audio_only = '|'.join(map(lambda ext: '\.{}'.format(ext), exts))

def play(a_file):
    return subprocess.Popen(['play', '-q', a_file],
                            stdout=subprocess.PIPE,
                            preexec_fn=os.setsid)

class FileListItem(BaseListItem):
    def __init__(self, text, is_single=True):
        super(FileListItem, self).__init__(text, is_single)
        self.playing = None

    def playSample(self):
        if self.playing:
            os.killpg(self.playing.pid, signal.SIGTERM)
        self.playing = play(self.text)

class FileList(BaseList):
    sample_playing = QtCore.pyqtSignal(bool)
    sample_selected = QtCore.pyqtSignal(str)

    def __init__(self, path, parent=None):
        super(FileList, self).__init__(parent)
        self.playback_enabled = False

        self.updateList(path)

    def mimeData(self, item):
        path = os.path.abspath(str(item[0].text))
        if os.path.isfile(path):
            mimeData = QtCore.QMimeData()
            mimeData.setUrls([QtCore.QUrl.fromLocalFile(path)])
            self.updateRecent(path)
            return mimeData

    def _keyEvents(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.updateList(os.getcwd())
        elif event.key() == QtCore.Qt.Key_Delete:
            if os.path.abspath(self.current_item.text) in config['Recent']:
                config['Recent'].remove(os.path.abspath(self.current_item.text))
                self.updateList('Recent')
        elif event.key() == QtCore.Qt.Key_Return \
                or event.key() == QtCore.Qt.Key_Space:
            if self.current_item.is_single: self.current_item.playSample()
            else: self.updateList(self.current_item.text)
        elif event.key() == QtCore.Qt.Key_Right \
                or event.key() == QtCore.Qt.Key_Semicolon:
            if not self.current_item.is_single:
                self.updateList(self.selectedItems()[0].text)

    def activatePressed(self, item):
        if self.select_flag:
            self.select_flag = False
        elif self.current_item:
            if self.current_item.is_single and self.playback_enabled: self.current_item.playSample()
            else: self.updateList(self.current_item.text)


    def _isAudio(self, a_file):
        if os.path.splitext(a_file)[1].lower()[1:] in exts:
            return True
        return False

    def getContents(self):
        entries = os.listdir(os.getcwd())
        entries = [i for i in entries if not i.startswith('.')]
        dir_list = ['..']
        file_list = []
        for entry in entries:
            if os.path.isdir(entry):
                dir_list.append(entry)
            elif os.path.isfile(entry):
                if self._isAudio(entry):
                    file_list.append(entry)
        dir_list.sort(key=str.lower)
        file_list.sort(key=str.lower)

        return dir_list, file_list

    def itemSelected(self, row):
        super(FileList, self).itemSelected(row)
        if self.current_item and self.current_item.is_single:
            self.sample_selected.emit(self.current_item.text)
            if self.playback_enabled: self.current_item.playSample()

    def updateList(self, dest):
        self.clear()
        if dest == "Recent":
            self.cwd_dirs = ['..']
            self.cwd_items = config['Recent'][::-1]
            self.drawContents()
            self.path_updated.emit('Recent')
        else:
            prev_folder = os.path.basename(os.getcwd()) \
                    if os.path.abspath(dest) == os.path.dirname(os.getcwd()) \
                    else None
            os.chdir(dest)
            self.cwd_dirs, self.cwd_items = self.getContents()
            index = self.cwd_dirs.index(prev_folder) \
                    if prev_folder \
                    else 1
            self.drawContents(index)
            self.path_updated.emit(os.getcwd())

    def drawContents(self, curr_index=1):
        super(FileList, self).drawContents(curr_index, FileListItem)

    def enablePlayback(self, state):
        config['Play'] = state
        self.playback_enabled = state

    def parseInput(self, text):
        if len(text) > 0:
            text = str(text)
            if not str(text)[0] == "/": self.searchText(text)

    def searchText(self, text):
        '''uses find, grep and awk to search within the current working directory'''
        ignore_case = ' && '.join(map(
            lambda word: '/{}/'.format(
                ''.join(map(
                    lambda z: '[{}{}]'.format(
                        z.lower(), z.upper()),
                    (c for c in word)))),
                text.split()))

        cmd = "find '{}' | grep -vE '\.asd|\.pf' | grep -E '{}'| awk {}".format(
                os.getcwd(),
                audio_only,
                ignore_case)

        results = subprocess.check_output(cmd, shell=True).decode('utf-8').split('\n')[:100]
        self.showSearch(results)

    def showSearch(self, results):
        self.clear()
        self.cwd_dirs = ['..', os.getcwd()]
        self.cwd_items = map(
                lambda s: './{}'.format(s[len(os.getcwd())+1:]),
                filter(None, results[:100])
                )
        self.drawContents()


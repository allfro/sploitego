#!/usr/bin/env python
from Tkinter import Tk
import sys
from PySide.QtGui import QMainWindow, QApplication, QTextCursor
from PySide.QtCore import SIGNAL

from metasploit.msfconsole import MsfRpcConsole
from metasploit.msfrpc import MsfRpcClient
from ui.shell import Ui_MainWindow

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = [ 'Nadeem Douba' ]

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


class MsfShellWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, msfrpc, **kwargs):
        QMainWindow.__init__(self, kwargs.pop('parent', None))
        self.setupUi(self)
        self.setWindowTitle('Metasploit Console')
        self._initCommandLine()
        self._msfInit(msfrpc, **kwargs)

    def _msfInit(self, msfrpc, **kwargs):
        self.connect(self.outputTextBrowser, SIGNAL('textChanged(QString)'), self._getOutput)
        self.prompt = 'msf >'
        self.c = MsfRpcConsole(msfrpc, sessionid=kwargs.get('sessionid'),cb=self._emitSignal)
        if 'command' in kwargs:
            self.commanderLineEdit.setText(kwargs['command'])
            self.commanderLineEdit.emit(SIGNAL('returnPressed()'))

    def _emitSignal(self, d):
        self.outputTextBrowser.emit(SIGNAL('textChanged(QString)'), repr(d))

    def _initCommandLine(self):
        self.connect(self.commanderLineEdit, SIGNAL('returnPressed()'), self._sendCommand)
        self.vb = self.outputTextBrowser.verticalScrollBar()

    def _sendCommand(self):
        c = self.outputTextBrowser.textCursor()
        c.movePosition(QTextCursor.End)
        self.outputTextBrowser.setTextCursor(c)
        cmd = str(self.commanderLineEdit.text())
        if cmd == 'exit':
            self.close()
            return
        self.c.execute(cmd)
        self.outputTextBrowser.insertHtml('%s<br>' % cmd)
        self.commanderLineEdit.clear()
        self.vb.setValue(self.vb.maximum())

    def _getOutput(self, d):
        d = eval(str(d))
        self.prompt = d['prompt']
        self.outputTextBrowser.insertPlainText('\n%s\n' % d['data'])
        self.outputTextBrowser.insertHtml('<font color="red"><b>%s</b></font><font color="black">&nbsp;</font>' % self.prompt)
        self.vb.setValue(self.vb.maximum())

    def closeEvent(self, event):
        self.c.__del__()
        QMainWindow.close(self)


def launch(msfrpc, **kwargs):
    app = QApplication(sys.argv)
    MsfShellWindow(msfrpc, **kwargs).show()
    if sys.platform == 'darwin':
        from subprocess import Popen
        Popen(['osascript', '-e', 'tell application "Python" to activate'])
    app.exec_()
#!/usr/bin/env python

from PyQt4.QtGui import QMainWindow
from PyQt4.QtCore import SIGNAL

from sploitego.metasploit.msfconsole import MsfRpcConsole
from sploitego.metasploit.msfrpc import MsfRpcClient
from ui.shell import Ui_MainWindow

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


class MsfShellWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, password, **kwargs):
        QMainWindow.__init__(self, kwargs.pop('parent', None))
        self.setWindowTitle('Metasploit Console')
        self.setupUi(self)
        self._initCommandLine()
        self._msfInit(password, **kwargs)

    def _msfInit(self, password, **kwargs):
        self.connect(self.outputTextBrowser, SIGNAL('textChanged(QString)'), self._getOutput)
        self.prompt = 'msf >'
        self.c = MsfRpcConsole(MsfRpcClient(password, **kwargs), cb=self._emitSignal)
        if kwargs['command']:
            self.commanderLineEdit.setText(kwargs['command'])
            self._sendCommand()

    def _emitSignal(self, d):
        self.outputTextBrowser.emit(SIGNAL('textChanged(QString)'), repr(d))

    def _initCommandLine(self):
        self.connect(self.commanderLineEdit, SIGNAL('returnPressed()'), self._sendCommand)
        self.vb = self.outputTextBrowser.verticalScrollBar()

    def _sendCommand(self):
        t = self.commanderLineEdit.text()
        self.c.execute(str(t))
        self.outputTextBrowser.insertHtml('%s<br>' % t)
        self.commanderLineEdit.clear()
        self.vb.setValue(self.vb.maximum())

    def _getOutput(self, d):
        d = eval(str(d))
        self.prompt = d['prompt']
        self.outputTextBrowser.insertPlainText('%s\n' % d['data'])
        self.outputTextBrowser.insertHtml('<font color="red"><b>%s</b></font> ' % self.prompt)
        self.vb.setValue(self.vb.maximum())
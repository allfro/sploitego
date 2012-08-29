#!/usr/bin/env python

from threading import Timer, Lock

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'MsfRpcConsole'
]


class MsfRpcConsole(object):

    def __init__(self, rpc, cb=None):
        """
        Emulates the msfconsole in msf except over RPC.

        Mandatory Arguments:
        - rpc : an msfrpc client object

        Optional Arguments:
        - cb : a callback function that gets called when data is received from the console.
        """
        self.console = rpc.consoles.console()
        self.callback = cb
        self.lock = Lock()
        self.running = True
        self.prompt = ''
        self._poller()

    def _poller(self):
        self.lock.acquire()
        if not self.running:
            return
        d = self.console.read()
        self.lock.release()
        if d['data'] or self.prompt != d['prompt']:
            self.prompt = d['prompt']
            if self.callback is not None:
                self.callback(d)
            else:
                print d['data']
        Timer(0.5, self._poller).start()

    def execute(self, command):
        """
        Execute a command on the console.

        Mandatory Arguments:
        - command : the command to execute
        """
        if not command.endswith('\n'):
            command += '\n'
        self.lock.acquire()
        self.console.write(command)
        self.lock.release()

    def __del__(self):
        self.lock.acquire()
        self.console.destroy()
        self.running = False
        self.lock.release()

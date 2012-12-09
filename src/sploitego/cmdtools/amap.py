#!/usr/bin/env python

from os import path, environ, pathsep
from subprocess import Popen, PIPE
from re import findall


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'AmapReportParser',
    'AmapScanner'
]


class AmapReportParser(object):

    def __init__(self, input):
        self.output = input

    @property
    def banners(self):
        return findall('Protocol on (.+?) matches (.+?) - banner: (.+)', self.output)


class AmapScanner(object):

    output = ''
    cmd = ''

    def getversion(self):
        for p in environ['PATH'].split(pathsep):
            program = path.join(p, 'amap')
            if path.exists(program):
                self.program = program
                self.version = self.run([])
                return True
        return False

    def run(self, args):
        self.cmd = ' '.join([self.program]+args)
        self._pipe = Popen([self.program]+args, stdin=PIPE, stdout=PIPE)
        r, e = self._pipe.communicate()
        self.output = r

        return r.strip('\n')

    def __init__(self):
        if not self.getversion():
            raise OSError('Could not find amap, check your OS path')

    def scan(self, args, sendto=AmapReportParser):
        r = self.run(args)
        if callable(sendto):
            return sendto(r)
        return sendto.write(r)

    def terminate(self):
        self._pipe.terminate()

    def __del__(self):
        try:
            self.terminate()
        except OSError:
            pass
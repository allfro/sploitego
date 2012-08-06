#!/usr/bin/env python


from os import path, name, sep, stat
from tempfile import gettempdir
from sys import maxint
from time import time

if name == 'nt':
    from win32con import LOCKFILE_EXCLUSIVE_LOCK as LOCK_EX, LOCKFILE_FAIL_IMMEDIATELY as LOCK_NB
    from win32file import _get_osfhandle, LockFileEx, UnlockFileEx
    from pywintypes import OVERLAPPED, error as WinIOError
else:
    from fcntl import flock, LOCK_EX, LOCK_NB, LOCK_SH, LOCK_UN

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'cookie',
    'flock',
    'fsemaphore',
    'fmutex',
    'ufile',
    'age'
]


if name == 'nt':
    LOCK_SH = 0
    LOCK_UN = 0
    __overlapped = OVERLAPPED()

    def flock(file, flags):
        hfile = _get_osfhandle(file.fileno())
        try:
            if flags & LOCK_UN:
                UnlockFileEx(hfile, 0, -0x10000, __overlapped)
            else:
                LockFileEx(hfile, flags, 0, -0x10000, __overlapped)
        except WinIOError, exc:
            raise IOError('[Errno %d] %s' % (exc[0], exc[2]))


def cookie(name):
    return sep.join([gettempdir(), name])


class fsemaphore(file):

    def __init__(self, name, mode='rb', buffering=-1):
        super(fsemaphore, self).__init__(name, mode, buffering)

    def lockex(self, nb=False):
        flags = LOCK_EX
        if nb:
            flags |= LOCK_NB
        flock(self, flags)

    def locksh(self, nb=False):
        flags = LOCK_SH
        if nb:
            flags |= LOCK_NB
        flock(self, flags)

    def unlock(self, nb=False):
        flags = LOCK_UN
        if nb:
            flags |= LOCK_NB
        flock(self, flags)


class fmutex(fsemaphore):

    def __init__(self, name):
        super(fmutex, self).__init__(cookie(name), 'wb')
        self.lockex()

    def __del__(self):
        self.unlock()


class ufile(file):

    def __init__(self, name):
        if path.exists(name):
            p, n = path.split(name)
            n, e = path.splitext(n)

            for i in xrange(2, maxint):
                name = path.join(p, '%s(%d)%s') % (n, i, e)
                if not path.exists(name):
                    break
        super(ufile, self).__init__(name, mode='wb')


def age(path):
    return time() - stat(path).st_mtime
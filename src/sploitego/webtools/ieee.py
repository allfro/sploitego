#!/usr/bin/env python

from os import path
from re import split

from canari.utils.fs import cookie, age, fsemaphore
from canari.utils.wordlist import wordlist
from canari.config import config


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'ouis'
]


def updatelist(filename):

    f = fsemaphore(filename, 'wb')
    f.lockex()
    ouis = dict(
        map(
            lambda x: split(r'\s+\(base 16\)\s+', x),
            wordlist('http://standards.ieee.org/develop/regauth/oui/oui.txt', r'([\d\w]{6}\s+\(base 16\)\s+\w.+)\n')
        )
    )
    for o in ouis:
        f.write('%s\n' % ','.join([o, ouis[o]]))
    f.close()
    return ouis


def readlist(filename):
    f = fsemaphore(filename)
    f.locksh()
    data = wordlist('file://%s' % filename)
    f.close()
    return dict(map(lambda x: (x[0],x[1]), map(lambda x: x.split(','), data)))


ouis = None
tmpfile = cookie('sploitego.ieee.tmp')


if not path.exists(tmpfile) or age(tmpfile) >= config['cookie/maxage']:
    ouis = updatelist(tmpfile)
else:
    ouis = readlist(tmpfile)
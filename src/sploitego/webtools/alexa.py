#!/usr/bin/env python

from os import path

from canari.utils.fs import fsemaphore, cookie, age
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
    'topsites'
]


def updatelist(filename):
    topsites = []
    f = fsemaphore(filename, 'wb')
    f.lockex()
    for i in xrange(0,20):
        page = wordlist('http://www.alexa.com/topsites/global;%d' % i, 'topsites-label">(.*?)</')
        topsites += page
        f.write('\n'.join(page))
        f.write('\n')
    f.close()
    return topsites


def readlist(filename):
    f = fsemaphore(filename)
    f.locksh()
    data = wordlist('file://%s' % filename)
    f.close()
    return data


topsites = None
tmpfile = cookie('sploitego.alexa.tmp')


if not path.exists(tmpfile) or age(tmpfile) >= config['cookie/maxage']:
    topsites = updatelist(tmpfile)
else:
    topsites = readlist(tmpfile)
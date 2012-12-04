#!/usr/bin/env python

from os import path

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
    'subdomains'
]


def updatelist(filename):
    f = fsemaphore(filename, 'wb')
    f.lockex()
    subdomains = config['dnsdiscovery/wordlist']
    f.write('\n'.join(subdomains))
    f.close()
    return subdomains


def readlist(filename):
    f = fsemaphore(filename)
    f.locksh()
    data = wordlist('file://%s' % filename)
    f.close()
    return data


subdomains = None
tmpfile = cookie('sploitego.dnsdiscovery.tmp')

if not path.exists(tmpfile) or age(tmpfile) >= config['cookie/maxage']:
    subdomains = updatelist(tmpfile)
else:
    subdomains = readlist(tmpfile)






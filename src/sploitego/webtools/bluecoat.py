#!/usr/bin/env python

from urllib import urlopen
from os import path

from sploitego.utils.fs import fsemaphore, age, cookie
from sploitego.xmltools.objectify import objectify
from sploitego.utils.wordlist import wordlist
from sploitego.config import config

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'categories'
]


def updatelist(filename):

    f = fsemaphore(filename, 'wb')
    f.lockex()
    categories = wordlist('http://sitereview.cwfservice.net/catdesc.jsp?referrer=k9webprotection&host=%3Clocalserver%3E&port=%3Clocalport%3E', '>(\d+) - (.+?)<', ignore=None)
    for c in categories:
        f.write('%s\n' % ','.join(c))
    f.close()
    return dict(map(lambda x: (int(x[0]),x[1]), categories))


def readlist(filename):
    f = fsemaphore(filename)
    f.locksh()
    data = wordlist('file://%s' % filename)
    f.close()
    return dict(map(lambda x: (int(x[0]),x[1]), map(lambda x: x.split(','), data)))


categories = None
tmpfile = cookie('sploitego.bluecoat.tmp')


if not path.exists(tmpfile) or age(tmpfile) >= 86400:
    categories = updatelist(tmpfile)
else:
    categories = readlist(tmpfile)


def _chunks(s):
    return [ int(s[i:i+2], 16) for i in range(0, len(s), 2) ]


def sitereview(site, port=80):
    r = urlopen(
        'http://sp.cwfservice.net/1/R/%s/K9-00006/0/GET/HTTP/%s/%s///' % (config['bluecoat/license'], site, port)
    )
    if r.code == 200:
        o = objectify(r.read())
        if 'DomC' in o:
            cats = _chunks(o.DomC)
            return [ categories.get(c, 'Unknown') for c in cats ]
        elif 'DirC' in o:
            cats = _chunks(o.DirC)
            return [ categories.get(c, 'Unknown') for c in cats ]
    return []

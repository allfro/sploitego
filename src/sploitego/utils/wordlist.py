#!/usr/bin/env python

from zlib import decompress, MAX_WBITS
from re import findall, search, sub
from urllib import urlopen

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'wordlist'
]


def wordlist(uri, match='(.*?)\n+', ignore='^#.*', strip=None):
    l = []
    data = urlopen(uri).read()
    if search('\.gz(ip)?$', uri) is not None:
        data = decompress(data, 16 + MAX_WBITS)
    if data:
        l = findall(match, data)
        if ignore is not None:
            l = filter(lambda x: search(ignore, x) is None, l)
        if strip is not None:
            l = map(lambda x: sub(strip, '', x), l)
    return l



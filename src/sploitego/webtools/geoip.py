#!/usr/bin/env python

from urllib2 import urlopen
from json import loads


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'locate'
]


def locate(ip=''):
    r = urlopen('http://freegeoip.net/json/%s' % ip)
    if r.code == 200:
        return loads(r.read())
    return None
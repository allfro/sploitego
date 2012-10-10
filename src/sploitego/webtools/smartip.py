#!/usr/bin/env python

from urllib import urlopen
from json.decoder import JSONDecoder


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'geoip'
]


def geoip(ip=''):
    r = urlopen('http://smart-ip.net/geoip-json/%s' % ip)
    if r.code == 200:
        j = JSONDecoder()
        return j.decode(r.read())
    return None
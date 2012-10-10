#!/usr/bin/env python

from canari.maltego.entities import Location, IPv4Address
from sploitego.webtools.smartip import geoip
from canari.framework import configure

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'dotransform',
    'onterminate'
]


@configure(
    label='To IP Address [Internet]',
    description='This transform returns your Internet IP.',
    uuids=[ 'sploitego.v2.LocationToIPv4Address_Internet' ],
    inputs=[ ( None, Location ) ],
)
def dotransform(request, response):
    r = geoip()
    if r is not None:
        response += IPv4Address(r['host'])
    return response
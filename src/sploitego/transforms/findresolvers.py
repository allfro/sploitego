#!/usr/bin/env python

from canari.maltego.entities import Location, IPv4Address
from sploitego.scapytools.dns import resolvers
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
    'dotransform'
]


@configure(
    label='To DNS Servers [IP Config]',
    description='This transform gets the DNS servers being used by this machine.',
    uuids=[ 'sploitego.v2.LocationToDNSServer_IPConfig' ],
    inputs=[ ( 'Reconnaissance', Location ) ],
)
def dotransform(request, response):
    for r in resolvers():
        response += IPv4Address(r)
    return response
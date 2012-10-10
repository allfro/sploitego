#!/usr/bin/env python

from socket import gethostname

from canari.maltego.entities import DNSName, Location
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
    label='To DNS Name [Hostname]',
    description='This transform gets this hosts Host Name.',
    uuids=[ 'sploitego.v2.LocationToDNSName_Hostname' ],
    inputs=[ ( 'Reconnaissance', Location ) ],
)
def dotransform(request, response):
    response += DNSName(gethostname())
    return response
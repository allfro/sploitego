#!/usr/bin/env python

from sploitego.maltego.message import Location, DNSName
from sploitego.framework import configure, superuser
from sploitego.config import config
from scapy.all import DNS, sniff

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'dotransform'
]


@superuser
@configure(
    label='To DNS Names [Passive Scan]',
    description='This transform returns the DNS queries that are occuring on the local network.',
    uuids=[ 'sploitego.v2.LocationToDNSName_PassiveScan' ],
    inputs=[ ( 'Reconnaissance', Location ) ]
)
def dotransform(request, response):
    r = sniff(count=config['scapy/sniffcount'], timeout=config['scapy/snifftimeout'])
    names = {}
    for i in r:
        if DNS in i:
            for j in range(i[DNS].qdcount):
                q = i[DNS].qd[j].qname.rstrip('.')
                if q not in names:
                    names[q] = True
                    response += DNSName(q)

    return response
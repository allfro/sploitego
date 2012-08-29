#!/usr/bin/env python

from sploitego.cmdtools.nmap import NmapScanner, NmapReportParser
from sploitego.framework import configure, superuser
from sploitego.maltego.message import IPv4Address
from common.nmap import addreport

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__author__ = 'Nadeem Douba'

__all__ = [
    'dotransform'
]


@superuser
@configure(
    label='To Port [Nmap -sU]',
    description='This transform performs an active UDP Nmap scan.',
    uuids=[ 'sploitego.v2.IPv4AddressToNmapReport_NmapU' ],
    inputs=[ ( 'Reconnaissance', IPv4Address ) ],
)
def dotransform(request, response):
    s = NmapScanner()
    args = ['-n', '-sU', request.value] + request.params
    r = s.scan(args, NmapReportParser)
    addreport(r, response, ' '.join(args))
    return response



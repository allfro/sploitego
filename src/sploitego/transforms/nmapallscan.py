#!/usr/bin/env python

from sploitego.cmdtools.nmap import NmapScanner, NmapReportParser
from canari.framework import configure, superuser
from canari.maltego.entities import IPv4Address
from canari.maltego.utils import debug
from common.nmap import addreport

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


@superuser
@configure(
    label='To Nmap Report [Nmap -A]',
    description='This transform performs an active Nmap scan.',
    uuids=[ 'sploitego.v2.IPv4AddressToNmapReport_NmapA' ],
    inputs=[ ( 'Reconnaissance', IPv4Address ) ],
)
def dotransform(request, response):
    target = request.value
    s = NmapScanner()
    debug('Starting scan on host: %s' % target)
    args = ['-n', '-A', target] + request.params
    r = s.scan(args, NmapReportParser)
    addreport(r, response, ' '.join(args))
    return response

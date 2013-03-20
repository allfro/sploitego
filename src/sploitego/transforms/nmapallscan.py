#!/usr/bin/env python

from canari.framework import configure, superuser
from canari.maltego.entities import IPv4Address
from canari.maltego.message import UIMessage
from canari.maltego.utils import debug

from common.nmap import addreport, getscanner
from common.entities import IPv6Address

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.2'
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
    uuids=[ 'sploitego.v2.IPv4AddressToNmapReport_NmapA', 'sploitego.v2.IPv6AddressToNmapReport_NmapA' ],
    inputs=[ ( 'Reconnaissance', IPv4Address ), ( 'Reconnaissance', IPv6Address ) ],
)
def dotransform(request, response):
    s = getscanner()
    debug('Starting scan on host: %s' % request.params)
    args = ['-n', '-A'] + request.params
    r = s.scan(request.value, *args)
    if r is not None:
        addreport(r, response, ' '.join(args + [request.value]), s.cmd)
    else:
        response += UIMessage(s.error)
    return response

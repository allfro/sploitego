#!/usr/bin/env python

from sploitego.cmdtools.nmap import NmapReportParser
from canari.maltego.entities import BuiltWithTechnology
from canari.framework import configure, superuser
from canari.maltego.message import UIMessage
from canari.maltego.message import Label
from common.entities import Port
from common.nmap import getscanner


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


@superuser
@configure(
    label='To Banner [Nmap -sV]',
    description='This transform performs an Nmap Version Scan. Note: this is an active scan.',
    uuids=[ 'sploitego.v2.PortToBanner_NmapV' ],
    inputs=[ ( 'Reconnaissance', Port ) ],
)
def dotransform(request, response):
    s = getscanner()
    args = ['-n', '-sV', '-p', request.value, request.fields['ip.destination']] + request.params
    if request.fields['protocol'] == 'UDP':
        args.insert(0, '-sU')
    r = s.scan(args, NmapReportParser)
    if r is not None:
        for host in r.addresses:
            for port in r.ports(host):
                e = BuiltWithTechnology(r.tobanner(port))
                if 'servicefp' in port:
                    e += Label('Service Fingerprint', port['servicefp'])
                if 'extrainfo' in port:
                    e += Label('Extra Information', port['extrainfo'])
                if 'method' in port:
                    e += Label('Method', port['method'])
                response += e
    else:
        response += UIMessage(s.error)
    return response
#!/usr/bin/env python

from sploitego.transforms.common.entities import NmapReport
from sploitego.transforms.common.nmap import addports
from sploitego.cmdtools.nmap import NmapReportParser
from canari.framework import configure


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


@configure(
    label='To Ports [Nmap Report]',
    description='This transform mines port scan information from an Nmap report.',
    uuids=[ 'sploitego.v2.NmapReportToPorts_NmapReport' ],
    inputs=[ ( 'Reconnaissance', NmapReport ) ],
)
def dotransform(request, response):
    r = NmapReportParser(file(request.fields['report.file']).read())
    addports(r, response)
    return response
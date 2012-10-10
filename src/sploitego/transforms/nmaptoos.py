#!/usr/bin/env python

from sploitego.transforms.common.entities import NmapReport
from sploitego.transforms.common.nmap import addsystems
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
    label='To OS [Nmap Report]',
    description='This transform mines OS information from an Nmap report.',
    uuids=[ 'sploitego.v2.NmapReportToOS_NmapReport' ],
    inputs=[ ( 'Reconnaissance', NmapReport ) ],
)
def dotransform(request, response):
    r = NmapReportParser(file(request.fields['report.file']).read())
    addsystems(r, response)
    return response
#!/usr/bin/env python

from sploitego.cmdtools.amap import AmapScanner, AmapReportParser
from canari.maltego.entities import BuiltWithTechnology
from sploitego.cmdtools.nmap import NmapReportParser
from canari.maltego.message import Label
from canari.framework import configure
from common.entities import NmapReport

from tempfile import NamedTemporaryFile


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
    label='To Banners [Amap]',
    description='This transform uses Amap to fingerprint services identified from an Nmap Report.',
    uuids=[ 'sploitego.v2.NmapReportToBanner_Amap' ],
    inputs=[ ( 'Reconnaissance', NmapReport ) ]
)
def dotransform(request, response):
    s = AmapScanner()
    f = NamedTemporaryFile(suffix='.gnmap', mode='wb')
    f.write(NmapReportParser(file(request.fields['report.file']).read()).greppable)
    f.flush()
    r = s.scan(['-bqi', f.name], AmapReportParser)
    f.close()
    for b in r.banners:
        e = BuiltWithTechnology(b[1])
        e += Label('Destination', b[0])
        e += Label('Extra Information', b[2])
        response += e
    return response
#!/usr/bin/env python

from canari.maltego.entities import Location, IPv4Address, DNSName
from canari.maltego.message import UIMessage, Label
from sploitego.webtools.smartip import geoip
from canari.framework import configure
from canari.config import config
from sploitego.resource import flag
from canari.maltego.html import A


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


def maplink(r):
    l = config['geoip/maplink']
    for k in r:
        var = '$%s' % k
        if var in l:
            l = l.replace(var, r[k])
    return l

@configure(
    label='To Location [Smart IP]',
    description='This transform attempts to geo locate the given IP or hostname.',
    uuids=[
        'sploitego.v2.IPv4AddressToLocation_SmartIP',
#        'sploitego.v2.NSRecordToLocation_SmartIP',
        'sploitego.v2.DNSNameToLocation_SmartIP',
#        'sploitego.v2.MXRecordToLocation_SmartIP'
    ],
    inputs=[
        ( 'Reconnaissance', IPv4Address ),
#        ( 'Reconnaissance', NSRecord ),
        ( 'Reconnaissance', DNSName ),
#        ( 'Reconnaissance', MXRecord )
    ],
)
def dotransform(request, response):
    r = geoip(request.value)
    if r is not None:
        if 'error' in r:
            response += UIMessage(r['error'])
            return response
        locname = ''
        cityf = None
        countryf = None
        if 'city' in r:
            locname += r['city']
            cityf = r['city']
        if 'countryName' in r:
            locname += ', %s' % r['countryName']
            countryf = r['countryName']
        e = Location(locname)
        if 'longitude' in r and 'latitude' in r:
            e.longitude = r['longitude']
            e.latitude = r['latitude']
            link = maplink(r)
            e += Label('Map It', A(link, link), type='text/html')
        if 'region' in r:
            e.area = r['region']
        if cityf is not None:
            e.city = cityf
        if countryf is not None:
            e.country = countryf
            e.iconurl = flag(countryf)
        if 'countryCode' in r:
            e.countrycode =  r['countryCode']
            if e.iconurl is None:
                e.iconurl = flag(r['countryCode'])
        response += e
    return response

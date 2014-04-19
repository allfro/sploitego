#!/usr/bin/env python

import string

from canari.maltego.entities import Location, IPv4Address, DNSName
from canari.maltego.message import UIMessage, Label
from canari.framework import configure
from canari.maltego.html import A

from sploitego.webtools.geoip import locate
from sploitego.resource import flag


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


def maplink(r, config):
    l = config['geoip/maplink']
    return l.format(**r)

@configure(
    label='To Location [Smart IP]',
    description='This transform attempts to geo locate the given IP or hostname.',
    uuids=[
        'sploitego.v2.IPv4AddressToLocation_SmartIP',
        'sploitego.v2.DNSNameToLocation_SmartIP'
    ],
    inputs=[
        ('Reconnaissance', IPv4Address),
        ('Reconnaissance', DNSName)
    ],
    remote=True
)
def dotransform(request, response, config):
    r = locate(request.value)
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
        if 'country_name' in r:
            locname += ', %s' % r['country_name']
            countryf = r['country_name']
        e = Location(locname)
        if 'longitude' in r and 'latitude' in r:
            e.longitude = float(r['longitude'] or 0.0)
            e.latitude = float(r['latitude'] or 0.0)
            link = maplink(r, config)
            e += Label('Map It', A(link, link), type='text/html')
        if 'region_name' in r:
            e.area = r['region_name']
        if cityf is not None:
            e.city = cityf
        if countryf is not None:
            e.country = countryf
            e.iconurl = flag(countryf)
        if 'country_code' in r:
            e.countrycode = r['country_code']
            if e.iconurl is None:
                e.iconurl = flag(r['country_code'])
        response += e
    return response

#!/usr/bin/env python

from re import split

from canari.maltego.message import UIMessage, Field, MatchingRule
from canari.maltego.entities import Device, IPv4Address
from canari.framework import configure


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
    label='To Device [IEEE OUI]',
    description='This transform gets the device manufacturer based on the MAC Address OUI.',
    uuids=[ 'sploitego.v2.IPv4AddressToDevice_IEEEOUI' ],
    inputs=[ ( 'Reconnaissance', IPv4Address ) ],
)
def dotransform(request, response):
    from sploitego.webtools.ieee import ouis
    if 'ethernet.hwaddr' not in request.fields or not request.fields['ethernet.hwaddr']:
        response += UIMessage('You must provide an Ethernet Hardware Address (ethernet.hwaddr) property.')
    else:
        oui = ''.join(request.fields['ethernet.hwaddr'].split(':')[0:3]).upper()
        if oui in ouis:
            e = Device(split('[^\w]', ouis[oui], 1)[0].title())
            e += Field('organization', ouis[oui], matchingrule=MatchingRule.Loose)
            response += e
        else:
            response += Device('Unknown Manufacturer')
    return response
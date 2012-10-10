#!/usr/bin/env python

from canari.maltego.entities import IPv4Address, Location
from canari.maltego.message import Field, MatchingRule
from canari.framework import configure
from scapy.all import IP, Ether

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
    label='To IP Address [Local]',
    description='This transform gets the interface IP Address.',
    uuids=[ 'sploitego.v2.LocationToIPv4Address_Local' ],
    inputs=[ ( 'Reconnaissance', Location ) ],
)
def dotransform(request, response):
    e = IPv4Address(IP(dst='4.2.2.1').src)
    e.internal = True
    e += Field(
        "ethernet.hwaddr", (Ether()/IP(dst='4.2.2.1')).src,
        displayname="Hardware Address", matching_rule=MatchingRule.Loose
    )
    response += e
    return response
#!/usr/bin/env python

from canari.framework import superuser, configure
from canari.maltego.entities import IPv4Address
from canari.maltego.message import Field
from scapy.all import conf, getmacbyip


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
]


@superuser
@configure(
    label='To Next Hop [Routing Table]',
    description='This transform fetches the next hop or router for a given destination.',
    uuids=[ 'sploitego.v2.IPv4AddressToNextHop_RoutingTable' ],
    inputs=[ ( 'Reconnaissance', IPv4Address ) ],
)
def dotransform(request, response):
    nexthop = conf.route6.route(request.value)[2] if ':' in request.value else conf.route.route(request.value)[2]
    e = IPv4Address(nexthop)
    e.internal = True
    if ':' not in nexthop:
        e += Field('ethernet.hwaddr', getmacbyip(nexthop), displayname='Hardware Address')
    response += e
    return response
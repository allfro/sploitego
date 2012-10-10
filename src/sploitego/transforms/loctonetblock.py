#!/usr/bin/env python

from canari.maltego.entities import Netblock, Location
from iptools.ip import IPAddress, IPNetwork
from canari.framework import configure
from scapy.all import conf

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
    label='To IP Netblocks [Local]',
    description='This transform gets the netblocks that are directly attached to this computer.',
    uuids=[ 'sploitego.v2.LocationToNetblock_Local' ],
    inputs=[ ( 'Reconnaissance', Location ) ],
)
def dotransform(request, response):

    for r in conf.route.routes:
        net = IPNetwork([IPAddress(r[0]), IPAddress(r[1])])
        if net.cidrlen not in [32, 0]:
            response += Netblock(net.netblock)

    return response
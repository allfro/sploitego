#!/usr/bin/env python

from sploitego.maltego.message import Netblock, Label, IPv4Address, BuiltInTransformSets
from sploitego.iptools.ip import IPAddress, IPNetwork
from sploitego.xmltools.objectify import objectify
from sploitego.iptools.arin import whoisip
from sploitego.framework import configure

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'dotransform'
]


@configure(
    label='To Netblocks [ARIN WHOIS]',
    description='This transform fetches the net blocks that the given IP belongs to using an ARIN WHOIS lookup.',
    uuids=[ 'sploitego.v2.IPv4AddressToNetblock_ARIN' ],
    inputs=[ ( BuiltInTransformSets.IPOwnerDetail, IPv4Address ) ],
)
def dotransform(request, response):
    ip = IPAddress(request.value)
    w = objectify(whoisip(ip, accept='application/xml'))
    network = IPNetwork([w.startAddress, w.endAddress])
    e = Netblock(network.netblock)
    e += Label('CIDR Notation', repr(network))
    e += Label('Network Mask', network.netmask)
    e += Label('Number of Hosts', int(~network.netmask) - 1)
    response += e
    for nb in w.netBlocks.netBlock:
        network = IPNetwork([nb.startAddress, nb.endAddress])
        e = Netblock(network.netblock)
        e += Label('CIDR Notation', repr(network))
        e += Label('Network Mask', network.netmask)
        e += Label('Number of Hosts', int(~network.netmask) - 1)
    return response
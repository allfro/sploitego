#!/usr/bin/env python

from canari.maltego.configuration import BuiltInTransformSets
from canari.maltego.entities import Netblock, IPv4Address
from xml.etree.cElementTree import fromstring
from iptools.ip import IPAddress, IPNetwork
from canari.maltego.message import Label
from canari.framework import configure
from iptools.arin import whoisip


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
    label='To Netblocks [ARIN WHOIS]',
    description='This transform fetches the net blocks that the given IP belongs to using an ARIN WHOIS lookup.',
    uuids=[ 'sploitego.v2.IPv4AddressToNetblock_ARIN' ],
    inputs=[ ( BuiltInTransformSets.IPOwnerDetail, IPv4Address ) ],
)
def dotransform(request, response):
    ip = IPAddress(request.value)
    w = fromstring(whoisip(ip, accept='application/xml'))
    network = IPNetwork([
        w.find('{http://www.arin.net/whoisrws/core/v1}startAddress').text,
        w.find('{http://www.arin.net/whoisrws/core/v1}endAddress').text
    ])
    e = Netblock(network.netblock)
    e += Label('CIDR Notation', repr(network))
    e += Label('Network Mask', network.netmask)
    e += Label('Number of Hosts', int(~network.netmask) - 1)
    response += e
    for nb in w.findall('netBlocks/netBlock'):
        network = IPNetwork([
            nb.find('startAddress').text,
            nb.find('endAddress').text
        ])
        e = Netblock(network.netblock)
        e += Label('CIDR Notation', repr(network))
        e += Label('Network Mask', network.netmask)
        e += Label('Number of Hosts', int(~network.netmask) - 1)
    return response
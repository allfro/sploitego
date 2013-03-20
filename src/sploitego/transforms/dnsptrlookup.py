#!/usr/bin/env python

from canari.maltego.configuration import BuiltInTransformSets
from canari.maltego.entities import IPv4Address
from canari.framework import configure

from common.entities import IPv6Address
from common.dnstools import nslookup


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.2'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'dotransform'
]


@configure(
    label='To DNS Name [DNS]',
    description='This transform will fetch the DNS records for a IP address.',
    uuids=[ 'sploitego.v2.IPv4AddressToDNSName_DNS', 'sploitego.v2.IPv6AddressToDNSName_DNS' ],
    inputs=[ ( BuiltInTransformSets.DNSFromIP, IPv4Address ), ( BuiltInTransformSets.DNSFromIP, IPv6Address ) ]
)
def dotransform(request, response):
    nslookup(request.value, 'PTR', response)
    return response
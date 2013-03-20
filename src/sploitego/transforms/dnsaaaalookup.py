#!/usr/bin/env python

from canari.maltego.configuration import BuiltInTransformSets
from canari.maltego.entities import DNSName
from canari.framework import configure

from common.dnstools import nslookup

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
    label='To IPv6 Address [DNS]',
    description='This transform attempts to resolve a DNS record to an IPv6 Address.',
    uuids=[
        'sploitego.v2.DNSNameToIPv6Address_DNS'
    ],
    inputs=[
        ( BuiltInTransformSets.ResolveToIP, DNSName )
    ]
)
def dotransform(request, response):
    nslookup(request.value, 'AAAA', response)
    return response
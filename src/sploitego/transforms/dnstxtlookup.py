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
    label='To TXT Record [DNS]',
    description='This transform attempts to resolve a DNS record to an TXT record.',
    uuids=[
        'sploitego.v2.DNSNameToTXT_DNS'
    ],
    inputs=[
        ( BuiltInTransformSets.ResolveToIP, DNSName )
    ]
)
def dotransform(request, response):
    nslookup(request.value, 'TXT', response)
    return response
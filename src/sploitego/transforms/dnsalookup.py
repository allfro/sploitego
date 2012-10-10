#!/usr/bin/env python

from canari.maltego.configuration import BuiltInTransformSets
from canari.maltego.entities import IPv4Address, DNSName
from sploitego.scapytools.dns import nslookup
from canari.framework import configure
from scapy.all import DNS


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
    label='To IPv4 Address [DNS]',
    description='This transform attempts to resolve a DNS record to an IPv4 Address.',
    uuids=[
#        'sploitego.v2.DomainToIPv4Address_DNS',
        'sploitego.v2.DNSNameToIPv4Address_DNS',
#        'sploitego.v2.MXRecordToIPv4Address_DNS',
#        'sploitego.v2.NSRecordToIPv4Address_DNS'
    ],
    inputs=[
#        ( BuiltInTransformSets.ResolveToIP, Domain ),
        ( BuiltInTransformSets.ResolveToIP, DNSName ),
#        ( BuiltInTransformSets.ResolveToIP, MXRecord ),
#        ( BuiltInTransformSets.ResolveToIP, NSRecord )
    ]
)
def dotransform(request, response):
    ans = nslookup(request.value)
    if ans is not None and DNS in ans:
        for i in range(0, ans[DNS].ancount):
            if ans[DNS].an[i].type == 1:
                response += IPv4Address(ans[DNS].an[i].rdata)
    return response
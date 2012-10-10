#!/usr/bin/env python

from canari.maltego.configuration import BuiltInTransformSets
from canari.maltego.entities import NSRecord, Domain
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
    label='To NS Records [DNS]',
    description='This transform attempts to resolve a DNS record to an IPv4 Address.',
    uuids=[ 'sploitego.v2.DomainToNSRecord_DNS' ],
    inputs=[ ( BuiltInTransformSets.DNSFromDomain, Domain ) ]
)
def dotransform(request, response):
    ans = nslookup(request.value, 'NS')
    if ans is not None and DNS in ans:
        for i in range(0, ans[DNS].ancount):
            if ans[DNS].an[i].type == 2:
                response += NSRecord(ans[DNS].an[i].rdata.rstrip('.'))
    return response
#!/usr/bin/env python

from canari.maltego.configuration import BuiltInTransformSets
from canari.maltego.entities import DNSName, IPv4Address
from sploitego.scapytools.dns import nslookup
from canari.framework import configure
from iptools.ip import IPAddress
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
    label='To DNS Name [DNS]',
    description='This transform will fetch the DNS records for a IP address.',
    uuids=[ 'sploitego.v2.IPv4AddressToDNSName_DNS' ],
    inputs=[ ( BuiltInTransformSets.DNSFromIP, IPv4Address ) ]
)
def dotransform(request, response):
    ans = nslookup(IPAddress(request.value).arpa, 'PTR')
    if ans is not None and DNS in ans:
        for i in range(0, ans[DNS].ancount):
            if ans[DNS].an[i].type == 12:
                e = DNSName(ans[DNS].an[i].rdata.rstrip('.'))
                response += e
    return response
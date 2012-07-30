#!/usr/bin/env python

from sploitego.maltego.message import DNSName, IPv4Address, BuiltInTransformSets
from sploitego.scapytools.dns import nslookup
from sploitego.iptools.ip import IPAddress
from sploitego.framework import configure
from scapy.all import DNS

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
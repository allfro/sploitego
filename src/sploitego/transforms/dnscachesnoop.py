#!/usr/bin/env python

from sploitego.maltego.message import NSRecord, Label, UIMessage, Table, DNSName, IPv4Address
from sploitego.scapytools.dns import nslookup
from sploitego.webtools.alexa import topsites
from sploitego.framework import configure
from sploitego.maltego.utils import debug
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
    label='To DNS Names [Cache Snoop]',
    description='This transform performs DNS cache snooping on the target DNS server for the Alexa top 500 list.',
    uuids=[
        'sploitego.v2.IPv4AddressToDNSName_CacheSnoop',
        'sploitego.v2.NSRecordToDNSName_CacheSnoop'
    ],
    inputs=[
        ( 'Reconnaissance', IPv4Address ),
        ( 'Reconnaissance', NSRecord )
    ]
)
def dotransform(request, response):
    ip = request.value
    ans = nslookup("www.google.ca", nameserver=ip)
    if ans is not None:
        for site in topsites:
            debug('Resolving %s' % site)
            ans = nslookup(site, nameserver=ip, rd=0)
            if ans[DNS].ancount:
                e = DNSName(site)
                t = Table(['Name', 'Query Class', 'Query Type', 'Data', 'TTL'], 'Cached Answers')
                for i in range(0, ans[DNS].ancount):
                    rr = ans[DNS].an[i]
                    t.addrow([
                            rr.rrname.rstrip('.'),
                            rr.sprintf('%rclass%'),
                            rr.sprintf('%type%'),
                            rr.rdata.rstrip('.'),
                            rr.sprintf('%ttl%')
                        ])
                e += Label('Cached Answers', t, type='text/html')
                response += e
    else:
        response += UIMessage('DNS server did not respond to initial DNS request.')
    return response
# !/usr/bin/env python

from canari.maltego.entities import NSRecord, DNSName, IPv4Address
from canari.maltego.message import Label, UIMessage
from canari.framework import configure
from canari.maltego.utils import debug
from canari.maltego.html import Table
from canari.config import config

import dns.query
import dns.message
import dns.rdatatype
import dns.rdataclass

from common.dnstools import nslookup_raw

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
    label='To DNS Names [Cache Snoop]',
    description='This transform performs DNS cache snooping on the target DNS server for the Alexa top 500 list.',
    uuids=[
        'sploitego.v2.IPv4AddressToDNSName_CacheSnoop',
        'sploitego.v2.NSRecordToDNSName_CacheSnoop'
    ],
    inputs=[
        ('Reconnaissance', IPv4Address),
        ('Reconnaissance', NSRecord)
    ]
)
def dotransform(request, response):
    nameserver = request.value

    if nslookup_raw('www.google.ca', resolver=nameserver).answer:
        for site in config['dnscachesnoop/wordlist']:
            debug('Resolving %s' % site)

            msg = nslookup_raw(site, resolver=nameserver, recursive=False)
            if not msg.answer:
                msg = nslookup_raw('www.%s' % site, resolver=nameserver, recursive=False)
            if msg.answer:
                e = DNSName(site)
                t = Table(['Name', 'Query Class', 'Query Type', 'Data', 'TTL'], 'Cached Answers')
                for rrset in msg.answer:
                    for rr in rrset:
                        t.addrow([
                            rrset.name.to_text(),
                            dns.rdataclass.to_text(rr.rdclass),
                            dns.rdatatype.to_text(rr.rdtype),
                            rr.to_text(),
                            rrset.ttl
                        ])
                e += Label('Cached Answers from %s' % nameserver, t, type='text/html')
                response += e
    else:
        response += UIMessage('DNS server did not respond to initial DNS request.')
    return response
#!/usr/bin/env python

from re import sub

from sploitego.maltego.message import  NSRecord, MXRecord, Domain, DNSName, Phrase, Field, BuiltInTransformSets
from sploitego.scapytools.dns import nslookup
from sploitego.framework import configure
from sploitego.maltego.utils import debug
from sploitego.config import config
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



def addrecord(record, response):
    if record.type == 2:
        response += NSRecord(record.rdata.rstrip('.'))
    elif record.type == 15:
        e = MXRecord(record.rdata.rstrip('.'))
        e += Field('mxrecord.priority', record.mxpriority)
        response += e
    elif record.type in [ 1, 5 ]:
        response += DNSName(record.rrname.rstrip('.'))
    elif record.type == 16:
        response += Phrase(sub('[\x00-\x1f]', '', record.rdata))
    return response


@configure(
    label='To DNS Names [Cached DNS]',
    description='This transform attempts to fetch all cached records known to the DNS servers.',
    uuids=[ 'sploitego.v2.DomainToDNSName_CachedDNS' ],
    inputs=[ ( BuiltInTransformSets.DNSFromDomain, Domain ) ]
)
def dotransform(request, response):

    for r in config['dnscachelookup/resolvers']:
        debug('fetching from %s' % r)
        ans = nslookup(request.value, 255, r, rd=0)
        if ans is None:
            continue
        elif isinstance(ans, list):
            for a in ans:
                addrecord(a.an, response)
        elif ans[DNS].ancount:
            for i in range(0, ans[DNS].ancount):
                addrecord(ans[DNS].an[i], response)
    return response
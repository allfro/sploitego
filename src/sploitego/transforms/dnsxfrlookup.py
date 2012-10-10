#!/usr/bin/env python

from canari.maltego.entities import NSRecord, MXRecord, DNSName, Phrase, Domain
from canari.maltego.configuration import BuiltInTransformSets
from canari.maltego.message import Field, UIMessage
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
        response += Phrase(record.rdata)
    return response


@configure(
    label='To DNS Names [DNS AXFR/IXFR]',
    description='This transform attempts to perform a DNS AXFR/IXFR transfer.',
    uuids=[ 'sploitego.v2.DomainToDNSName_XFR' ],
    inputs=[ ( BuiltInTransformSets.DNSFromDomain, Domain ) ]
)
def dotransform(request, response):
    ans = nslookup(request.value, 'AXFR')
    if not isinstance(ans, list) and not ans[DNS].ancount:
        ans = nslookup(request.value, 'IXFR')
    if isinstance(ans, list):
        for a in ans:
            addrecord(a.an, response)
    elif ans[DNS].ancount:
        for i in range(0, ans[DNS].ancount):
            addrecord(ans[DNS].an[i], response)
    else:
        response += UIMessage('AXFR/IXFR was unsuccessful.')
    return response
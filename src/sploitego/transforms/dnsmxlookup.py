#!/usr/bin/env python

from canari.maltego.configuration import BuiltInTransformSets
from canari.maltego.entities import MXRecord, Domain
from sploitego.scapytools.dns import nslookup
from canari.maltego.message import Field
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
    label='To MX Records [DNS]',
    description='This transform will fetch the MX records for a given domain.',
    uuids=[ 'sploitego.v2.DomainToMXRecord_DNS' ],
    inputs=[ ( BuiltInTransformSets.DNSFromDomain, Domain ) ]
)
def dotransform(request, response):
    ans = nslookup(request.value, 'MX')
    if ans is not None and DNS in ans:
        for i in range(0, ans[DNS].ancount):
            if ans[DNS].an[i].type == 15:
                e = MXRecord(ans[DNS].an[i].rdata.rstrip('.'))
                e += Field('mxrecord.priority', ans[DNS].an[i].mxpriority)
                response += e
    return response
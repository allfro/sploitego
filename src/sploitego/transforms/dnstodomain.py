#!/usr/bin/env python

from canari.maltego.configuration import BuiltInTransformSets
from canari.maltego.entities import DNSName, Domain
from canari.framework import configure


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
    label='To Domain [DNS]',
    description='This transform gets the domain of the DNS name.',
    uuids=[
        'sploitego.v2.DNSNameToDomain_DNS',
#        'sploitego.v2.NSRecordToDomain_DNS',
#        'sploitego.v2.MXRecordToDomain_DNS'
    ],
    inputs=[
        ( BuiltInTransformSets.DomainFromDNS, DNSName ),
#        ( BuiltInTransformSets.DomainFromDNS, NSRecord ),
#        ( BuiltInTransformSets.DomainFromDNS, MXRecord )
    ]
)
def dotransform(request, response):
    dns = request.value
    if '.' in dns:
        response += Domain('.'.join(dns.split('.')[-2:]))
    else:
        response += Domain(request.value)
    return response
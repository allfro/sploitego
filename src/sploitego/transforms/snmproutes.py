#!/usr/bin/env python

from sploitego.scapytools.snmp import SNMPManager, SNMPError
from canari.maltego.message import UIMessage, Label
from canari.maltego.entities import IPv4Address
from common.entities import SNMPCommunity
from canari.framework import configure
from canari.maltego.html import Table
from common.snmp import snmpargs


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
    label='To Routes [SNMP]',
    description='This transform uses SNMP to retrieve the routing table for the device being queried.',
    uuids=['sploitego.v2.SNMPCommunityToRoute_SNMP'],
    inputs=[('Reconnaissance', SNMPCommunity)]
)
def dotransform(request, response):
    try:
        s = SNMPManager(*snmpargs(request))
        nexthops = {}
        for i in s.walk('1.3.6.1.2.1.4.21.1.1'):
            nm = s.get('.'.join(['1.3.6.1.2.1.4.21.1.11', i['value']]))
            if nm['value'] != '255.255.255.255':
                nh = s.get('.'.join(['1.3.6.1.2.1.4.21.1.7', i['value']]))
                if nh['value'] not in nexthops:
                    nexthops[nh['value']] = []
                nexthops[nh['value']].append(i['value'])
        for nh in nexthops:
            e = IPv4Address(nh)
            t = Table(['Destination Network'], 'Routing Table')
            for r in nexthops[nh]:
                t.addrow([r])
            e += Label('Routing Table', t, type='text/html')
            response += e
    except SNMPError, s:
        response += UIMessage(str(s))
    return response
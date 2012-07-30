#!/usr/bin/env python

from sploitego.framework import configure
from common.entities import SNMPCommunity
from sploitego.scapytools.snmp import SNMPManager, SNMPError
from common.snmp import snmpargs
from sploitego.maltego.message import DNSName, UIMessage

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
    label='To DNS Name [SNMP]',
    description='This transform uses SNMP to retrieve the hostname of the device being queried.',
    uuids=['sploitego.v2.SNMPCommunityToDNSName_SNMP'],
    inputs=[('Reconnaissance', SNMPCommunity)]
)
def dotransform(request, response):
    try:
        s = SNMPManager(*snmpargs(request))
        response += DNSName(s.hostname)
    except SNMPError, s:
        response += UIMessage(str(s))
    return response
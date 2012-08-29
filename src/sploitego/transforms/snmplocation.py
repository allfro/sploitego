#!/usr/bin/env python

from sploitego.framework import configure
from common.entities import SNMPCommunity
from sploitego.scapytools.snmp import SNMPManager, SNMPError
from common.snmp import snmpargs
from sploitego.maltego.message import Location, UIMessage

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
    label='To Location [SNMP]',
    description='This transform uses SNMP to retrieve the location of the device being queried.',
    uuids=['sploitego.v2.SNMPCommunityToLocation_SNMP'],
    inputs=[('Reconnaissance', SNMPCommunity)]
)
def dotransform(request, response):
    try:
        s = SNMPManager(*snmpargs(request))
        response += Location(s.location)
    except SNMPError, s:
        response += UIMessage(str(s))
    return response



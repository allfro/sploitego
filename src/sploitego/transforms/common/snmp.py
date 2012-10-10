#!/usr/bin/env python

from canari.maltego.message import MaltegoException
from iptools.ip import IPAddress
from canari.config import config


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


def snmpargs(request):
    if request.fields['protocol'].upper() != 'UDP':
        raise MaltegoException('SNMP over UDP for versions 1 and 2c are only supported.')
    return (
        str(IPAddress(request.fields['snmp.agent'])),
        int(request.fields['ip.port']),
        request.value,
        request.fields['snmp.version'],
        config['scapy/sr_timeout'],
        config['scapy/sr_retries']
    )
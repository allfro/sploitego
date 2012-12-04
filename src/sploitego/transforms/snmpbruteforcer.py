#!/usr/bin/env python

from sploitego.scapytools.snmp import SNMPBruteForcer
from canari.maltego.message import MaltegoException
from common.entities import Port, SNMPCommunity
from canari.utils.wordlist import wordlist
from canari.framework import configure
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

__all__ = [
    'dotransform'
]


@configure(
    label='To SNMP Community [Brute Force]',
    description='This transform attempts to find SNMP community strings using a word list',
    uuids=['sploitego.v2.PortToSNMPCommunity_BruteForce'],
    inputs=[('Reconnaissance', Port)]
)
def dotransform(request, response):
    protocol = request.fields['protocol'].upper()
    if protocol != 'UDP':
        raise MaltegoException('SNMP over UDP for versions 1 and 2c are only supported.')
    agent = str(IPAddress(request.fields['ip.destination']))
    port = int(request.value)
    wl = config['snmp/wordlist']
    for v in ['v1', 'v2c']:
        bf = SNMPBruteForcer(agent, port, v, config['snmp/bf_timeout'], config['snmp/bf_rate'])
        for c in bf.guess(wl):
            e = SNMPCommunity(c)
            e.port = port
            e.agent = agent
            e.protocol = protocol
            e.version = v
            response += e
    return response

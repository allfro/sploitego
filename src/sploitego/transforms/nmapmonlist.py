#!/usr/bin/env python

import re

from sploitego.cmdtools.nmap import NmapReportParser
from canari.maltego.entities import IPv4Address
from canari.framework import configure, superuser
from canari.maltego.message import UIMessage, Field, Label
from common.entities import Port
from common.nmap import getscanner, savereport


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'dotransform',
    'onterminate'
]


@superuser
@configure(
    label='To Client IPv4Address [NTP monlist]',
    description='This transform performs an Nmap NTP monlist scan to retrieve a list of NTP clients.',
    uuids=[ 'sploitego.v2.PortToClients_NTPMonList' ],
    inputs=[ ( 'Reconnaissance', Port ) ],
)
def dotransform(request, response):

    if request.fields['protocol'] != 'UDP':
        response += UIMessage('NTP Monlist scans only work on UDP ports.')
        return response

    s = getscanner()

    args = [ '-n', '-Pn', '-sU', '--script=ntp-monlist', '-p', request.value ] + request.params

    r = s.scan(request.fields['ip.destination'], *args)

    if r is not None:
        for host in r.addresses:
            for port in r.ports(host):
                if 'ntp-monlist' in port['script']:
                    to_clients(response, port['script']['ntp-monlist'])
    else:
        response += UIMessage(s.error)

    return response


class Category:
    AlternativeTargetInterfaces = 0
    PrivateServers = 1
    PublicServers = 2
    PrivatePeers = 3
    PublicPeers = 4
    PrivateClients = 5
    PublicClients = 6
    OtherAssociations = 7

    @classmethod
    def name(cls, id):
        if not id:
            return 'Alternative Target Interfaces'
        elif id == 1:
            return 'Private Servers'
        elif id == 2:
            return 'Public Servers'
        elif id == 3:
            return 'Private Peers'
        elif id == 4:
            return 'Public Peers'
        elif id == 5:
            return 'Private Clients'
        elif id == 6:
            return 'Public Clients'
        elif id == 7:
            return 'Other Associations'


ip_matcher = re.compile('([\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})')


def to_clients(response, output):
    cat = None
    for line in output.split('\n'):
        if not line:
            continue
        elif line.startswith('      '):
            e = None
            if cat in range(Category.AlternativeTargetInterfaces, Category.OtherAssociations):
                for ip in ip_matcher.findall(line):
                    e = IPv4Address(ip)
                    e += Field('category', Category.name(cat), displayname='Category')
                    response += e
            elif cat == Category.OtherAssociations:
                ip, desc = line.strip().split(' ', 1)
                e = IPv4Address(ip)
                e += Label('Additional Info', desc)
                e += Field('category', Category.name(cat), displayname='Category')
                response += e
        elif line.startswith('  '):
            for id in range(Category.AlternativeTargetInterfaces, Category.OtherAssociations + 1):
                if Category.name(id) in line:
                    cat = id
                    break
#!/usr/bin/env python

from socket import socket, SOCK_DGRAM, AF_INET, timeout
from random import randint
from time import sleep

from scapy.all import (SNMP, SNMPnext, SNMPvarbind, ASN1_OID, SNMPget, ASN1_DECODING_ERROR, ASN1_NULL, ASN1_IPADDRESS,
                       SNMPset, SNMPbulk)
from iptools.ip import IPAddress


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


class SNMPError(Exception):
    pass


class SNMPVersion:
    v1 = 0
    v2c = 1
    v3 = 2

    @classmethod
    def iversion(cls, v):
        if v in ['v1', '1']:
            return cls.v1
        elif v in ['v2', '2', 'v2c']:
            return cls.v2c
        elif v in ['v3', '3']:
            return cls.v3
        raise ValueError('No such version %s' % v)

    @classmethod
    def sversion(cls, v):
        if not v:
            return 'v1'
        elif v == 1:
            return 'v2c'
        elif v == 2:
            return 'v3'
        raise ValueError('No such version number %s' % v)


class SNMPManager(object):

    def __init__(self, agent, port=161, community='public', version='v2c', timeout=2, retry=3):
        self.version = SNMPVersion.iversion(version)
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.s.settimeout(timeout)
        self.addr = (agent, port)
        self.community = community
        self.retry = retry + 1
        self._check()

    def _check(self):
        return self.description

    @property
    def description(self):
        return self.get('1.3.6.1.2.1.1.1.0')['value']

    @property
    def contact(self):
        return self.get('1.3.6.1.2.1.1.4.0')['value']

    @property
    def hostname(self):
        return self.get('1.3.6.1.2.1.1.5.0')['value']

    @property
    def location(self):
        return self.get('1.3.6.1.2.1.1.6.0')['value']

    def _sr(self, p):
        retry = 0
        while retry < self.retry:
            i = randint(0, 2147483647)
            p.PDU.id = i
            self.s.sendto(str(p), self.addr)
            r = None
            try:
                while True:
                    r = SNMP(self.s.recvfrom(65535)[0])
                    if r.PDU.id.val == i:
                        break
            except timeout:
                retry += 1
                continue
            error = r.PDU.error.val
            if not error:
                return r
            elif error == 1:
                raise SNMPError('Response message too large to transport.')
            elif error == 2:
                raise SNMPError('The name of the requested object was not found.')
            elif error == 3:
                raise SNMPError('A data type in the request did not match the data type in the SNMP agent.')
            elif error == 4:
                raise SNMPError('The SNMP manager attempted to set a read-only parameter')
            raise SNMPError('An unknown error has occurred')
        raise SNMPError('Unable to connect to host %s.' % repr(self.addr))

    def getnext(self, oid):
        p = SNMP(
            community=self.community,
            version=self.version,
            PDU=SNMPnext(varbindlist=[SNMPvarbind(oid=ASN1_OID(oid))])
        )
        r = self._sr(p).PDU.varbindlist[0]
        return {'oid':r.oid.val, 'type':type(r.value), 'value':r.value.val}

    def walk(self, oid):
        tree = []
        current = self.getnext(oid)
        while current['oid'].startswith(oid) and current['type'] not in [ASN1_NULL, ASN1_DECODING_ERROR]:
            tree.append(current)
            current = self.getnext(current['oid'])
        return tree

    def bulk(self, oid, num=10):
        tree = []
        p = SNMP(
            community=self.community,
            version=self.version,
            PDU=SNMPbulk(max_repetitions=num, varbindlist=[SNMPvarbind(oid=ASN1_OID(oid))])
        )
        r = self._sr(p).PDU.varbindlist
        for v in r:
            tree.append({'oid':v.oid.val, 'type':type(v.value), 'value':v.value.val})
        return tree


    def get(self, oid):
        p = SNMP(
            community=self.community,
            version=self.version,
            PDU=SNMPget(varbindlist=[SNMPvarbind(oid=ASN1_OID(oid))])
        )
        r = self._sr(p).PDU.varbindlist[0]
        return { 'oid' : r.oid.val, 'type' : type(r.value), 'value' : r.value.val }

    def set(self, oid, value):
        p = SNMP(
            community=self.community,
            version=self.version,
            PDU=SNMPset(varbindlist=[SNMPvarbind(oid=ASN1_OID(oid), value=value)])
        )
        self._sr(p)

    def setint(self, oid, value):
        if not isinstance(value, int):
            raise TypeError('Expected int got %s instead.' % type(value).__name__)
        self.set(oid, value)

    def setstr(self, oid, value):
        if not isinstance(value, basestring):
            value = str(value)
        self.set(oid, value)

    def setip(self, oid, value):
        if not isinstance(value, IPAddress) and not isinstance(value, ASN1_IPADDRESS):
            value = ASN1_IPADDRESS(str(IPAddress(value)))
        self.set(oid, value)

    def __del__(self):
        self.s.close()


class SNMPBruteForcer(object):

    def __init__(self, agent, port=161, version='v2c', timeout=0.5, rate=1000):
        self.version = SNMPVersion.iversion(version)
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.s.settimeout(timeout)
        self.addr = (agent, port)
        self.rate = rate

    def guess(self, communities):
        if 'public' not in communities:
            communities.append('public')
        if 'private' not in communities:
            communities.append('private')
        p = SNMP(
            version=self.version,
            PDU=SNMPget(varbindlist=[SNMPvarbind(oid=ASN1_OID('1.3.6.1.2.1.1.1.0'))])
        )
        r = []
        for c in communities:
            i = randint(0, 2147483647)
            p.PDU.id = i
            p.community = c
            self.s.sendto(str(p), self.addr)
            sleep(1/self.rate)
        while True:
            try:
                p = SNMP(self.s.recvfrom(65535)[0])
            except timeout:
                break
            r.append(p.community.val)
        return r

    def __del__(self):
        self.s.close()
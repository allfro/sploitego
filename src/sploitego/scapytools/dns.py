#!/usr/bin/env python

from struct import unpack, pack
import socket

from scapy.all import (   IP, ICMP, TCP, DNS, UDP, DNSQR, DNSgetstr, DNSRRField, DNSStrField, DNSRR,
                       ShortEnumField, IntField, ShortField, StrField, dnstypes, dnsclasses, RDataField, RDLenField,
                       RandShort)
from iptools.ip import resolvers


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ =[
    'nslookup',
    'inquery',
    'ixfr',
    'axfr'
]


def __decodeRR(self, name, s, p):
    ret = s[p:p+10]
    type,cls,ttl,rdlen = unpack("!HHIH", ret)
    p += 10

    rr = None
    if type == 15:
        rr = DNSMXRR("\x00"+ret+s[p:p+rdlen])
        rr.rdata = DNSgetstr(s, p+2)[0]
        rr.rdlen = rdlen
    elif type == 6:
        rr = DNSSOARR("\x00"+ret+s[p:p+rdlen])
        rr.mname, q = DNSgetstr(s, p)
        rr.rname, q = DNSgetstr(s, q)
        rr.serial,rr.refresh,rr.retry,rr.expire,rr.minimum = unpack('!IIIII', s[q:q+20])
        rr.rdlen = rdlen
    else:
        rr = DNSRR("\x00"+ret+s[p:p+rdlen])
        if 2 <= rr.type <= 5:
            rr.rdata = DNSgetstr(s, p)[0]
        del rr.rdlen

    p += rdlen

    rr.rrname = name
    return rr,p

DNSRRField.decodeRR = __decodeRR


class DNSMXRR(DNSRR):
    name = "DNS MX Resource Record"
    show_indent=0
    fields_desc = [ DNSStrField("rrname",""),
                    ShortEnumField("type", 1, dnstypes),
                    ShortEnumField("rclass", 1, dnsclasses),
                    IntField("ttl", 0),
                    RDLenField("rdlen"),
                    ShortField("mxpriority", 0),
                    RDataField("rdata", "", length_from=lambda pkt: pkt.rdlen - 2) ]


class DNSSOARR(DNSRR):
    name = "DNS SOA Resource Record"
    show_indent=0
    fields_desc = [ DNSStrField("rrname",""),
                    ShortEnumField("type", 1, dnstypes),
                    ShortEnumField("rclass", 1, dnsclasses),
                    IntField("ttl", 0),
                    ShortField("rdlen", 0),
                    StrField("mname", ""),
                    StrField("rname", ""),
                    IntField("serial", 0),
                    IntField("refresh", 0),
                    IntField("retry", 0),
                    IntField("expire", 0),
                    IntField("minimum", 0)]


def nslookup(qname, qtype='A', nameserver=resolvers(), rd=1, timeout=2, retry=2):

    if qtype in [ 'AXFR', 'IXFR' ]:
        ans = inquery(qname, 'SOA', nameserver, timeout=timeout, retry=retry)
        if ans is not None and ans.ancount:
            authns = [ a.mname for a in ans.an ]
            if qtype == 'AXFR':
                ans = axfr(qname, authns, timeout=timeout, retry=retry)
            else:
                ans = ixfr(qname, authns, timeout=timeout, retry=retry)
    else:
        ans = inquery(qname, qtype, nameserver, rd, timeout=timeout, retry=retry)

    return ans


def inquery(qname, qtype, nameserver, rd=1, timeout=2, retry=2):

    if not isinstance(nameserver, list):
        nameserver = [ nameserver ]

    s = socket.socket(type=socket.SOCK_DGRAM)
    s.settimeout(timeout)

    dnsq = DNS(id=RandShort(), rd=rd, qd=DNSQR(qname=qname, qtype=qtype))
    sendit = True
    id = 0

    for ns in nameserver:
        for r in range(0, retry+1):
            try:
                if sendit:
                    p = str(dnsq)
                    id = unpack('!H', p[0:2])[0]
                    s.sendto(p, 0, (ns, 53))
                dnsr = DNS(s.recvfrom(4096)[0])
                if id != dnsr.id:
                    sendit = False
                    continue
                return dnsr
            except socket.timeout:
                sendit = True
                continue
            except socket.error:
                sendit = True
                continue

    return None


def ixfr(qname, authnameserver, serial=0, refresh=0, retry_int=0, expiry=0, ttl=0, timeout=2, retry=2):
    soa = '\xc0\x0c\x00\x06\x00\x01\x00\x00\x00\x00\x00\x16\x00\x00'
    soa += pack('!IIIII', serial, refresh, retry_int, expiry, ttl)

    dnsq = DNS(id=RandShort(), rd=0, ra=0, nscount=1, qd=DNSQR(qname=qname, qtype='IXFR'))/soa
    return _dnsxfr(authnameserver, dnsq, timeout, retry)


def axfr(qname, authnameserver, timeout=2, retry=2):

    dnsq = DNS(id=RandShort(), rd=0, ra=0, qd=DNSQR(qname=qname, qtype='AXFR'))
    return _dnsxfr(authnameserver, dnsq, timeout, retry)


def _dnsxfr(authnameserver, packet, timeout=2, retry=2):

    if not isinstance(authnameserver, list):
        authnameserver = [ authnameserver ]

    for ns in authnameserver:
        for r in range(0, retry+1):
            s = socket.socket()
            s.settimeout(timeout)
            d = ''
            try:
                s.connect((ns, 53))
                s.sendall('%s%s' % (pack('!H', len(packet)), str(packet)))
                while True:
                    dr = s.recv(8192)
                    d += dr
            except socket.timeout:
                s.close()
                if d:
                    return _parsexfr(d)
                continue
            except socket.error:
                s.close()
                continue

    return []


def _parsexfr(xfr):
    i = 0
    ans = []
    while i < len(xfr):
        sz = unpack('!H', xfr[i:i+2])[0]
        i += 2
        ans.append(DNS(xfr[i:i+sz]))
        i += sz

    if len(ans) == 1:
        return ans[0]

    return ans
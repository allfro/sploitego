#!/usr/bin/env python
import collections

import socket

import dns.query
import dns.resolver
import dns.reversename
import dns.rdatatype

from canari.maltego.entities import DNSName, MXRecord, NSRecord, IPv4Address, Phrase
from canari.maltego.message import UIMessage, Field

from entities import IPv6Address


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'nslookup'
]


def xfr(ns, domain, response, type_='AXFR', fallback_to_ixfr=True, discovered_names=None):
    if discovered_names is None:
        discovered_names = []
    try:
        for msg in dns.query.xfr(ns, domain, type_):
            for ans in msg.answer:
                name = ans.name.to_text(True)
                if ans.rdtype in [1, 5] and name not in discovered_names:
                    discovered_names.append(name)
                    response += DNSName(domain if name == '@' else '.'.join([name, domain]))
    except dns.resolver.NXDOMAIN:
        response += UIMessage("DNS records for %s do not exist on %s." % (repr(domain), repr(ns)))
    except dns.resolver.Timeout:
        response += UIMessage("DNS request for %s timed out on %s." % (repr(domain), repr(ns)))
    except dns.exception.FormError:
        if type_ != 'IXFR' and fallback_to_ixfr:
            xfr(ns, domain, response, 'IXFR', discovered_names=discovered_names)
        else:
            response += UIMessage("Could not transfer DNS zone for %s from %s." % (repr(domain), repr(ns)))
    return discovered_names


def nslookup(name, type_, response, resolvers=None, recursive=True):
    name = name.rstrip('.')
    if isinstance(type_, basestring):
        type_ = dns.rdatatype.from_text(type_)
    if type_ == dns.rdatatype.PTR:
        name = dns.reversename.from_address(name)
    if not resolvers:
        resolvers = dns.resolver.get_default_resolver().nameservers
    elif isinstance(resolvers, basestring):
        resolvers = [resolvers]

    if type_ in [dns.rdatatype.AXFR, dns.rdatatype.IXFR]:
        try:
            discovered_names = []
            for ns in dns.resolver.query(name, dns.rdatatype.NS):
                xfr(ns.to_text(), name, response, discovered_names=discovered_names)
            return True
        except dns.resolver.NXDOMAIN:
            response += UIMessage("DNS records for %s do not exist." % repr(name))
        except dns.resolver.NoNameservers:
            response += UIMessage("No nameservers found for %s." % repr(name))
        except dns.resolver.Timeout:
            response += UIMessage("DNS request for %s timed out." % repr(name))
        except dns.resolver.NoAnswer:
            response += UIMessage("DNS request for %s resulted in no response." % repr(name))
        except socket.error:
            response += UIMessage("A socket error has occurred. Make sure you are connected or the traffic is allowed.")
        return False

    try:
        request = dns.message.make_query(name, type_, dns.rdataclass.IN)
        if not recursive:
            request.flags ^= dns.flags.RD
        for resolver in resolvers:
            ans = dns.query.udp(request, resolver).answer
            if ans:
                for rrset in ans:
                    for rr in rrset:
                        if rr.rdtype == type_:
                            if type_ == dns.rdatatype.A:
                                response += IPv4Address(rr.to_text(True))
                            elif type_ == dns.rdatatype.NS:
                                response += UIMessage(repr(rr))
                                response += NSRecord(rr.to_text()[:-1])
                            elif type_ == dns.rdatatype.CNAME:
                                response += DNSName(rr.to_text())
                            elif type_ == dns.rdatatype.SOA:
                                e = NSRecord(rr.mname.to_text(True))
                                e += Field('mailaddr', rr.rname.to_text(True), 'Authority')
                                response += e
                            elif type_ == dns.rdatatype.PTR:
                                response += DNSName(rr.to_text()[:-1])
                            elif type_ == dns.rdatatype.MX:
                                e = MXRecord(rr.exchange.to_text(True))
                                e.mxpriority = rr.preference
                                response += e
                            elif type_ == dns.rdatatype.TXT:
                                response += Phrase(rr.to_text(True))
                            elif type_ == dns.rdatatype.AAAA:
                                response += IPv6Address(rr.to_text(True))
                            else:
                                response += Phrase(rr.to_text(True))
                return True
    except dns.resolver.NXDOMAIN:
        response += UIMessage("DNS records for %s do not exist." % repr(name))
    except dns.resolver.Timeout:
        response += UIMessage("DNS request for %s timed out." % repr(name))
    except dns.resolver.NoNameservers:
        response += UIMessage("No name servers found for %s." % repr(name))
    except dns.resolver.NoAnswer:
        response += UIMessage("The DNS server returned with no response for %s." % repr(name))
    except socket.error:
        response += UIMessage("A socket error has occurred. Make sure you are connected or the traffic is allowed.")
    return False


def nslookup_raw(name, type_=dns.rdatatype.A, resolver=None, recursive=True, tcp=False):
    if not resolver:
        try:
            resolver = dns.resolver.get_default_resolver().nameservers.pop()
        except IndexError:
            raise OSError("A DNS resolver could not be found.")
    m = dns.message.make_query(name, type_, dns.rdataclass.IN)
    if not recursive:
        m.flags ^= dns.flags.RD
    if tcp:
        return dns.query.tcp(m, resolver)
    return dns.query.udp(m, resolver)
#!/usr/bin/env python

import socket

import dns.query
import dns.resolver
import dns.reversename

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


_names = []

def xfr(ns, domain, response, type='AXFR', fallback_to_ixfr=True):
    try:
        for msg in dns.query.xfr(ns, domain, type):
            for ans in msg.answer:
                name = ans.name.to_text()
                if ans.rdtype in [1, 5] and name not in _names:
                    _names.append(name)
                    response += DNSName(domain if name =='@' else '.'.join([name, domain]))
    except dns.resolver.NXDOMAIN:
        response += UIMessage("DNS records for %s do not exist on %s." % (repr(domain), repr(ns)))
    except dns.resolver.Timeout:
        response += UIMessage("DNS request for %s timed out on %s." % (repr(domain), repr(ns)))
    except dns.exception.FormError:
        if type != 'IXFR' and fallback_to_ixfr:
            xfr(ns, domain, response, 'IXFR')
        else:
            response += UIMessage("Could not transfer DNS zone for %s from %s." % (repr(domain), repr(ns)))


def nslookup(name, type, response, resolvers=None):

    name = name.rstrip('.')
    type = type.upper()
    resolver = None

    if type in ['AXFR', 'IXFR']:
        try:
            for ns in dns.resolver.query(name, 'NS'):
                xfr(ns.to_text().rstrip('.'), name, response)
        except dns.resolver.NXDOMAIN:
            response += UIMessage("DNS records for %s do not exist." % repr(name))
        except dns.resolver.Timeout:
            response += UIMessage("DNS request for %s timed out." % repr(name))
        except socket.error:
            response += UIMessage("A socket error has occurred. Make sure you are connected or the traffic is allowed.")
        return

    if resolvers is not None:
        if not isinstance(resolvers, list):
            raise ValueError('DNS resolvers must be a list of strings.')
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = resolvers
    else:
        resolver = dns.resolver.Resolver()

    if type == 'PTR':
        name = dns.reversename.from_address(name)

    try:
        ans = resolver.query(name, type, raise_on_no_answer=False)
        if ans.rrset is None:
            return
        for r in ans:
            if r.rdtype == 1 and type == 'A':
                response += IPv4Address(r.to_text())
            elif r.rdtype == 2 and type == 'NS':
                response += NSRecord(r.to_text().rstrip('.'))
            elif r.rdtype == 5 and type == 'CNAME':
                response += DNSName(r.to_text().rstrip('.'))
            elif r.rdtype == 6 and type == 'SOA':
                e = NSRecord(r.mname.to_text().rstript('.'))
                e += Field('mailaddr', r.rname.to_text().rstrip('.'), 'Authority')
                response += e
            elif r.rdtype == 12 and type == 'PTR':
                response += DNSName(r.to_text().rstrip('.'))
            elif r.rdtype == 15 and type == 'MX':
                e = MXRecord(r.exchange.to_text().rstrip('.'))
                e.mxpriority = r.preference
                response += e
            elif r.rdtype == 16 and type == 'TXT':
                response += Phrase(r.to_text())
            elif r.rdtype == 28 and type == 'AAAA':
                response += IPv6Address(r.to_text())
            else:
                response += Phrase(r.to_text())
    except dns.resolver.NXDOMAIN:
        response += UIMessage("DNS records for %s do not exist." % repr(name))
    except dns.resolver.Timeout:
        response += UIMessage("DNS request for %s timed out." % repr(name))
    except dns.resolver.NoAnswer:
        response += UIMessage("The DNS server returned with no response for %s." % repr(name))
    except socket.error:
        response += UIMessage("A socket error has occurred. Make sure you are connected or the traffic is allowed.")
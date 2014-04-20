# !/usr/bin/env python
from Queue import Queue
import re

from threading import Thread
from time import sleep
from uuid import uuid4

from canari.maltego.configuration import BuiltInTransformSets
from canari.maltego.entities import DNSName, Domain
from canari.maltego.message import UIMessage
from canari.maltego.utils import debug
from canari.framework import configure
from canari.config import config

import dns

from common.dnstools import nslookup_raw


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'onterminate',
    'dotransform'
]


class DNSResolver(Thread):
    def __init__(self, domain, queue_recv, queue_send, lookup_rate=None):
        super(DNSResolver, self).__init__()
        self.domain = domain
        self.lookup_rate = lookup_rate or config['dnsdiscovery/lookup_rate']
        self.queue_send = queue_send
        self.queue_recv = queue_recv

    def run(self):
        while True:
            subdomain = self.queue_recv.get()
            if not subdomain:
                break
            name = '%s.%s' % (subdomain, self.domain)
            name = re.sub('\.+', '.', name)
            # debug('Resolving name: %s' % name)
            try:
                msg = nslookup_raw(name)
                if msg.answer:
                    self.queue_send.put(msg)
            except dns.exception.Timeout:
                debug('Request timed out for name: %s' % name)
                pass
            sleep(1 / self.lookup_rate)
        self.queue_send.put(None)

def get_names(domain, msg):
    names = set([])
    if msg.answer:
        for rrset in msg.answer:
            name = rrset.name.to_text()[:-1]
            if rrset.name.to_text()[:-1].endswith(domain):
                names.add(name)
            for rr in rrset:
                cname = rr.to_text()[:-1]
                if rr.rdtype == dns.rdatatype.CNAME and cname.endswith(domain):
                    names.add(cname)
    return names


def get_ip_addresses(msg):
    return set([rr.to_text() for rrset in msg.answer for rr in rrset if rrset.rdtype == 1])


@configure(
    label='To DNS Names [Brute Force]',
    description='This transform attempts to find subdomains using brute-force with a custom word list.',
    uuids=['sploitego.v2.DomainToDNSName_BruteForce'],
    inputs=[( BuiltInTransformSets.DNSFromIP, Domain )],
)
def dotransform(request, response):

    domain = request.value
    wildcard_ips = set()
    found_subdomains = {}

    try:
        msg = nslookup_raw('%s.%s' % (str(uuid4()), domain))
        if msg.answer:
            wildcard_ips = get_ip_addresses(msg)
            name = '*.%s' % domain
            response += DNSName(name)
            found_subdomains[name] = 1
    except dns.exception.Timeout:
        pass

    if wildcard_ips:
        warning = 'Warning: wildcard domain is defined... results may not be accurate'
        debug(warning)
        response += UIMessage(warning)

    ncount = 0
    nthreads = config['dnsdiscovery/numthreads']
    subdomains = set(config['dnsdiscovery/wordlist'])

    threads = []
    queue_send = Queue()
    queue_recv = Queue()
    for i in range(0, nthreads):
        t = DNSResolver(request.value, queue_send, queue_recv)
        t.start()
        threads.append(t)

    for s in subdomains:
        queue_send.put(s)

    for i in range(0, nthreads):
        queue_send.put(None)

    while True:
        msg = queue_recv.get()
        if not msg:
            ncount += 1
            if ncount == nthreads:
                break
        elif msg.answer:
            ips = get_ip_addresses(msg)
            if wildcard_ips and wildcard_ips.issuperset(ips):
                continue
            for name in get_names(domain, msg):
                if name in found_subdomains:
                    continue
                else:
                    found_subdomains[name] = 1
                    response += DNSName(name)

    for t in threads:
        t.join()
    return response
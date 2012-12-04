#!/usr/bin/env python

from threading import Thread
from Queue import Queue
from time import sleep
from uuid import uuid4



from canari.maltego.configuration import BuiltInTransformSets
from canari.maltego.entities import DNSName, Domain
from sploitego.scapytools.dns import nslookup
from canari.maltego.message import UIMessage
from canari.maltego.utils import debug
from canari.framework import configure
from canari.config import config
from scapy.all import DNS


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
    def __init__(self, *args):
        self.domain = args[0]
        self.lookup_rate = config['dnsdiscovery/lookup_rate']
        super(DNSResolver, self).__init__()

    def run(self):
        while True:
            subdomain = q.get()
            if subdomain is None:
                break
            ans = nslookup('%s.%s' % (subdomain, self.domain))
            if ans is not None and DNS in ans and ans[DNS].ancount:
                qret.put(ans[DNS])
            sleep(1/self.lookup_rate)
        qret.put(None)


def getnames(domain, dnsr):
    names = set([])
    if dnsr[DNS].ancount:
        names.add(dnsr[DNS].qd.qname[:-1])
        for i in range(0, dnsr[DNS].ancount):
            if dnsr[DNS].an[i].type == 5 and dnsr[DNS].an[i].rdata[:-1].endswith(domain):
                names.add(dnsr[DNS].an[i].rdata[:-1])
    return names


def getips(dnsr):
    return set([
        dnsr[DNS].an[i].rdata for i in range(0, dnsr.ancount)
        if dnsr[DNS].an[i].type == 1
    ])


@configure(
    label='To DNS Names [Brute Force]',
    description='This transform attempts to find subdomains using brute-force with a custom word list.',
    uuids=[ 'sploitego.v2.DomainToDNSName_BruteForce' ],
    inputs=[ ( BuiltInTransformSets.DNSFromIP, Domain ) ],
)
def dotransform(request, response):

    domain = request.value

    global q
    global qret
    q = Queue()
    qret = Queue()

    ans = nslookup('%s.%s' % (str(uuid4()), domain))
    wcip = getips(ans)
    foundsds = {}
    if wcip:
        response += UIMessage('Warning: wildcard domain is defined... results may not be accurate')

    ncount = 0
    nthreads = config['dnsdiscovery/numthreads']
    subdomains = config['dnsdiscovery/wordlist']

    threads = []
    for i in range(0, nthreads):
        t = DNSResolver(request.value)
        t.start()
        threads.append(t)

    for sd in subdomains:
        q.put(sd)

    for i in range(0, nthreads):
        q.put(None)

    while True:
        r = qret.get()
        if r is None:
            ncount += 1
            if ncount == nthreads:
                break
        else:
            names = getnames(domain, r)
            ips = getips(r)
            if wcip and wcip.issuperset(ips):
                continue
            for name in names:
                if name in foundsds:
                    continue
                else:
                    foundsds[name] = 1
                    response += DNSName(name)

    for t in threads:
        t.join()
    return response


def onterminate(*args):
    debug('Terminated.')
    exit(-1)
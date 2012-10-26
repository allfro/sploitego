#!/usr/bin/env python

from xml.etree.cElementTree import fromstring

from scapy.all import arping, sr, sr1, TCP, IP, ICMP, sniff, ARP
from canari.maltego.message import Field, MaltegoException
from sploitego.scapytools.route import route, traceroute2
from canari.framework import configure, superuser
from canari.maltego.entities import IPv4Address
from iptools.ip import IPNetwork, IPAddress
from canari.maltego.utils import debug
from canari.config import config
from iptools.arin import whoisip


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


@superuser
@configure(
    label='To Neighbors [Active Scan]',
    description='This transform attempts to identify hosts that are directly attached to the same router as the target',
    uuids=[ 'sploitego.v2.IPv4AddressToNeighbors_ActiveScan' ],
    inputs=[ ( "Reconnaissance", IPv4Address ) ],
)
def dotransform(request, response):
    r = route(request.value)
    if r is None:
        raise MaltegoException('Network is unavailable')
    elif not r['nexthop']:
        return findlocalneighbors(r['network'], response)
    return findremoteneighbors(IPAddress(request.value), response)


def findlocalneighbors(network, response):

    debug('ARP sweeping %s' % network.netblock)
#    e = Netblock(network.netblock)
#    e += Label('CIDR Notation', repr(network))
#    e += Label('Network Mask', network.netmask)
#    e += Label('Number of Hosts', int(~network.netmask) - 1)
#    response += e

    ans = arping(
        repr(network),
        timeout=config['scapy/sr_timeout'],
        verbose=config['scapy/sr_verbose']
    )[0]

    for i in ans:
        e = IPv4Address(i[1].psrc)
        e.internal = True
        e += Field('ethernet.hwaddr', i[1].hwsrc, displayname='Hardware Address')
        response += e

    if len(ans) <= 1:
        passivescan(network, response)

    return response


def passivescan(network, response):

    nodes = {}
    debug('Sniffing network traffic for more hosts.')
    ans = sniff(count=config['scapy/sniffcount'], timeout=config['scapy/snifftimeout'])
    debug('Analyzing traffic.')
    for i in ans:
        src = None
        dst = None
        if IP in i:
            src = i[IP].src
            dst = i[IP].dst
        elif ARP in i:
            src = i[ARP].psrc
            dst = i[ARP].pdst
        else:
            continue

        if src in network and src not in nodes:
            nodes[src] = True
            e = IPv4Address(src, internal=True)
            e += Field('ethernet.hwaddr', i.src, displayname='Hardware Address')
            response += e

        if dst in network and dst not in nodes and i.dst != 'ff:ff:ff:ff:ff:ff':
            nodes[dst] = True
            e = IPv4Address(dst, internal=True)
            e += Field('ethernet.hwaddr', i.dst, displayname='Hardware Address')
            response += e


def findremoteneighbors(ip, response):

    debug('Doing an ARIN whois lookup...')
    w = fromstring(whoisip(ip, accept='application/xml'))
    network = IPNetwork([
        w.find('{http://www.arin.net/whoisrws/core/v1}startAddress').text,
        w.find('{http://www.arin.net/whoisrws/core/v1}endAddress').text
    ])

#    e = Netblock(network.netblock)
#    e += Label('CIDR Notation', repr(network))
#    e += Label('Network Mask', network.netmask)
#    e += Label('Number of Hosts', int(~network.netmask) - 1)
#    response += e

    if network.cidrlen < 24:
        debug('According to ARIN, the CIDR length is %d, reducing it to 24 for the scan...' % network.cidrlen)
        network.netblock = '%s/24' % ip

    debug('Probing the host on TCP ports 0-1024...')
    r = sr1(
        IP(dst=str(ip))/TCP(dport=(0,1024)),
        timeout=config['scapy/sr_timeout'],
        verbose=config['scapy/sr_verbose'],
        retry=config['scapy/sr_retries']
    )

    if r is not None and r.src == ip:
        dport = r.sport

        debug('Performing a traceroute to destination %s' % ip)
        ans = traceroute2(
            str(ip),
            TCP(dport=dport),
            timeout=config['scapy/sr_timeout'],
            verbose=config['scapy/sr_verbose'],
            retry=config['scapy/sr_retries']
        )

        l_hop = ans[-1]
        sl_hop = ans[-2]

        if sl_hop['ttl'] != l_hop['ttl'] - 1:
            debug(
                "It takes %d hops to get to %s but we could only find the router at hop %d (%s)." %
                (l_hop['ttl'], ip, sl_hop['ttl'], sl_hop['ip'])
            )
            debug("Can't find second last hop... aborting...")
        else:
            debug('It takes %d hops to get to %s and it is attached to router %s...' % (l_hop['ttl'], ip, sl_hop['ip']))
            debug('Sending probe packets to %s with ttl %d...' % (network, sl_hop['ttl']))

            ans = sr(
                IP(dst=repr(network), ttl=sl_hop['ttl'])/TCP(dport=dport),
                timeout=config['scapy/sr_timeout'],
                verbose=config['scapy/sr_verbose'],
                retry=config['scapy/sr_retries']
            )[0]

            for r in ans:
                if r[1].src == sl_hop['ip']:
                    debug('%s is attached to the same router...' % r[0].dst)

                    e = IPv4Address(r[0].dst)

                    alive = sr1(
                        IP(dst=r[0].dst)/TCP(dport=dport),
                        timeout=config['scapy/sr_timeout'],
                        verbose=config['scapy/sr_verbose'],
                        retry=config['scapy/sr_retries']
                    )

                    if alive is not None:
                       e += Field('alive', 'true')
                    response += e

    return response
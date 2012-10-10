#!/usr/bin/env python

from scapy.all import sr, sr1, conf, IP
from iptools.ip import IPNetwork, IPAddress


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'route',
    'traceroute',
    'traceroute2'
]


def route(ip):

    routes = [ {
        'network' : IPNetwork([r[0], r[1]]),
        'nexthop' : IPAddress(r[2]),
        'iface' : r[3],
        'iface_ip' : IPAddress(r[4])
    } for r in conf.route.routes ]

    routes.sort(key=lambda r: r['network'])

    for r in routes:
        if r['network'].cidrlen != 32 and ip in r['network']:
            return r


def traceroute(dst, probe, ttl=(0, 255), timeout=2, retry=2, verbose=0):
    return sr(IP(dst=dst, ttl=ttl)/probe, timeout=timeout, retry=retry, verbose=verbose)[0]


def traceroute2(dst, probe, timeout=2, retry=2, verbose=0):
    hops = []
    for i in range(1, 256):
        r = sr1(IP(dst=dst, ttl=i)/probe, timeout=timeout, retry=retry, verbose=verbose)
        if r is not None:
            hops.append({ 'ttl' : i, 'ip' : r.src })
        else:
            continue
        if r.src == dst:
            break
    return hops
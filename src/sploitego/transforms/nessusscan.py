#!/usr/bin/env python

from time import sleep

from sploitego.maltego.message import Domain, IPv4Address
from common.nessus import scan, login, policy
from sploitego.framework import configure
from common.entities import NessusReport

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


@configure(
    label='To Nessus Report [Nessus]',
    description='This transform performs a Nessus scan on a host.',
    uuids=['sploitego.v2.DomainToNessusReport_Nessus', 'sploitego.v2.IPv4AddressToNessusReport_Nessus'],
    inputs=[('Scanning', Domain), ('Scanning', IPv4Address)],
    debug=False
)
def dotransform(request, response):
    ns = login()
    p = policy(ns)
    r = scan(ns, request.value, p).report
    while r.status != 'completed':
        sleep(1)
    nr = NessusReport(r.name)
    nr.uuid = r.uuid
    response += nr
    return response


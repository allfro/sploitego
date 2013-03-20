#!/usr/bin/env python

from common.entities import Port, NessusVulnerability
from canari.framework import configure
from common.tenable import login
from nessus import Report


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.2'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'dotransform'
]


@configure(
    label='To Ports [Nessus]',
    description='This transform retrieves all the ports associated with a given vulnerability.',
    uuids=['sploitego.v2.NessusVulnerabilityToPorts_Nessus'],
    inputs=[('Scanning', NessusVulnerability)],
    debug=False
)
def dotransform(request, response):
    s = login(host=request.fields['nessus.server'], port=request.fields['nessus.port'])
    if s is None:
        return response
    vulns = Report(s, request.fields['nessusreport.uuid'], '').vulnerabilities
    for h in vulns[request.fields['nessusplugin.id']].hosts:
        p = Port(h.port)
        p.destination = h.name
        p.status = 'Open'
        p.protocol = h.protocol
        response += p
    return response
#!/usr/bin/env python

from common.entities import NessusVulnerability, NessusReport
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
    label='To Vulnerabilities [Nessus]',
    description='This transform returns the list of discovered vulnerabilities.',
    uuids=['sploitego.v2.NessusReportToVulnerabilities_Nessus'],
    inputs=[('Scanning', NessusReport)],
    debug=False
)
def dotransform(request, response):
    s = login(host=request.fields['nessus.server'], port=request.fields['nessus.port'])
    if s is None:
        return response
    vulns = Report(s, request.fields['nessusreport.uuid'], request.value).vulnerabilities
    for k in vulns:
        v = vulns[k]
        e = NessusVulnerability(v.name, weight=v.count)
        e.severity = v.severity
        e.pluginid = v.id
        e.count = v.count
        e.family = v.family
        e.uuid = v.uuid
        e.server = s.server
        e.port = s.port
        response += e
    return response


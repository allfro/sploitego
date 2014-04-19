#!/usr/bin/env python

from nessus import Report, ReportFilter, ReportFilterQuery
from canari.resource import icon_resource
from canari.maltego.message import Field
from canari.framework import configure


from common.entities import NessusVulnerability, NessusReport
from common.tenable import login


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
    label='To Metasploitable [Nessus]',
    description='This transform returns the list of discovered vulnerabilities that have exploits available in Metasploit.',
    uuids=['sploitego.v2.NessusReportToMetasploitable_Nessus'],
    inputs=[('Scanning', NessusReport)],
    debug=False
)
def dotransform(request, response):
    s = login()
    if s is None:
        return response

    vulns = Report(s, request.entity.uuid, request.value).search(
        ReportFilterQuery(
            ReportFilter(
                'exploit_framework_metasploit',
                'eq',
                'true'
            )
        )
    )

    for k, v in vulns.iteritems():
        e = NessusVulnerability(v.name, weight=v.count)
        e.severity = v.severity
        e.iconurl = icon_resource('logos/metasploit.png')
        e.pluginid = v.id
        e.count = v.count
        e.family = v.family
        e.uuid = v.uuid
        e.server = s.server
        e.port = s.port
        e += Field('metasploit_name', v.hosts[0].details[0].output['metasploit_name'], displayname='Metasploit Name')
        response += e
    return response


# !/usr/bin/env python

from nessus import Report
from canari.resource import icon_resource
from canari.framework import configure

from common.entities import NessusVulnerability, MetasploitSession
from common.tenable import login as nessus_login
from common.msfrpcd import login as metasploit_login


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
    label='To Session [Metasploit]',
    description='This transform returns a Metasploit session if successful.',
    uuids=['sploitego.v2.NessusVulnToMetasploitSession_Metasploit'],
    inputs=[('Exploitation', NessusVulnerability)],
    debug=False
)
def dotransform(request, response):
    from sploitego.msftools.exploit import launch

    s = nessus_login(host=request.entity.server, port=request.entity.port)
    if s is None:
        return response
    m = metasploit_login()
    if m is None:
        return response

    vulns = Report(s, request.entity.uuid, '').vulnerabilities
    for h in vulns[request.entity.pluginid].hosts:
        session = launch(m, {'RPORT': int(h.port), 'RHOST': h.name}, filter_=request.fields.get('metasploit_name'))

        if session != -1:
            e = MetasploitSession('%s:%s' % (h.name, h.port))
            e.sessionid = session
            e.server = m.server
            e.port = m.port
            e.uri = m.uri
            e.iconurl = icon_resource('logos/terminal.png')
            response += e
        break

    return response


#!/usr/bin/env python
import os
import subprocess
from canari.commands.common import get_bin_dir

from canari.framework import configure

from common.entities import MetasploitSession


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
    label='To Shell [Metasploit]',
    description='This transform returns a Metasploit shell if successful.',
    uuids=['sploitego.v2.MetasploitSessionToShell_Metasploit'],
    inputs=[('Exploitation', MetasploitSession)],
    debug=False
)
def dotransform(request, response):
    script = os.path.join(get_bin_dir(), 'qtmsfconsole')
    subprocess.Popen(
        [
            script,
            request.entity.server,
            request.entity.port,
            request.entity.uri,
            request.entity.uuid
        ]
    )
    return response


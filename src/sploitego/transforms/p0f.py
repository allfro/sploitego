#!/usr/bin/env python

from canari.maltego.entities import BuiltWithTechnology, IPv4Address
from sploitego.cmdtools.p0f import fingerprint, P0fStatus
from canari.framework import configure, superuser


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'dotransform',
    'onterminate'
]

@superuser
@configure(
    label='To Technology [P0f]',
    description='This transform queries the P0f API for an OS fingerprint.',
    uuids=['sploitego.v2.IPv4AddressToTechnology_P0f'],
    inputs=[('Reconnaissance', IPv4Address)],
)
def dotransform(request, response):
    i = fingerprint(request.value)
    if i['status'] == P0fStatus.OK and i['os_name']:
        d = '%s %s' % (i['os_name'], i['os_flavor'])
        if i['http_name']:
            d = '%s (%s)' % (i['http_name'], d)
        response += BuiltWithTechnology(d)
    return response
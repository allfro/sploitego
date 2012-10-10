#!/usr/bin/env python

from urllib import urlopen

from canari.maltego.entities import Website, DNSName
from sploitego.webtools.thumbnails import thumbnail
from canari.maltego.message import UIMessage
from canari.framework import configure

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


@configure(
    label='To Web site [Query Ports 80]',
    description='This transform queries port 80 for websites',
    uuids=[ 'sploitego.v2.DNSNameToWebsite_QueryPorts' ],
    inputs=[ ( None, DNSName ) ],
)
def dotransform(request, response):
    try:
        url = 'http://%s' % request.value
        urlopen(url)
        response += Website(request.value, iconurl=thumbnail(url))
    except IOError, ioe:
        response += UIMessage(str(ioe))
    return response
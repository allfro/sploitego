#!/usr/bin/env python

from sploitego.webtools.bluecoat import sitereview
from sploitego.maltego.message import Website
from sploitego.framework import configure
from common.entities import SiteCategory

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'dotransform'
]


@configure(
    label='To Site Category [Blue Coat]',
    description='Gets the site category for a given Website.',
    uuids=[ 'sploitego.v2.WebsiteToSiteCategory_BlueCoat' ],
    inputs=[ ( 'Reconnaissance', Website ) ]
)
def dotransform(request, response):
    for c in sitereview(request.value):
        response += SiteCategory(c)
    return response
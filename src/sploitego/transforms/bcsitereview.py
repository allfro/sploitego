#!/usr/bin/env python

from canari.maltego.entities import Website
from common.entities import SiteCategory
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
    'dotransform'
]


@configure(
    label='To Site Category [Blue Coat]',
    description='Gets the site category for a given Website.',
    uuids=[ 'sploitego.v2.WebsiteToSiteCategory_BlueCoat' ],
    inputs=[ ( 'Reconnaissance', Website ) ],
    remote=True
)
def dotransform(request, response):
    from sploitego.webtools.bluecoat import sitereview
    for c in sitereview(request.value):
        response += SiteCategory(c)
    return response
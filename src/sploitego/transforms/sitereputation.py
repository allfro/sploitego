#!/usr/bin/env python

from sploitego.webtools.aceinsights import AceInsightMiner, Miner
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
    label='To Site Category [Websense]',
    description='Gets the site category for a given Website.',
    uuids=[ 'sploitego.v2.WebsiteToSiteCategory_Websense' ],
    inputs=[ ( 'Reconnaissance', Website ) ],
    remote=True
)
def dotransform(request, response):
    ac = AceInsightMiner(request.value)
    r = ac.getdata(Miner.WebsenseCategory)
    if r is not None:
        if 'static_category_name' in r:
            response += SiteCategory(r['static_category_name'])
        elif 'realtime_category_name' in r:
            response += SiteCategory(r['realtime_category_name'])
    return response

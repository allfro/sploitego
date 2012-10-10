#!/usr/bin/env python

from httplib import urlsplit
from re import findall

from canari.maltego.configuration import BuiltInTransformSets
from canari.maltego.entities import DNSName, Domain
from sploitego.webtools.bing import searchweb
from canari.framework import configure
from canari.config import config


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
    label='To DNS Names [Bing]',
    description='This transform attempts to find subdomains using the Microsoft Bing search engine.',
    uuids=[ 'sploitego.v2.DomainToDNSName_Bing' ],
    inputs=[ ( BuiltInTransformSets.DNSFromDomain, Domain ) ]
)
def dotransform(request, response):
    domain = request.value
    exclude = set()
    for i in range(0, config['bingsubdomains/maxrecursion']):
        q = ' '.join(['site:%s' % domain] + map(lambda x: '-site:%s' % x, exclude))
        results = searchweb(q)
        for r in results:
            domains = [ urlsplit(d).netloc for d in findall('<web:Url>(.+?)</web:Url>', r) ]
            for d in domains:
                if d not in exclude and d != domain:
                    exclude.add(d)
                    response += DNSName(d)
    return response
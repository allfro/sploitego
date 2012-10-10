#!/usr/bin/env python

from httplib import HTTPConnection
from urllib import urlencode

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
    'searchweb'
]


def searchweb(query, content_type='xml'):
    if content_type not in ['xml', 'json']:
        raise ValueError('Invalid content type requested: %s' % content_type)

    maxpages = config['bing/maxpages']
    appid = config['bing/appid']
    c = HTTPConnection('api.bing.net')
    params = {'Appid': appid, 'query': query, 'sources': 'web', 'web.count': 50, 'web.offset' : 0}


    pages = []
    for i in range(0, maxpages):
        c.request('GET', '/%s.aspx?%s' % (content_type, urlencode(params)))
        r = c.getresponse()

        if r.status == 200:
            pages.append(r.read())

        params['web.offset'] += 50

    return pages

#!/usr/bin/env python

from xml.etree.cElementTree import fromstring
from urllib import urlopen
import os
from json import loads, dumps

from canari.utils.fs import fsemaphore, age, cookie
from canari.utils.wordlist import wordlist


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'sitereview'
]


def updatelist(filename):
    d = None
    with fsemaphore(filename, 'wb') as f:
        f.lockex()
        try:
            categories = wordlist(
                'http://sitereview.bluecoat.com/rest/categoryList?alpha=true',
                loads
            )
            d = dict([('%02x' % c['num'], c['name']) for c in categories])
            f.write(dumps(d))
        except Exception, e:
            f.close()
            os.unlink(tmpfile)
            raise e
    return d


def readlist(filename):
    with fsemaphore(filename) as f:
        f.locksh()
        data = wordlist('file://%s' % filename, loads)
    return data


tmpfile = cookie('sploitego.bluecoat.tmp')


def _chunks(s):
    return [s[i:i + 2] for i in range(0, len(s), 2)]


def sitereview(site, config, port=80):
    categories = None
    if not os.path.exists(tmpfile) or age(tmpfile) >= config['cookie/maxage']:
        categories = updatelist(tmpfile)
    else:
        categories = readlist(tmpfile)

    r = urlopen(
        'http://sp.cwfservice.net/1/R/%s/K9-00006/0/GET/HTTP/%s/%s///' % (config['bluecoat/license'], site, port)
    )

    if r.code == 200:
        e = fromstring(r.read())
        domc = e.find('DomC')
        dirc = e.find('DirC')
        if domc is not None:
            cats = _chunks(domc.text)
            return [categories.get(c, 'Unknown') for c in cats]
        elif dirc is not None:
            cats = _chunks(dirc.text)
            return [categories.get(c, 'Unknown') for c in cats]
    return []

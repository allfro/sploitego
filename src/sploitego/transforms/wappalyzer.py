#!/usr/bin/env python

from sploitego.framework import configure
from sploitego.maltego.message import URL, BuiltWithTechnology, Field
from sploitego.webtools.wappalyzer import Wappalyzer

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = ['Inspired by Wappalyzer (http://wappalyzer.com)']

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'dotransform'
]

@configure(
    label='To BuiltWith [Wappalyzer]',
    description='This transform will attempt to fingerprint the URLs application stack',
    uuids=['sploitego.v2.URLToBuiltWith_Wappalyzer'],
    inputs=[('Reconnaissance', URL)],
    debug=True
)
def dotransform(request, response):
    r = Wappalyzer().analyze(request.value)
    for i in r:
        e = BuiltWithTechnology(i)
        e += Field('categories', ', '.join(r[i]))
        response += e
    return response
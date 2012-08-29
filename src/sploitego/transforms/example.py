#!/usr/bin/env python

from sploitego.maltego.message import Person, Phrase
from sploitego.maltego.utils import debug, progress
from sploitego.framework import superuser, configure

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
    label='To Phrase [Hello World]',
    description='Returns a phrase entity with the phrase "Hello Word!"',
    uuids=[ 'sploitego.v2.PersonToPhrase_HelloWorld' ],
    inputs=[ ( 'Useless', Person ) ],
    debug=True
)
def dotransform(request, response):
    progress(50)
    debug('This was pointless!')
    progress(100)
    return response + Phrase('Hello %s' % request.value)


def onterminate():
    debug('Caught signal... exiting.')
    exit(0)
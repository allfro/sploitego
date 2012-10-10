#!/usr/bin/env python

from json.decoder import JSONDecoder

from canari.maltego.message import UIMessage, Label
from sploitego.webtools.pipl import pipljsonsearch
from canari.maltego.entities import Person
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
    label='To Related People [Pipl]',
    description="This transform attempts to find people related to the person in question.",
    uuids=[ 'sploitego.v2.PersonToRelatedPeople_Pipl' ],
    inputs=[ ( 'Relationships From Person', Person ) ],
)
def dotransform(request, response):
    p = JSONDecoder().decode(
        pipljsonsearch(
            first_name=request.fields['firstname'],
            last_name=request.fields['lastname']
        )
    )

    if 'error' in p:
        response += UIMessage(p['error'])

    for r in p['results']['records']:
        if 'relationships' in r:
            for rel in r['relationships']:
                e = Person(rel['name']['display'])
                e += Label(
                    'Source', '<a href="%s">%s</a>' % (r['source']['url'], r['source']['@ds_name']), type='text/html'
                )
                response += e

    return response
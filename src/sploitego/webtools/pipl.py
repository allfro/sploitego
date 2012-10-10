#!/usr/bin/env python

from urllib import urlencode, urlopen

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
    'PiplSearchError',
    'PiplSearchType',
    'PiplPeopleMode',
    'piplsearch',
    'piplxmlsearch',
    'pipljsonsearch'
]


class PiplSearchError(Exception):
    pass


class PiplSearchType(object):
    XML = "xml"
    JSON = "json"


class PiplPeopleMode(object):
    All = "all"
    One = "one"


def piplsearch(**kwargs):

    type = kwargs.get('type', PiplSearchType.XML)

    if type not in [PiplSearchType.JSON, PiplSearchType.XML]:
        raise PiplSearchError("Search type must be either 'json' or 'xml' not '%s'." % type)

    d = {
        'exact_name': kwargs.get('exact_name', 0),
        'no_sponsored': kwargs.get('no_sponsored', 1),
        'person_mode': kwargs.get('person_mode', PiplPeopleMode.All),
        'key': config['pipl/apikey']
    }

    if d['key'] is None:
        raise PiplSearchError('You need an API key to search Pipl.')

    if d['person_mode'] not in [PiplPeopleMode.All, PiplPeopleMode.One]:
        raise PiplSearchError("Person search mode must be either 'all' or 'one' not '%s'." % d['person_mode'])

    if 'country' in d and len(d['country']) != 2:
        raise PiplSearchError("Country must be a two letter country code.")

    if 'state' in d and len(d['state']) != 2:
        raise PiplSearchError("State/province must be a two letter state code.")

    params = [
        'first_name','middle_name','last_name','country','state',
        'city','from_age','to_age','email','phone','username','tag'
    ]

    for k in kwargs:
        if k in params and kwargs[k] is not None:
            d[k] = kwargs[k]

    url = 'http://apis.pipl.com/search/v2/%s/?%s' % (type, urlencode(d))

    r = urlopen(url)

    return r.read()


def piplxmlsearch(**kwargs):
    kwargs.update({'type':'xml'})
    return piplsearch(**kwargs)


def pipljsonsearch(**kwargs):
    kwargs.update({'type':'json'})
    return piplsearch(**kwargs)
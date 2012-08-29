#!/usr/bin/env python

from urllib2 import urlopen, quote, Request, HTTPError

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'ARINSearchError',
    'whois',
    'textwhois',
    'xmlwhois',
    'jsonwhois',
    'htmlwhois',
    'whoisorg',
    'whoisnet',
    'whoispoc',
    'whoisasn',
    'whoiscustomer',
    'whoisrdns',
    'whoisip',
    'whoiscidr'
]


_resource_qualifiers = {
    'poc' : ['orgs', 'asns', 'nets'],
    'org' : ['pocs', 'asns', 'nets'],
    'asn' : ['pocs'],
    'net' : ['pocs', 'parent', 'children', 'rdns'],
    'rdns' : ['nets'],
    'ip' : [],
    'cidr' : ['more', 'less'],
    'customer': []
}


_matrix_parameters = {
    'orgs' : ['handle', 'name', 'dba', 'q'],
    'customers' : ['handle', 'name', 'q'],
    'pocs' : ['handle', 'domain', 'first', 'middle', 'last', 'company', 'city', 'q'],
    'asns' : ['handle', 'name', 'q'],
    'nets' : ['handle', 'name', 'q']
}


_query_parameters = [
    'showDetails',
    'showPocs',
    'showARIN'
]


_accept_types = [
    'text/plain',
    'text/html',
    'application/json',
    'application/xml'
]


class ARINSearchError(Exception):
    pass


def whois(resource, handle=None, qualifier=None, query_params=None, matrix_params=None, accept='text/plain'):
    url = 'http://whois.arin.net/rest/'

    if handle is not None:
        if resource not in _resource_qualifiers.keys():
            raise ValueError("Invalid resource type: '%s' not in %s" % (resource, _resource_qualifiers.keys()))

        url += '%s/%s' % (resource, quote(handle.strip(' ')))

        if qualifier is not None:
            if qualifier not in _resource_qualifiers[resource]:
                raise ValueError("Invalid resource type qualifier: '%s' not in %s" % (qualifier, _resource_qualifiers[resource]))

            url += '/%s' % qualifier

    else:
        if resource not in _matrix_parameters.keys():
            raise ValueError("Invalid resource type: '%s' not in %s" % (resource, _matrix_parameters.keys()))

        url += '%s' % resource

        if matrix_params is not None:
            if not set(matrix_params).issubset(_matrix_parameters[resource]):
                diff = ', '.join(set(matrix_params).difference(_matrix_parameters[resource]))
                raise ValueError("Invalid matrix parameter(s): '%s' not in %s" % (diff, _matrix_parameters[resource]))

            url += ';' +  ';'.join(map(lambda r: '%s=%s' % (r, matrix_params[r]), matrix_params))

    if query_params is not None:
        if not set(query_params).issubset(_query_parameters):
            diff = ', '.join(set(query_params).difference(_query_parameters))
            raise ValueError("Invalid query parameter(s): '%s' not in %s" % (diff, _query_parameters))

        url += '?' + '&'.join(map(lambda p: '%s=%s' % (p, query_params[p]), query_params))


    if accept not in _accept_types:
        raise ValueError("Invalid 'Accept' type: '%s' not in %s" % (accept, _accept_types))

    r = Request(
        url,
        headers={'Accept':accept}
    )

    try:
        return urlopen(r).read()
    except HTTPError, e:
        raise ARINSearchError('Invalid search: %s (reason: %s)' % (url, e))


textwhois = whois


def xmlwhois(resource, **kwargs):
    return whois(resource, accept='application/xml', **kwargs)


def jsonwhois(resource, **kwargs):
    return whois(resource, accept='application/json', **kwargs)


def htmlwhois(resource, **kwargs):
    return whois(resource, accept='text/html', **kwargs)


def whoisorg(org, **kwargs):
    return whois('org', handle=org, **kwargs)


def whoisnet(net, **kwargs):
    return whois('net', handle=net, **kwargs)


def whoispoc(poc, **kwargs):
    return whois('poc', handle=poc, **kwargs)


def whoisasn(asn, **kwargs):
    return whois('asn', handle=asn, **kwargs)


def whoiscustomer(customer, **kwargs):
    return whois('customer', handle=customer, **kwargs)


def whoisrdns(rdns, **kwargs):
    return whois('rdns', handle=rdns, **kwargs)


def whoisip(ip, **kwargs):
    return whois('ip', handle=str(ip), **kwargs)


def whoiscidr(cidr, **kwargs):
    return whois('cidr', handle=cidr, **kwargs)
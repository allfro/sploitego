#!/usr/bin/env python

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'privileged',
    'specification'
]


def superuser(f):
    f.privileged = True
    return f


class configure(object):

    def __init__(self, **kwargs):
        diff = set(['label', 'uuids', 'inputs']).difference(kwargs)
        if diff:
            raise TypeError('Missing transform specification properties: %s' % ', '.join(diff))
        if not isinstance(kwargs['uuids'], list):
            raise TypeError('Expected type list (got %s instead)' % type(kwargs['uuids']).__name__)
        if not isinstance(kwargs['inputs'], list):
            raise TypeError('Expected type list (got %s instead)' % type(kwargs['inputs']))
        kwargs['description'] = kwargs.get('description', '')
        kwargs['debug'] = kwargs.get('debug', False)
        self.specification = kwargs

    def __call__(self, f):
        f.__dict__.update(self.specification)
        return f

#!/usr/bin/env python

from xml.etree import cElementTree as cET
from re import sub, findall, search

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'objectify',
    'stripns'
]


class PoliteObject(list):
    pass

PoliteObject.__getattr__ = lambda self, key: PoliteObject()


def hasattr(obj, key):
    try:
        obj.__getattribute__(key)
        return True
    except AttributeError:
        return False


def stripns(text):
    ns = findall('xmlns:?([^=]+)', text)
    if ns:
        text = sub(r'xmlns?(:%s)*=.+?["\'\s]|%s:' % ('|:'.join(ns), ':|'.join(ns)), '', text)
        text = sub(r'xmlns=["\'][^"]+["\']', '', text)
    return text


def objectify(text, **kwargs):
    return _objectify(cET.fromstring(stripns(text)), **kwargs)


def _objectify(element, elem_prefix='', attr_prefix='', dictattr_prefix='@'):

    if not element.items() and not element.getchildren():
        if element.text is not None and search('^\s+$', element.text) is None:
            return element.text
        return None

    obj = type(
        element.tag,
        (dict,),
        {
            '__iter__': lambda self: iter(self) if isinstance(self, list) else iter([self]),
            '__getattr__': lambda self, key: PoliteObject(),
            '__name__': 'DynamicObject',
            'hasattr': hasattr
        }
    )()

    if element.text is not None and search('^\s+$', element.text) is None:
        obj['$'] = element.text
        obj.__setattr__('__cdata__', element.text)

    for attr in element.items():
        obj[dictattr_prefix+attr[0]] = attr[1]
        obj.__setattr__(attr_prefix+attr[0], attr[1])

    for subelement in element:
        nodetag = elem_prefix+subelement.tag
        if obj.hasattr(nodetag):
            collection = obj.__getattribute__(nodetag)
            if not isinstance(collection, list):
                collection = [collection]
                obj[nodetag] = collection
                obj.__setattr__(nodetag, collection)
            newobj = _objectify(subelement, elem_prefix, attr_prefix, dictattr_prefix)
            if newobj is not None:
                collection.append(newobj)
        else:
            newobj = _objectify(subelement, elem_prefix, attr_prefix, dictattr_prefix)
            if newobj is not None:
                obj[nodetag] = newobj
                obj.__setattr__(nodetag, obj[nodetag])

    return obj
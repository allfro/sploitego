#!/usr/bin/env python

import xml.etree.ElementTree as ET
from numbers import Number
from copy import deepcopy
from pickle import dumps
from sys import stdout
from re import sub

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'XSStringAttribute',
    'XSEnumAttribute',
    'XSIntegerAttribute',
    'XSBooleanAttribute',
    'XSFloatAttribute',
    'XSLongAttribute',
    'XSAttributeType',
    'XMLAttribute',
    'XSStringSubElement',
    'XSCDataSubElement',
    'XSEnumSubElement',
    'XSIntegerSubElement',
    'XSBooleanSubElement',
    'XSFloatSubElement',
    'XSLongSubElement',
    'XSListSubElement',
    'XSSubElementType',
    'XMLSubElement',
    'ElementTree',
    'Element'
]


_e = ET.Element
_se = ET.SubElement
_eto = ET.ElementTree


class XSStringAttribute(object):

    def __init__(self, name, default=None, required=False):
        self.name = name
        self.required = required
        if default is not None and not isinstance(default, basestring):
            default = str(default)
        self.default = default

    def __get__(self, obj, objtype):
        return obj.attrib.setdefault(self.name, self.default)

    def __set__(self, obj, val):
        if val is None:
            if self.default is None:
                if self.name in obj.attrib:
                    del obj.attrib[self.name]
            else:
                obj.attrib[self.name] = self.default
            return
        elif not isinstance(val, basestring):
            val = str(val)
        obj.attrib[self.name] = val


class XSEnumAttribute(XSStringAttribute):

    def __init__(self, name, choices, default=None, required=False):
        self.choices = [ str(c) if not isinstance(c, basestring) else c for c in choices ]
        super(XSEnumAttribute, self).__init__(name, default, required)

    def __set__(self, obj, val):
        if not isinstance(val, basestring):
            val = str(val)
        if val not in self.choices:
            raise ValueError('Expected one of %s (got %s instead)' % (self.choices, val))
        super(XSEnumAttribute, self).__set__(obj, val)


class XSIntegerAttribute(XSStringAttribute):

    def __get__(self, obj, objtype):
        return int(super(XSIntegerAttribute, self).__get__(obj, objtype))

    def __set__(self, obj, val):
        if not isinstance(val, Number):
            raise TypeError('Expected an instance of int (got %s instance instead)' % type(val).__name__)
        super(XSIntegerAttribute, self).__set__(obj, val)


class XSBooleanAttribute(XSStringAttribute):

    def __init__(self, name, default=False, required=False):
        super(XSBooleanAttribute, self).__init__(name, str(default).lower(), required)

    def __get__(self, obj, objtype):
        return super(XSBooleanAttribute, self).__get__(obj, objtype) == 'true'

    def __set__(self, obj, val):
        if not isinstance(val, bool):
            raise TypeError('Expected an instance of bool (got %s instance instead)' % type(val).__name__)
        super(XSBooleanAttribute, self).__set__(obj, str(val).lower())


class XSFloatAttribute(XSStringAttribute):

    def __get__(self, obj, objtype):
        return float(super(XSFloatAttribute, self).__get__(obj, objtype))

    def __set__(self, obj, val):
        if not isinstance(val, Number):
            raise TypeError('Expected an instance of float (got %s instance instead)' % type(val).__name__)
        super(XSFloatAttribute, self).__set__(obj, val)


class XSLongAttribute(XSStringAttribute):

    def __get__(self, obj, objtype):
        return long(super(XSLongAttribute, self).__get__(obj, objtype))

    def __set__(self, obj, val):
        if not isinstance(val, Number):
            raise TypeError('Expected an instance of float (got %s instance instead)' % type(val).__name__)
        super(XSLongAttribute, self).__set__(obj, val)


class XSAttributeType(object):
    String = XSStringAttribute
    Float = XSFloatAttribute
    Integer = XSIntegerAttribute
    Enum = XSEnumAttribute
    Bool = XSBooleanAttribute
    Long = XSLongAttribute


class XMLAttribute(object):

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        if self.name is None:
            raise ValueError("Keyword argument 'name' is required.")
        self.property = kwargs.get('propname', sub('[^\w]+', '_', self.name))
        self.type = kwargs.get('type', XSAttributeType.String)
        self.default = kwargs.get('default', None)
        self.required = kwargs.get('required', False)
        self.choices = kwargs.get('choices')

    def __call__(self, cls):
        if self.type is XSAttributeType.Enum:
            setattr(cls, self.property, self.type(self.name, self.choices, self.default))
        else:
            setattr(cls, self.property, self.type(self.name, self.default))
        return cls


class XSStringSubElement(object):

    def __init__(self, name, default=None):
        self.name = name
        if default is not None and not isinstance(default, basestring):
            default = str(default)
        self.default = default

    def __get__(self, obj, objtype):
        e = obj.find(self.name)
        if e is None:
            if self.default is None:
                return None
            e = obj.findelement(self.name)
            e.text = self.default
            return e.text
        if e.text is None and self.default is not None:
            e.text = self.default
        return e.text

    def __set__(self, obj, val):
        if val is None:
            e = obj.find(self.name)
            if e is not None:
                if self.default is None:
                    obj.remove(e)
                else:
                    e.text = self.default
            return
        if not isinstance(val, basestring):
            val = str(val)
        obj.findelement(self.name).text = val


class XSCDataSubElement(XSStringSubElement):

    def __init__(self, name, default=None):
        super(XSCDataSubElement, self).__init__('%s/CDATA' % name, default)


class XSEnumSubElement(XSStringSubElement):

    def __init__(self, name, choices, default=None):
        self.choices = [ str(c) if not isinstance(c, basestring) else c for c in choices ]
        super(XSEnumSubElement, self).__init__(name, default)

    def __set__(self, obj, val):
        if not isinstance(val, basestring):
            val = str(val)
        if val not in self.choices:
            raise ValueError('Expected one of %s (got %s instead)' % (self.choices, val))
        super(XSEnumSubElement, self).__set__(obj, val)


class XSIntegerSubElement(XSStringSubElement):

    def __get__(self, obj, objtype):
        return int(super(XSIntegerSubElement, self).__get__(obj, objtype))

    def __set__(self, obj, val):
        if not isinstance(val, Number):
            raise TypeError('Expected an instance of int (got %s instance instead)' % type(val))
        super(XSIntegerSubElement, self).__set__(obj, val)


class XSBooleanSubElement(XSStringSubElement):

    def __init__(self, name, default=False):
        super(XSBooleanSubElement, self).__init__(name, str(default).lower())

    def __get__(self, obj, objtype):
        return super(XSBooleanSubElement, self).__get__(obj, objtype) == 'true'

    def __set__(self, obj, val):
        if not isinstance(val, bool):
            raise TypeError('Expected an instance of bool (got %s instance instead)' % type(val))
        super(XSBooleanSubElement, self).__set__(obj, str(val).lower())


class XSFloatSubElement(XSStringSubElement):

    def __get__(self, obj, objtype):
        return float(super(XSFloatSubElement, self).__get__(obj, objtype))

    def __set__(self, obj, val):
        if not isinstance(val, Number):
            raise TypeError('Expected an instance of float (got %s instance instead)' % type(val))
        super(XSFloatSubElement, self).__set__(obj, val)


class XSLongSubElement(XSStringSubElement):

    def __get__(self, obj, objtype):
        return long(super(XSLongSubElement, self).__get__(obj, objtype))

    def __set__(self, obj, val):
        if not isinstance(val, Number):
            raise TypeError('Expected an instance of float (got %s instance instead)' % type(val))
        super(XSLongSubElement, self).__set__(obj, val)


class XSListSubElement(object):

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, objtype):
        return obj.findelement(self.name)


class XSSubElementType(object):
    String = XSStringSubElement
    Float = XSFloatSubElement
    Integer = XSIntegerSubElement
    Enum = XSEnumSubElement
    Bool = XSBooleanSubElement
    Long = XSLongSubElement
    List = XSListSubElement
    CData = XSCDataSubElement


class XMLSubElement(object):

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        if self.name is None:
            raise ValueError("Keyword argument 'name' is required.")
        self.property = kwargs.get('propname', sub('[^\w]+', '_', self.name))
        self.type = kwargs.get('type', XSSubElementType.String)
        self.default = kwargs.get('default', None)
        self.required = kwargs.get('required', False)
        self.choices = kwargs.get('choices')

    def __call__(self, cls):
        if self.type is XSSubElementType.Enum:
            setattr(cls, self.property, self.type(self.name, self.choices, self.default))
        elif self.type is XSSubElementType.List:
            setattr(cls, self.property, self.type(self.name))
        else:
            setattr(cls, self.property, self.type(self.name, self.default))
        return cls


class ElementTree(ET.ElementTree):
    """ElementTree with CDATA support."""
    def _write(self, file, node, encoding, namespaces):
        if node.tag == 'CDATA':
            if node.text is not None:
                text = node.text.encode(encoding)
                file.write('<![CDATA[%s]]>' % text)
        else:
            _eto._write(self, file, node, encoding, namespaces)

    def write(self, file=stdout, encoding='us-ascii'):
        _eto.write(self, file, encoding)


class Element(ET._ElementInterface, object):

    def __init__(self, tag='Element', attrib={}, **kwargs):
        attrib = attrib.copy()
        attrib.update(kwargs)
        super(Element, self).__init__(tag, attrib)

    def __add__(self, other):
        newobj = deepcopy(self)
        newobj += other
        return newobj

    def __iadd__(self, other):
        if isinstance(other, list):
            for o in other:
                self.appendelement(o)
        else:
            self.appendelement(other)
        return self

    appendelements = __iadd__

    def __sub__(self, other):
        newobj = deepcopy(self)
        newobj -= other
        return newobj

    def __isub__(self, other):
        if isinstance(other, list):
            for o in other:
                self.removeelement(o)
        else:
            self.removeelement(other)
        return self

    removeelements = __isub__

    def appendelement(self, other):
        self.append(other)

    def removeelement(self, other):
        self.remove(other)

    def findelement(self, name):
        e = self.find(name)
        if e is None:
            if '/' in name:
                path = name.split('/')
                e = self
                for p in path:
                    ce = e.find(p)
                    if ce is None:
                        e = _se(e, p)
            else:
                e = _se(self, name)
        return e

    def makeelement(self, tag, attrib):
        return Element(tag, attrib)

    def __eq__(self, other):
        return dumps(self) == dumps(other)

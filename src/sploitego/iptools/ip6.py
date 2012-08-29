#!/usr/bin/env python

from socket import inet_pton, inet_ntop, gaierror, getfqdn, AF_INET6
from struct import pack, unpack
from re import search, match
from numbers import Number

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'inet_itop6',
    'inet_ptoi6',
    'isnetmask6',
    'iswildcard6',
    'cidrlen6',
    'netmask6',
    'cltonm6',
    'IP6Address'
]


def inet_itop6(i):
    return inet_ntop(AF_INET6, pack('!2Q', long(i) >> 64, long(i) & 0xffffffffffffffff))


def inet_ptoi6(ip):
    l = unpack('!2Q', inet_pton(AF_INET6, ip))
    return long(l[0] << 64 | l[1])


def isnetmask6(ip):
    """Returns True if ip is a network mask (e.g. 255.255.0.0).

    Arguments:
    ip -- an IP6Address object, int, long, or any object that supports __index__.
    """
    b = bin(ip)
    return len(b) == 130 and match('0b1+0*$', b) is not None


def iswildcard6(ip):
    """Returns True if ip is a wildcard mask (e.g. 0.0.0.255).

    Arguments:
    ip -- an IP6Address object, int, long, or any object that supports __index__.
    """
    return match('0b0*1*$', bin(ip)) is not None


def cidrlen6(start, end):
    """Returns the CIDR length for a given range (start-end).

    Arguments:
    start -- an IP6Address object, int, long representing the start IP address.
    end -- an IP6Address object, int, long representing the end IP address.
    """
    return 128 if start == end else 130 - len(bin(start ^ end))


def netmask6(start, end):
    """Returns the network mask for a given range (start-end).

    Arguments:
    start -- an IP6Address object, int, long representing the start IP address.
    end -- an IP6Address object, int, long representing the end IP address.
    """
    cl = cidrlen6(start, end)
    return IP6Address(0xffffffffffffffffffffffffffffffff << (128 - cl))


def cltonm6(cidr_len):
    """Converts a CIDR length to a network mask.

    Arguments:
    cidr_len -- An integer representing the CIDR length.
    """
    return IP6Address(int(('1' * cidr_len) + ('0' * (128 - cidr_len)), 2))


class IP6Address(Number):

    def __init__(self, value=0L):
        self.address = value

    def split(self, delimiter=':'):
        return self._str.split(delimiter)

    def _setaddress(self, value):
        if isinstance(value, IP6Address):
            self._str = value._str
            self._long = value._long
        elif isinstance(value, Number):
            self._long = long(value) & 0xffffffffffffffffffffffffffffffff
            self._str = inet_itop6(self._long)
        elif isinstance(value, basestring):
            if search('[^a-fA-F\d:\.]', value):
                try:
                    self._long = inet_ptoi6(self._str)
                    self._str = value
                except (gaierror, TypeError), m:
                    if len(value) == 16:
                        l = unpack('!2Q', value)
                        self._long = l[0] << 64 | l[1]
                        self._str = inet_itop6(self._long)
                    else:
                        raise ValueError('invalid IP address or hostname: %s (Reason: %s)' % (value, m))
            else:
                self._long = inet_ptoi6(value)
                self._str = value
        else:
            raise ValueError('invalid IP address or hostname: %s' % value)

    def _getaddress(self):
        return str(self)

    address = property(_getaddress, _setaddress)

    def _gethostname(self):
        return getfqdn(str(self))

    hostname = property(_gethostname, _setaddress)

    def _getstruct(self):
        return pack('!2Q', long(self) >> 64, long(self) & 0xffffffffffffffff)

    struct = property(_getstruct, _setaddress)

    def _oper(self, other, operator):
        result = IP6Address(other)
        result.address = eval('long(self) %s long(result)' % operator)
        return result

    def _roper(self, other, operator):
        result = IP6Address(other)
        return eval('result %s long(self)' % operator)

    def _ioper(self, other, operator):
        self.address = eval('long(self) %s long(other)' % operator)
        return self

    def __getitem__(self, item):
        if isinstance(item, slice):
            return [ self[i] for i in range(*item.indices(len(self))) ]
        else:
            if item > 15 or item < -16:
                raise IndexError
            if item >= 0:
                return long(self) >> (8 * (15 - item)) & 0xff
            else:
                return long(self) >> (8 * abs(item + 1)) & 0xff

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            for i, j in enumerate(range(*key.indices(len(self)))):
                self[j] = value[i]
        else:
            if key > 15 or key < -16:
                raise IndexError
            bits = 15 - key if key >= 0 else abs(key + 1)
            self.address = (long(self) ^ (self[key] << (8 * bits))) | ((value & 0xff) << (8 * bits))

    def __add__(self, other):
        return self._oper(other, '+')

    def __radd__(self, other):
        return self._roper(other, '+')

    def __iadd__(self, other):
        return self._ioper(other, '+')

    def __sub__(self, other):
        return self._oper(other, '-')

    def __rsub__(self, other):
        return self._roper(other, '-')

    def __isub__(self, other):
        return self._ioper(other, '-')

    def __and__(self, other):
        return self._oper(other, '&')

    def __rand__(self, other):
        return self._roper(other, '&')

    def __iand__(self, other):
        return self._ioper(other, '&')

    def __or__(self, other):
        return self._oper(other, '|')

    def __ror__(self, other):
        return self._roper(other, '|')

    def __ior__(self, other):
        return self._ioper(other, '|')

    def __xor__(self, other):
        return self._oper(other, '^')

    def __rxor__(self, other):
        return self._roper(other, '^')

    def __ixor__(self, other):
        return self._ioper(other, '^')

    def __rshift__(self, other):
        return self._oper(other, '>>')

    def __rrshift__(self, other):
        return self._roper(other, '>>')

    def __irshift__(self, other):
        return self._ioper(other, '>>')

    def __lshift__(self, other):
        return self._oper(other, '<<')

    def __rlshift__(self, other):
        return self._roper(other, '<<')

    def __ilshift__(self, other):
        return self._ioper(other, '<<')

    def __div__(self, other):
        return self._oper(other, '/')

    def __rdiv__(self, other):
        return self._roper(other, '/')

    def __idiv__(self, other):
        return self._ioper(other, '/')

    def __mul__(self, other):
        return self._oper(other, '*')

    def __rmul__(self, other):
        return self._roper(other, '*')

    def __imul__(self, other):
        return self._ioper(other, '*')

    def __mod__(self, other):
        return self._oper(other, '%')

    def __rmod__(self, other):
        return self._roper(other, '%')

    def __imod__(self, other):
        return self._ioper(other, '%')

    def __pow__(self, other):
        return self._oper(other, '**')

    def __rpow__(self, other):
        return self._roper(other, '**')

    def __ipow__(self, other):
        return self._ioper(other, '**')

    def __invert__(self):
        return IP6Address(~long(self))

    def __neg__(self):
        return IP6Address(-1 * long(self))

    def _cmp(self, other, operator):
        result = IP6Address(other)
        return eval('long(self) %s long(result)' % operator)

    def __eq__(self, other):
        return self._cmp(other, '==')

    def __ne__(self, other):
        return self._cmp(other, '!=')

    def __gt__(self, other):
        return self._cmp(other, '>')

    def __ge__(self, other):
        return self._cmp(other, '>=')

    def __lt__(self, other):
        return self._cmp(other, '<')

    def __le__(self, other):
        return self._cmp(other, '<=')

    def __eq__(self, other):
        return self._cmp(other, '==')

    def __nonzero__(self):
        return long(self) != 0

    def __str__(self):
        return self._str

    def __repr__(self):
        return str(self)

    def __hex__(self):
        return hex(long(self))

    def __oct__(self):
        return oct(long(self))

    def __index__(self):
        return long(self)

    def __int__(self):
        return int(self._long)

    def __long__(self):
        return self._long

    def __len__(self):
        return 16
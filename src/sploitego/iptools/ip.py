#!/usr/bin/env python

from operator import add, sub, and_, or_, xor, rshift, lshift, div, mul, mod, pow, eq, ne, lt, le, gt, ge
from socket import inet_aton, inet_ntoa, gethostbyname, gaierror, getfqdn
from re import split, search, match, findall
from struct import pack, unpack
from numbers import Number
from os import path, sep

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'inet_itop',
    'inet_ptoi',
    'isnetmask',
    'iswildcard',
    'cidrlen',
    'netmask',
    'cltonm',
    'iptuple',
    'iprange',
    'portrange',
    'resolvers',
    'IPAddress',
    'IPNetwork'
]


def inet_itop(i):
    """Given an integer, returns a string containing the dotted IP address.

    Arguments:
    i -- an integer.
    """
    return inet_ntoa(pack('!L', int(i) & 0xffffffff))


def inet_ptoi(ip):
    """Returns the integer representation of the dotted IP address.

    Arguments:
    ip -- a string containing the dotted IP address.
    """
    return unpack('!L', inet_aton(ip))[0]


def isnetmask(ip):
    """Returns True if ip is a network mask (e.g. 255.255.0.0).

    Arguments:
    ip -- an IPAddress object, int, long, or any object that supports __index__.
    """
    if not ip: return True
    b = bin(ip)
    return len(b) == 34 and match('0b1*0*$', b) is not None


def iswildcard(ip):
    """Returns True if ip is a wildcard mask (e.g. 0.0.0.255).

    Arguments:
    ip -- an IPAddress object, int, long, or any object that supports __index__.
    """
    if not ip: return True
    return match('0b0*1*$', bin(ip)) is not None


def cidrlen(start, end):
    """Returns the CIDR length for a given range (start-end).

    Arguments:
    start -- an IPAddress object, int, long representing the start IP address.
    end -- an IPAddress object, int, long representing the end IP address.
    """
    return 32 if start == end else 34 - len(bin(start ^ end))


def netmask(start, end):
    """Returns the network mask for a given range (start-end).

    Arguments:
    start -- an IPAddress object, int, long representing the start IP address.
    end -- an IPAddress object, int, long representing the end IP address.
    """
    cl = cidrlen(start, end)
    return IPAddress(0xffffffff << (32 - cl))


def cltonm(cidr_len):
    """Converts a CIDR length to a network mask.

    Arguments:
    cidr_len -- An integer representing the CIDR length.
    """
    return IPAddress(int(('1' * cidr_len) + ('0' * (32 - cidr_len)), 2))


def iptuple(ips):
    """Returns a list containing the first and last IP Address of a network block.

     Arguments:
     ips -- a string representing a network range (e.g. a.b.c.d-w.x.y.z or a.b-x.c.d or a.b.c.d-y.z)
    """
    if '-' in ips:
        if ips.count('-') == 1:
            [ start, end ] = ips.split('-')
            if start.count('.') != 3:
                return _iptuple(ips)
            else:
                start, end = IPAddress(start), IPAddress(end)
                for i in range(0, 4 - len(end)):
                    end[i] = start[i]
                return [ start, end ] if end > start else [ end, start ]
        else:
            return _iptuple(ips)
    else:
        start = IPAddress(ips)
        return [ start, start ]


def _iptuple(ips):
    start = IPAddress()
    end = IPAddress()
    for i, o in enumerate(ips.split('.')):
        if '-' in o:
            r = [ int(o) for o in o.split('-') ]
            r.sort()
            start[i], end[i] = r[0], r[1]
        else:
            start[i] = end[i] = int(o)
    return [ start, end ]


def iprange(ips):
    start, end = iptuple(ips)
    if start == end:
        return [ start ]
    end += 1
    return [IPAddress(i) for i in range(start, end)]


def portrange(ports):
    ps = []
    for p in ports.split(','):
        if '-' not in p:
            ps.append(int(p))
        else:
            start, end = p.split('-')
            ps += range(int(start), int(end)+1)
    return ps


def resolvers():
    """Returns a list of the current system's DNS resolvers."""
    r = []
    if sep == '/' and path.exists('/etc/resolv.conf'):
        for l in open('/etc/resolv.conf'):
            if l.startswith('nameserver'):
                ns = split('\s+', l)
                r.append(ns[1])
    elif sep == '\\':
        # TODO: Get MS Winblows resolvers
        pass
    return r


class IPAddress(Number):

    _len = 0

    def __init__(self, value=0):
        self.address = value

    def split(self, delimiter='.'):
        return self._str.split(delimiter)

    def _setaddress(self, value):
        if isinstance(value, IPAddress):
            self._len = value._len
            self._str = value._str
            self._int = value._int
        elif isinstance(value, Number):
            self._len = 4
            self._int = int(value) & 0xffffffff
            self._str = inet_itop(self._int)
        elif isinstance(value, basestring):
            if value.endswith('in-addr.arpa'):
                octets = findall('(\d+?)\\.', value)
                if octets:
                    self._str = '.'.join(reversed(octets)) + ('.0' * (4 - len(octets)))
                else:
                    self._str = '0.0.0.0'
                self._int = inet_ptoi(self._str)
            elif search('[^\d.]', value):
                self._len = 4
                try:
                    self._str = gethostbyname(value)
                    self._int = inet_ptoi(self._str)
                except (gaierror, TypeError), m:
                    if len(value) == 4:
                        self._int = unpack('!L', value)[0]
                        self._str = inet_itop(self._int)
                    else:
                        raise ValueError('invalid IP address or hostname: %s (Reason: %s)' % (value, m))
            else:
                dc = value.count('.')
                self._len = dc + 1
                if dc != 3:
                    for i in range(0, 3 - dc):
                        value = '0.' + value
                self._int = inet_ptoi(value)
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
        return pack('!L', int(self))

    struct = property(_getstruct, _setaddress)

    def _getarpa(self):
        return '%d.%d.%d.%d.in-addr.arpa' % tuple(reversed(self[:]))

    arpa = property(_getarpa, _setaddress)

    def _oper(self, other, operator):
        result = IPAddress(other)
        result.address = operator(int(self), int(result))
        return result

    def _roper(self, other, operator):
        result = IPAddress(other)
        return operator(result, int(self))

    def _ioper(self, other, operator):
        self.address = operator(int(self), int(other))
        return self

    def __getitem__(self, item):
        if isinstance(item, slice):
            return [ self[i] for i in range(*item.indices(4)) ]
        else:
            if item > 3 or item < -4:
                raise IndexError
            if item >= 0:
                return int(self) >> (8 * (3 - item)) & 0xff
            else:
                return int(self) >> (8 * abs(item + 1)) & 0xff

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            for i, j in enumerate(range(*key.indices(4))):
                self[j] = value[i]
        else:
            if key > 3 or key < -4:
                raise IndexError
            tmp = self._len
            bits = 3 - key if key >= 0 else abs(key + 1)
            self.address = (int(self) ^ (self[key] << (8 * bits))) | ((value & 0xff) << (8 * bits))
            self._len = max(tmp, 4 - key)

    def __add__(self, other):
        return self._oper(other, add)

    def __radd__(self, other):
        return self._roper(other, add)

    def __iadd__(self, other):
        return self._ioper(other, add)

    def __sub__(self, other):
        return self._oper(other, sub)

    def __rsub__(self, other):
        return self._roper(other, sub)

    def __isub__(self, other):
        return self._ioper(other, sub)

    def __and__(self, other):
        return self._oper(other, and_)

    def __rand__(self, other):
        return self._roper(other, and_)

    def __iand__(self, other):
        return self._ioper(other, and_)

    def __or__(self, other):
        return self._oper(other, or_)

    def __ror__(self, other):
        return self._roper(other, or_)

    def __ior__(self, other):
        return self._ioper(other, or_)

    def __xor__(self, other):
        return self._oper(other, xor)

    def __rxor__(self, other):
        return self._roper(other, xor)

    def __ixor__(self, other):
        return self._ioper(other, xor)

    def __rshift__(self, other):
        return self._oper(other, rshift)

    def __rrshift__(self, other):
        return self._roper(other, rshift)

    def __irshift__(self, other):
        return self._ioper(other, rshift)

    def __lshift__(self, other):
        return self._oper(other, lshift)

    def __rlshift__(self, other):
        return self._roper(other, lshift)

    def __ilshift__(self, other):
        return self._ioper(other, lshift)

    def __div__(self, other):
        return self._oper(other, div)

    def __rdiv__(self, other):
        return self._roper(other, div)

    def __idiv__(self, other):
        return self._ioper(other, div)

    def __mul__(self, other):
        return self._oper(other, mul)

    def __rmul__(self, other):
        return self._roper(other, mul)

    def __imul__(self, other):
        return self._ioper(other, mul)

    def __mod__(self, other):
        return self._oper(other, mod)

    def __rmod__(self, other):
        return self._roper(other, mod)

    def __imod__(self, other):
        return self._ioper(other, mod)

    def __pow__(self, other):
        return self._oper(other, pow)

    def __rpow__(self, other):
        return self._roper(other, pow)

    def __ipow__(self, other):
        return self._ioper(other, pow)

    def __invert__(self):
        return IPAddress(~int(self))

    def __neg__(self):
        return IPAddress(-1 * int(self))

    def _cmp(self, other, comparator):
        result = IPAddress(other)
        return comparator(int(self), int(result))

    def __eq__(self, other):
        return self._cmp(other, eq)

    def __ne__(self, other):
        return self._cmp(other, ne)

    def __gt__(self, other):
        return self._cmp(other, gt)

    def __ge__(self, other):
        return self._cmp(other, ge)

    def __lt__(self, other):
        return self._cmp(other, lt)

    def __le__(self, other):
        return self._cmp(other, le)

    def __nonzero__(self):
        return int(self) != 0

    def __str__(self):
        return self._str

    def __repr__(self):
        return str(self)

    def __hex__(self):
        return hex(int(self))

    def __oct__(self):
        return oct(int(self))

    def __index__(self):
        return int(self)

    def __int__(self):
        return self._int

    def __long__(self):
        return long(int(self))

    def __len__(self):
        return self._len


class IPNetwork(list):

    def __init__(self, netblock):
        super(IPNetwork, self).__init__()
        self._setnetblock(netblock)

    def _setnetblock(self, netblock):
        if len(self):
            del self[:]
        if isinstance(netblock, list):
            nr = [ ip if isinstance(ip, IPAddress) else IPAddress(ip) for ip in netblock ]
            nr.sort()
            if len(nr) == 1:
                self.append(nr[0])
                self.append(nr[0])
            else:
                if isnetmask(nr[-1]):
                    self.append(nr[0] & nr[-1])
                    self.append(nr[0] | ~nr[-1])
                else:
                    nm = netmask(nr[0], nr[-1])
                    self.append(nr[0] & nm)
                    self.append(nr[-1] | ~nm)
        elif isinstance(netblock, basestring):
            if '/' in netblock:
                [ ip, cl ] = netblock.split('/')
                if '.' in cl:
                    nm = IPAddress(cl)
                    if isnetmask(nm):
                        self.append(ip & nm)
                        self.append(ip | ~nm)
                    else:
                        raise ValueError('Invalid netmask: %s' % nm)
                else:
                    nm = cltonm(int(cl))
                    self.append(ip & nm)
                    self.append(ip | ~nm)
            elif '-' in netblock:
                [ start, end ] = iptuple(netblock)
                nm = netmask(start, end)
                self.append(start & nm)
                self.append(end | ~nm)
            else:
                self.append(IPAddress(netblock))
                self.append(IPAddress(netblock))

    def _getnetblock(self):
        return '%s-%s' % (self[0], self[1])

    netblock = property(_getnetblock, _setnetblock)

    def _setcidrlen(self, value):
        nm = cltonm(value)
        self[0] &= nm
        self[1] = self[0] | ~nm

    def _getcidrlen(self):
        return cidrlen(*self)

    cidrlen = property(_getcidrlen, _setcidrlen)

    def _setnetmask(self, value):
        nm = IPAddress(value)
        if not isnetmask(nm):
            raise ValueError('Invalid netmask: %s' % nm)
        self[0] &= nm
        self[1] = self[0] | ~nm

    def _getnetmask(self):
        return netmask(*self)

    netmask = property(_getnetmask, _setnetmask)

    def _setwildcard(self, value):
        wc = IPAddress(value)
        if iswildcard(wc):
            raise ValueError('Invalid wildcard: %s' % wc)
        self.netmask = ~wc

    def _getwildcard(self):
        return ~self.netmask

    wildcard = property(_getwildcard, _setwildcard)

    def __setitem__(self, key, value):
        if key < -2 or key > 1:
            raise IndexError('list index out of range')
        super(IPNetwork, self).__setitem__(key, value)
        self.netblock = list(self)

    def _cmpor(self, other, lcmp, rcmp):
        if not isinstance(other, IPNetwork):
            other = IPNetwork(other)
        return lcmp(self[1], other[1]) or rcmp(self.cidrlen, other.cidrlen)

    def _cmpand(self, other, lcmp, rcmp):
        if not isinstance(other, IPNetwork):
            other = IPNetwork(other)
        return lcmp(self[1], other[1]) and rcmp(self.cidrlen, other.cidrlen)

    def __eq__(self, other):
        return self._cmpand(other, eq, eq)

    def __ne__(self, other):
        return self._cmpor(other, ne, ne)

    def __lt__(self, other):
        return self._cmpor(other, lt, gt)

    def __gt__(self, other):
        return self._cmpor(other, gt, lt)

    def __le__(self, other):
        return self._cmpand(other, le, ge)

    def __ge__(self, other):
        return self._cmpand(other, ge, le)

    def __contains__(self, item):
        return self[0] <= item <= self[1]

    def __str__(self):
        return self.netblock

    def __repr__(self):
        return '%s/%s' % (self[0], self.cidrlen)
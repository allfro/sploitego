#!/usr/bin/env python

from nessus import NessusXmlRpcClient, NessusSessionException, NessusException
from canari.easygui import multpasswordbox, choicebox
from canari.utils.fs import cookie, fsemaphore
from canari.config import config

from urlparse import parse_qsl
from urllib import urlencode
from os import path, unlink
from time import strftime


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'login',
    'policy',
    'scan'
]


def login():
    s = None
    fn = cookie('nessus')
    if not path.exists(fn):
        f = fsemaphore(fn, 'wb')
        f.lockex()
        fv = ['localhost', '8834']
        errmsg = ''
        while True:
            fv = multpasswordbox(errmsg, 'Nessus Login', ['Server:', 'Port:', 'Username:', 'Password:'], fv)
            try:
                s = NessusXmlRpcClient(fv[2], fv[3], fv[0], fv[1])
            except NessusException, e:
                errmsg = str(e)
                continue
            break
        f.write(urlencode({'host' : fv[0], 'port' : fv[1], 'token': s.token}))
    else:
        f = fsemaphore(fn)
        f.locksh()
        try:
            d = dict(parse_qsl(f.read()))
            s = NessusXmlRpcClient(**d)
        except NessusSessionException:
            unlink(fn)
            return login()
    return s


def policy(s):
    ps = s.policies.list
    c = choicebox('Select a Nessus scanning policy', 'Nessus Policies', ps)
    if c is None:
        return None
    return filter(lambda x: str(x) == c, ps)[0]


def scan(s, t, p):
    return s.scanner.scan(strftime(config['nessus/namefmt']), t, p)

# !/usr/bin/env python
import socket

from nessus import NessusXmlRpcClient, NessusSessionException, NessusException
from canari.easygui import multpasswordbox, choicebox
from canari.utils.fs import cookie, fsemaphore
from canari.config import config

from urlparse import parse_qsl
from urllib import urlencode

import os
import time


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.2'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'login',
    'policy',
    'scan'
]


def login(host='localhost', port='8834', username='', password=''):
    s = None
    fn = cookie('%s.%s.nessus' % (host, port))
    if not os.path.exists(fn):
        with fsemaphore(fn, 'wb') as f:
            f.lockex()
            errmsg = ''
            while True:
                fv = multpasswordbox(
                    errmsg,
                    'Nessus Login',
                    ['Server:', 'Port:', 'Username:', 'Password:'],
                    [host, port, username, password]
                )
                if not fv:
                    f.close()
                    os.unlink(fn)
                    return
                host, port, username, password = fv
                try:
                    s = NessusXmlRpcClient(username, password, host, port)
                except NessusException, e:
                    errmsg = str(e)
                    continue
                except socket.error, e:
                    errmsg = str(e)
                    continue
                break
            f.write(urlencode(dict(host=host, port=port, token=s.token)))
    else:
        with fsemaphore(fn) as f:
            f.locksh()
            try:
                d = dict(parse_qsl(f.read()))
                s = NessusXmlRpcClient(**d)
                policies = s.policies.list
            except NessusException:
                os.unlink(fn)
                return login()
            except NessusSessionException:
                os.unlink(fn)
                return login()
            except socket.error:
                os.unlink(fn)
                return login()
    return s


def policy(s):
    ps = s.policies.list
    c = choicebox('Select a Nessus scanning policy', 'Nessus Policies', ps)
    if c is None:
        return
    return filter(lambda x: str(x) == c, ps)[0]


def scan(s, t, p):
    return s.scanner.scan(time.strftime(config['nessus/namefmt']), t, p)

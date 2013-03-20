#!/usr/bin/env python
import socket
from urlparse import parse_qsl
from urllib import urlencode
from os import path, unlink

from canari.easygui import multpasswordbox
from canari.utils.fs import cookie, fsemaphore
from canari.config import config

from metasploit.msfrpc import MsfRpcClient, MsfRpcError


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'login'
]


def login(**kwargs):
    s = None
    host = kwargs.get('host', config['msfrpcd/server'])
    port = kwargs.get('port', config['msfrpcd/port'])
    uri = kwargs.get('uri', config['msfrpcd/uri'])
    fn = cookie('%s.%s.%s.msfrpcd' % (host, port, uri.replace('/', '.')))
    if not path.exists(fn):
        f = fsemaphore(fn, 'wb')
        f.lockex()
        fv = [ host, port, uri, 'msf' ]
        errmsg = ''
        while True:
            fv = multpasswordbox(errmsg, 'Metasploit Login', ['Server:', 'Port:', 'URI', 'Username:', 'Password:'], fv)
            if not fv:
                return
            try:
                s = MsfRpcClient(fv[4], server=fv[0], port=fv[1], uri=fv[2], username=fv[3])
            except MsfRpcError, e:
                errmsg = str(e)
                continue
            except socket.error, e:
                errmsg = str(e)
                continue
            break
        f.write(urlencode({'host' : fv[0], 'port' : fv[1], 'uri': fv[2], 'token': s.sessionid}))
        f.unlock()

        if 'db' not in s.db.status:
            s.db.connect(
                config['metasploit/dbusername'],
                database=config['metasploit/dbname'],
                driver=config['metasploit/dbdriver'],
                host=config['metasploit/dbhost'],
                port=config['metasploit/dbport'],
                password=config['metasploit/dbpassword']
            )
    else:
        f = fsemaphore(fn)
        f.locksh()
        try:
            d = dict(parse_qsl(f.read()))
            s = MsfRpcClient('', **d)
        except MsfRpcError:
            unlink(fn)
            return login()
        except socket.error:
            unlink(fn)
            return login()
    return s
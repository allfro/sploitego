#!/usr/bin/env python

from xml.etree.cElementTree import XML
from os import path, pathsep, environ
from subprocess import Popen, PIPE


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'NmapReportParser',
    'NmapScanner'
]


def NmapReportParser(output):
    if not output:
        return None
    elif 'xmloutputversion="1.03"' in output:
        return NmapReportVersion103(output)
    elif 'xmloutputversion="1.04"' in output:
        return NmapReportVersion104(output)
    raise NotImplementedError('Nmap 5.x and 6.x XML reports are the only supported formats')


class NmapReportBase(object):

    def __init__(self, output):
        self.output = output
        self.xml = XML(output)

    @property
    def addresses(self):
        raise NotImplementedError

    @property
    def report(self):
        return self.output

    def mac(self, address):
        raise NotImplementedError

    def _host(self, address):
        raise NotImplementedError

    def ports(self, address):
        raise NotImplementedError

    @property
    def scaninfo(self):
        raise NotImplementedError

    @property
    def verbosity(self):
        raise NotImplementedError

    @property
    def debugging(self):
        raise NotImplementedError

    def hostnames(self, address):
        raise NotImplementedError

    def times(self, address):
        raise NotImplementedError

    @property
    def runstats(self):
        raise NotImplementedError

    def scanstats(self, address):
        raise NotImplementedError

    def status(self, address):
        raise NotImplementedError

    @property
    def nmaprun(self):
        raise NotImplementedError

    def tobanner(self, port):
        raise NotImplementedError

    @property
    def greppable(self):
        raise NotImplementedError


class NmapReportVersion103(NmapReportBase):

    def os(self, address):
        host = self._host(address)
        if host is not None:
            r = {
                'osmatch': [osm.attrib for osm in host.findall('os/osmatch')],
                'osclass': [osm.attrib for osm in host.findall('os/osclass')],
                'portused': host.find('os/portused').attrib  if host.find('os/portused') is not None else {}
            }
            return r
        return { 'osmatch' : [], 'osclass' : [], 'portused' : {} }

    @property
    def addresses(self):
        return [ a.get('addr') for a in self.xml.findall('host/address') if a.get('addrtype') == 'ipv4' ]

    def mac(self, address):
        host = self._host(address)
        if host is not None:
            for addr in host.findall('address'):
                if addr.get('addrtype') == 'mac':
                    return addr.get('addr')
        return None

    def _host(self, address):
        for host in self.xml.findall('host'):
            for addr in host.findall('address'):
                if addr.get('addr') == address:
                    return host
        return None

    def ports(self, address):
        host = self._host(address)
        ports = []
        if host is not None:
            for p in host.findall('ports/port'):
                r = p.attrib
                map(lambda x: r.update(x.attrib), p.getchildren())
                ports.append(r)
        return ports

    @property
    def scaninfo(self):
        return self.xml.find('scaninfo').attrib

    @property
    def verbosity(self):
        return self.xml.find('verbose').get('level')

    @property
    def debugging(self):
        return self.xml.find('debugging').get('level')

    def hostnames(self, address):
        host = self._host(address)
        if host is not None:
            return [ hn.attrib for hn in host.findall('hostnames/hostname') ]
        return []

    def times(self, address):
        host = self._host(address)
        if host is not None:
            return host.find('times').attrib
        return {}

    @property
    def runstats(self):
        rs = {}
        map(lambda x: rs.update(x.attrib), self.xml.find('runstats').getchildren())
        return rs

    def scanstats(self, address):
        host = self._host(address)
        if host is not None:
            return host.attrib
        return {}

    def status(self, address):
        host = self._host(address)
        if host is not None:
            return host.find('status').attrib
        return {}

    @property
    def nmaprun(self):
        return self.xml.attrib

    def tobanner(self, port):
        banner = port.get('product', 'Unknown')
        version = port.get('version')
        if version is not None:
            banner += ' %s' % version
        extrainfo = port.get('extrainfo')
        if extrainfo is not None:
            banner += ' (%s)' % extrainfo
        return banner

    @property
    def greppable(self):
        n = self.nmaprun
        output = '# Nmap %s scan initiated %s as: %s\n' % (n['version'], n['startstr'], n['args'])
        for a in self.addresses:
            s = self.status(a)
            output += 'Host: %s () Status: %s\n' % (a, s['state'].title())
            output += 'Host: %s () Ports:' % a
            for p in self.ports(a):
                output += ' %s/%s/%s//%s///,' % (p['portid'], p['state'], p['protocol'], p['name'])
            output = output.rstrip(',')
        output += '\n# %s\n' % self.runstats['summary']
        return output


class NmapReportVersion104(NmapReportVersion103):
    pass


class NmapScanner(object):

    output = ''
    cmd = ''

    def getversion(self, binargs=[], binpath=None):
        if binargs:
            self.program = binargs if isinstance(binargs, list) else [ binargs ]
            self.version = self.run(['--version'])
            return True
        elif binpath is None:
            for p in environ['PATH'].split(pathsep):
                program = path.join(p, 'nmap')
                if path.exists(program):
                    self.program = [ program ]
                    self.version = self.run(['--version'])
                    return True
        elif path.exists(binpath):
            self.program = [ binpath ]
            self.version = self.run(['--version'])
            return True
        return False

    def run(self, args):
        self.cmd = ' '.join(self.program + args)
        self._pipe = Popen(self.program + args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        r, e = self._pipe.communicate()
        self.output = r
        self.error = e

        return r.strip('\n')

    def __init__(self, binargs=[], binpath=None):
        if not self.getversion(binargs, binpath):
            raise OSError('Could not find nmap, check your OS path')

    def scan(self, args, sendto=NmapReportParser):
        r = self.run(['-oX', '-'] + args)
        if callable(sendto):
            return sendto(r)
        return sendto.write(r)

    def terminate(self):
        self._pipe.terminate()

    def __del__(self):
        try:
            self.terminate()
        except OSError:
            pass
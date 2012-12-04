#!/usr/bin/env python

from ConfigParser import NoOptionError
from sploitego.cmdtools.nmap import NmapScanner

from entities import Port, NmapReport, OS
from canari.maltego.message import Label
from canari.utils.fs import ufile
from canari.config import config

from os import makedirs, path
from time import strftime


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


def getscanner():
    binargs = None
    try:
        binargs = config['nmap/nmapcmd'].split(' ')
    except NoOptionError:
        pass
    return NmapScanner() if binargs is None else NmapScanner(binargs)


def addports(report, response):

    for addr in report.addresses:
        for port in report.ports(addr):
            e = Port(port['portid'])
            e.protocol = port['protocol'].upper()
            e.status = port['state'].title()
            e.destination = addr
            e.response = port['reason']
            e += Label('Service Name', port.get('name', 'unknown'))
            if 'servicefp' in port:
                e += Label('Service Fingerprint', port['servicefp'])
            if 'extrainfo' in port:
                e += Label('Extra Information', port['extrainfo'])
            if 'method' in port:
                e += Label('Method', port['method'])
            response += e


def savereport(report):
    if not path.exists(config['nmap/reportdir']):
        makedirs(config['nmap/reportdir'])
    f = ufile(strftime(path.join(config['nmap/reportdir'], config['nmap/namefmt'])))
    f.write(report.output)
    f.close()
    return f.name


def addreport(report, response, tag, cmd):
    e = NmapReport('Nmap %s Report: %s' % (tag, report.nmaprun['startstr']))
    e.file = savereport(report)
    e.command = cmd
    response += e


def addsystems(report, response):
    for addr in report.addresses:
        for osm in report.os(addr)['osmatch']:
            e = OS(osm['name'])
            e.name = osm['name']
            e += Label('Accuracy', osm['accuracy'])
            response += e
#!/usr/bin/env python

from os import makedirs, path, sep
from time import strftime

from sploitego.maltego.message import Label
from entities import Port, NmapReport, OS
from sploitego.utils.fs import ufile
from sploitego.config import config

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


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


def addreport(report, response, tag):
    e = NmapReport('Nmap %s Report: %s' % (tag, report.nmaprun['startstr']))
    e.file = savereport(report)
    e.command = report.nmaprun['args']
    response += e


def addsystems(report, response):
    for addr in report.addresses:
        for osm in report.os(addr)['osmatch']:
            e = OS(osm['name'])
            e += Label('Accuracy', osm['accuracy'])
            response += e
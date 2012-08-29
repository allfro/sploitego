#!/usr/bin/env python


import sys
from zipfile import ZipFile
from argparse import ArgumentParser
#from sploitego.xmltools.objectify import objectify
from sploitego.commands.common import cmd_name
from xml.etree.cElementTree import XML


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


parser = ArgumentParser(
    description='Convert Maltego graph files (*.mtgx) to comma-separated values (CSV) file.',
    usage='sploitego %s <graph>' % cmd_name(__name__)
)

parser.add_argument(
    'graph',
    metavar='<graph>',
    help='The name of the graph file you wish to convert to CSV.',
)


def parse_args(args):
    return parser.parse_args(args)


def help():
    parser.print_help()


def description():
    return parser.description


def run(args):

    opts = parse_args(args)

    zip = ZipFile(opts.graph)
    graphs = filter(lambda x: x.endswith('.graphml'), zip.namelist())

    for f in graphs:
        csv = open(f.split('/')[1].split('.')[0] + '.csv', 'w')
        xml = XML(zip.open(f).read())
        for e in xml.findall('{http://graphml.graphdrawing.org/xmlns}graph/{http://graphml.graphdrawing.org/xmlns}node/{http://graphml.graphdrawing.org/xmlns}data/{http://maltego.paterva.com/xml/mtgx}MaltegoEntity'):
            csv.write(('"Entity Type=%s",' % e.get('type')).strip())
            for prop in e.findall('{http://maltego.paterva.com/xml/mtgx}Properties/{http://maltego.paterva.com/xml/mtgx}Property'):
                value = prop.find('{http://maltego.paterva.com/xml/mtgx}Value').text or ''
                if '"' in value:
                    value.replace('"', '""')
                csv.write(('"%s=%s",' % (prop.get('displayName'), value)).strip())
            csv.write('\n')
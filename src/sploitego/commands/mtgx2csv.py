#!/usr/bin/env python


import sys
from zipfile import ZipFile
from argparse import ArgumentParser
from sploitego.xmltools.objectify import objectify
from sploitego.commands.common import cmd_name


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = ['Nadeem Douba']

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


def run(args):

    opts = parse_args(args)

    zip = ZipFile(opts.graph)
    graphs = filter(lambda x: x.endswith('.graphml'), zip.namelist())

    for f in graphs:
        csv = open(f.split('/')[1].split('.')[0] + '.csv', 'w')
        xml = zip.open(f).read()
        o = objectify(xml)
        for node in o.graph.node:
            for d in node.data:
                if 'MaltegoEntity' in d:
                    csv.write(('"Entity Type=%s",' % d.MaltegoEntity.type).strip())
                    for prop in d.MaltegoEntity.Properties.Property:
                        if '"' in prop.Value:
                            prop.Value.replace('"', '""')
                        csv.write(('"%s=%s",' % (prop.displayName, prop.Value)).strip())
                    csv.write('\n')
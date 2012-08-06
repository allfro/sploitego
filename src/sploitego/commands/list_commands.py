#!/usr/bin/env python

from argparse import ArgumentParser
from sploitego.commands.common import get_commands, cmd_name, highlight
from sys import modules

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

cmds = get_commands()
cmds.update({'list-commands': modules[__name__]})

parser = ArgumentParser(
    description='Lists all the available sploitego commands',
    usage='sploitego %s' % cmd_name(__name__)
)


def help():
    parser.print_help()


def description():
    return parser.description


def run(args):
    k = cmds.keys()
    k.sort()
    for i in k:
        print '%s - %s' % (highlight(i, 'green', True), cmds[i].description())
#!/usr/bin/env python

from argparse import ArgumentParser
from sploitego.commands.common import get_commands, cmd_name
from sys import modules

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

cmds = get_commands()
cmds.update({'help': modules[__name__]})

parser = ArgumentParser(
    description='Shows help related to various sploitego commands',
    usage='sploitego %s <command>' % cmd_name(__name__)
)
parser.add_argument(
    'command',
    metavar='<command>',
    choices=cmds,
    help='The sploitego command you want help for (%s)' % ', '.join(cmds)
)


def help():
    parser.print_help()


def description():
    return parser.description


def run(args):
    cmds[parser.parse_args(args).command].help()
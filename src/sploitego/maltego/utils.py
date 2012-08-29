#!/usr/bin/env python

from signal import signal, SIGTERM, SIGINT
from sys import exit, argv, stderr
from cStringIO import StringIO
from re import split

from sploitego.maltego.message import MaltegoMessage, Message, MaltegoTransformExceptionMessage, MaltegoException

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'onterminate',
    'message',
    'croak',
    'parseargs',
    'debug',
    'progress'
]


def onterminate(func):
    """Register a signal handler to execute when Maltego forcibly terminates the transform."""
    signal(SIGTERM, func)
    signal(SIGINT, func)


def message(m):
    """Write a MaltegoMessage to stdout and exit successfully"""
    sio = StringIO()
    m.entities
    Message(MaltegoMessage(m)).write(sio)
    print sio.getvalue()
    exit(0)


def croak(error_msg):
    """Throw an exception in the Maltego GUI containing error_msg."""
    Message(MaltegoMessage(MaltegoTransformExceptionMessage(exceptions=MaltegoException(error_msg)))).write()
    exit(0)


def parseargs(args=argv):
    """Parse arguments for Maltego local transforms."""

    if len(args) < 3:
        stderr.write('usage: %s <transform> [param1 ... paramN] <value> [field1=value1...#fieldN=valueN]\n' % args[0])
        exit(-1)

    arg_script = args[1]
    arg_field = args[-1] if '=' in args[-1] else None
    arg_value = args[-1] if arg_field is None else args[-2]
    arg_param = []

    if arg_field is None and len(args) > 3:
        arg_param = list(args[2:-1])
    elif arg_field is not None and len(args) > 4:
        arg_param = list(args[2:-2])

    fields = {}
    if arg_field is not None:
        fs = split(r'(?<=[^\\])#', arg_field)
        if fs is not None:
            fields = dict(map(lambda x: x.split('=', 1), fs))

    return arg_script, arg_param, arg_value, fields


def debug(*args):
    """Send debug messages to the Maltego console."""
    for i in args:
        stderr.write('D:%s\n' % str(i))


def progress(i):
    """Send a progress report to the Maltego console."""
    stderr.write('%%%d\n' % min(max(i, 0), 100))
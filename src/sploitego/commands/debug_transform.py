#!/usr/bin/env python

import logging
import sys
from os import execvp, geteuid, name, path, environ
from traceback import format_exc
from argparse import ArgumentParser
from distutils.sysconfig import get_config_var
from sploitego.commands.common import croak, import_transform, cmd_name, console_message
from sploitego.maltego.message import MaltegoException, MaltegoTransformResponseMessage
from sploitego.maltego.utils import onterminate, parseargs
from sploitego.config import config

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


parser = ArgumentParser(
    description='Runs Sploitego local transforms in a terminal-friendly fashion.',
    usage='sploitego %s <transform> [param1 ... paramN] <value> [field1=value1...#fieldN=valueN]' % cmd_name(__name__)
)

parser.add_argument(
    'transform',
    metavar='<transform>',
    help='The name of the transform you wish to run (e.g. sploitego.transforms.nmapfastscan).'
)

parser.add_argument(
    'value',
    metavar='<value>',
    help='The value of the input entity being passed into the local transform.'
)

parser.add_argument(
    'params',
    metavar='[param1 ... paramN]',
    help='Any extra parameters that can be sent to the local transform.'
)

parser.add_argument(
    'fields',
    metavar='[field1=value1...#fieldN=valueN]',
    help='The fields of the input entity being passed into the local transform.'
)


def help():
    parser.print_help()


def description():
    return parser.description


def run(args):

    logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

    [transform, params, value, fields] = parseargs(['sploitego %s' % cmd_name(__name__)] + args)

    m = None
    pysudo = path.join(get_config_var('BINDIR'), 'pysudo')
    if config['default/path'] is not None:
        environ['PATH'] = config['default/path']
    try:
        m = import_transform(transform)

        if name == 'posix' and hasattr(m.dotransform, 'privileged') and geteuid():
            execvp(pysudo, [pysudo] + list(sys.argv))
            sys.exit(-1)

        if hasattr(m, 'onterminate'):
            onterminate(m.onterminate)
        else:
            m.__setattr__('onterminate', lambda *args: exit(-1))

        msg = m.dotransform(
            type(
                'MaltegoTransformRequestMessage',
                (object,),
                    {
                    'value' : value,
                    'fields' : fields,
                    'params' : params
                }
            )(),
            MaltegoTransformResponseMessage()
        )

        if isinstance(msg, MaltegoTransformResponseMessage):
            console_message(msg)
        elif isinstance(msg, basestring):
            raise MaltegoException(msg)
        else:
            raise MaltegoException('Could not resolve message type returned by transform.')
    except MaltegoException, me:
        croak(str(me))
    except ImportError:
        e = format_exc()
        croak(e)
    except Exception:
        e = format_exc()
        croak(e)
    except KeyboardInterrupt, be:
        if m is not None:
            m.onterminate()
#!/usr/bin/env python



from getpass import getuser
from os import path, sep, getcwd
from re import sub
from argparse import ArgumentParser
from sploitego.commands.common import write_template, read_template, cmd_name


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


parser = ArgumentParser(
    description='Creates a new transform in the specified directory and auto-updates __init__.py.',
    usage='sploitego %s <transform name> [options]' % cmd_name(__name__)
)

parser.add_argument(
    'transform',
    metavar='<transform name>',
    help='The name of the transform you wish to create.'
)

parser.add_argument(
    '-d',
    '--transform-dir',
    metavar='<dir>',
    help='The directory in which you wish to create the transform.',
    default=getcwd()
)


def help():
    parser.print_help()


def description():
    return parser.description


def parse_args(args):
    args = parser.parse_args(args)
    return args


def run(args):

    opts = parse_args(args)

    initf = sep.join([opts.transform_dir, '__init__.py'])
    transform = opts.transform
    directory = opts.transform_dir
    transformf = sep.join([directory, transform if transform.endswith('.py') else '%s.py' % transform ])

    if not path.exists(initf):
        print 'Directory %s does not appear to be a python package directory... quitting!' % repr(opts.transform_dir)
        exit(-1)
    if path.exists(transformf):
        print 'Transform %s already exists... quitting' % repr(transformf)
        exit(-1)

    values = {
        'author' : getuser(),
        'year' : 2012
    }

    write_template(
        transformf,
        read_template('newtransform', values)
    )

    print 'updating %s' % initf
    init = file(initf).read()

    with file(initf, mode='wb') as w:
        w.write(
            sub(
                r'__all__\s*\=\s*\[',
                '__all__ = [\n    %s,' % repr(transform),
                init
            )
        )

    print 'done!'

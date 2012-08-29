#!/usr/bin/env python



from os import path, sep, getcwd, unlink
from re import sub
from argparse import ArgumentParser
from sploitego.commands.common import   cmd_name


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


parser = ArgumentParser(
    description='Deletes a transform in the specified directory and auto-updates __init__.py.',
    usage='sploitego %s <transform name> [options]' % cmd_name(__name__)
)

parser.add_argument(
    'transform',
    metavar='<transform name>',
    help='The name of the transform you wish to delete.'
)

parser.add_argument(
    '-d',
    '--transform-dir',
    metavar='<dir>',
    help='The directory from which you wish to delete the transform.',
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
    transformf = sep.join([opts.transform_dir, transform if transform.endswith('.py') else '%s.py' % transform ])

    if not path.exists(initf):
        print 'Directory %s does not appear to be a python package directory... quitting!' % repr(opts.transform_dir)
        exit(-1)
    if not path.exists(transformf):
        print "Transform %s doesn't exists... quitting" % repr(transformf)
        exit(-1)

    print 'deleting transform %s...' % repr(transformf)
    unlink(transformf)

    print 'updating %s' % initf
    init = file(initf).read()

    with file(initf, mode='wb') as w:
        w.write(
            sub(
                r'\s*%s,?' % repr(transform),
                '',
                init
            )
        )

    print 'done!'

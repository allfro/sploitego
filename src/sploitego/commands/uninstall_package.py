#!/usr/bin/env python

import logging

from os import sep, path, mkdir, listdir, unlink, rmdir
from argparse import ArgumentParser
from sys import path as pypath
from sploitego.commands.common import detect_settings_dir, cmd_name

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


# Argument parser
parser = ArgumentParser(
    description="Uninstalls and unconfigures sploitego transform packages in Maltego's UI",
    usage='sploitego %s <package> [options]' % cmd_name(__name__)
)

parser.add_argument(
    'package',
    metavar='<package>',
    help='the name of the sploitego transforms package to uninstall.'
)
parser.add_argument(
    '-s',
    '--settings-dir',
    metavar='[settings dir]',
    default=detect_settings_dir,
    help='the path to the Maltego settings directory (automatically detected if excluded)'
)


def help():
    parser.print_help()


def description():
    return parser.description


def uninstall_transform(module, spec, prefix):

    installdir = sep.join([prefix, 'config', 'Maltego', 'TransformRepositories', 'Local'])

    if not path.exists(installdir):
        mkdir(installdir)

    setsdir = sep.join([prefix, 'config', 'Maltego', 'TransformSets'])

    for i,n in enumerate(spec.uuids):

        print 'Uninstalling transform %s from %s...' % (n, module)

        if spec.inputs[i][0] is not None:
            setdir = sep.join([setsdir, spec.inputs[i][0]])
            f = sep.join([setdir, n])
            if path.exists(f):
                unlink(f)
            if path.exists(setdir) and not listdir(setdir):
                rmdir(setdir)

        tf = sep.join([installdir, '%s.transform' % n])
        tsf = sep.join([installdir, '%s.transformsettings' % n])

        if path.exists(tf):
            unlink(tf)
        if path.exists(tsf):
            unlink(tsf)


def parse_args(args):
    args = parser.parse_args(args)
    if args.settings_dir is detect_settings_dir:
        args.settings_dir = detect_settings_dir()
    return args


def run(args):
    logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

    opts = parse_args(args)

    if not opts.package.endswith('.transforms'):
        opts.package = '%s.transforms' % opts.package

    if '' not in pypath:
        pypath.insert(0, '')

    m = __import__(opts.package, globals(), locals(), ['__all__'])

    for t in m.__all__:
        transform = '%s.%s' % (opts.package, t)
        m2 = __import__(transform, globals(), locals(), ['dotransform'])
        if hasattr(m2, 'dotransform') and hasattr(m2.dotransform, 'label'):
            uninstall_transform(
                m2.__name__,
                m2.dotransform,
                opts.settings_dir
            )

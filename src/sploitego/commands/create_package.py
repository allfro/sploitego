#!/usr/bin/env python

from os import path, sep
from argparse import ArgumentParser
from sploitego.commands.common import read_template, write_template, generate_all, build_skeleton, cmd_name
from getpass import getuser


__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


parser = ArgumentParser(
    description='Creates a Sploitego transform package skeleton.',
    usage='sploitego %s <package name>' % cmd_name(__name__)
)

parser.add_argument(
    'package',
    metavar='<package name>',
    help='The name of the sploitego package you wish to create.'
)


def write_setup(package_name, values):
    write_template(sep.join([package_name, 'setup.py']), read_template('setup', values))
    write_template(sep.join([package_name, 'README.md']), read_template('README', values))


def write_root(base, init):
    write_template(
        sep.join([base, '__init__.py']),
        init + generate_all('resources', 'transforms')
    )


def write_resources(package_name, resources, init, values):
    write_template(
        sep.join([resources, '__init__.py']),
        init + generate_all('etc', 'images')
    )

    write_template(
        sep.join([resources, 'etc', '__init__.py']),
        init
    )

    write_template(
        sep.join([resources, 'images', '__init__.py']),
        init
    )

    write_template(
        sep.join([resources, 'etc', '%s.conf' % package_name]),
        read_template('conf', values)
    )


def write_common(transforms, init, values):
    write_template(
        sep.join([transforms, '__init__.py']),
        init + generate_all('common', 'helloworld')
    )

    write_template(
        sep.join([transforms, 'helloworld.py']),
        read_template('transform', values)
    )

    write_template(
        sep.join([transforms, 'common', '__init__.py']),
        init + generate_all('entities')
    )

    write_template(
        sep.join([transforms, 'common', 'entities.py']),
        read_template('entities', values)
    )


def help():
    parser.print_help()


def run(args):

    opts = parser.parse_args(args)

    package_name = opts.package
    capitalized_package_name = package_name.capitalize()

    values = {
        'package' : package_name,
        'entity' : 'My%sEntity' % capitalized_package_name,
        'base_entity' : '%sEntity' % capitalized_package_name,
        'author' : getuser(),
        'year' : 2012,
        'project' : capitalized_package_name,
        'namespace' : package_name
    }

    base = sep.join([package_name, 'src', package_name])
    transforms = sep.join([base, 'transforms'])
    resources = sep.join([base, 'resources'])

    if not path.exists(package_name):
        print 'creating skeleton in %s' % package_name
        build_skeleton(
            package_name,
            [package_name, 'src'],
            [package_name, 'maltego'],
            base,
            transforms,
            [transforms, 'common'],
            resources,
            [resources, 'etc'],
            [resources, 'images']
        )
    else:
        print 'A directory with the name %s already exists... exiting' % package_name
        exit(-1)


    init = read_template('__init__', values)

    write_setup(package_name, values)

    write_root(base, init)

    write_resources(package_name, resources, init, values)

    write_common(transforms, init, values)

    print 'done!'
#!/usr/bin/env python

from sploitego.resource import conf
from re import findall, search, match, split
from ConfigParser import SafeConfigParser
from os import environ, getcwd, sep
from urlparse import urlsplit

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'SploitegoConfigParser',
    'config'
]


class SploitegoConfigParser(SafeConfigParser):

    def _interpolate_environment_variables(self, value):
        if isinstance(value, str):
            evs = self._get_env_vars(value)
            if evs:
                for ev in evs:
                    s = '${%s}' % ev
                    value = value.replace(s, environ[ev])
        return value

    def _interpolate(self, section, option, value, d):
        if isinstance(value, str):
            value = self._interpolate_environment_variables(value)
        elif isinstance(value, dict):
            for i in value:
                value[i] = self._interpolate_environment_variables(value[i])
        else:
            for i in range(0, len(value)):
                value[i] = self._interpolate_environment_variables(value[i])
        value = SafeConfigParser._interpolate(self, section, option, value, d)
        return value

    def _get_env_vars(self, value):
        return findall(r'\${(.+?)}', value)

    def __iadd__(self, other):
        self.add_section(other)
        return self

    def __isub__(self, other):
        self.remove_section(other)
        return self

    def __getitem__(self, item):
        section,option = item.split('/')
        value = self.get(section, option)
        if isinstance(value, basestring):
            if value.startswith('module:'):
                r = urlsplit(value.replace('module', 'http'))
                try:
                    v = r.path.lstrip('/')
                    m = __import__(r.netloc, globals(), locals(), [v])
                    value = m.__dict__[v]
                except ImportError:
                    pass
            elif match(r'^\d+$', value) is not None:
                value = int(value)
            elif match(r'^\d+\.\d+$', value) is not None:
                value = float(value)
            elif search(r'\s*(?<=[^\\]),+\s*', value) is not None:
                l = split(r'\s*(?<=[^\\]),+\s*', value)
                value = []
                for v in l:
                    if match(r'^\d+$', v) is not None:
                        v = int(v)
                    elif match(r'^\d+\.\d+$', v) is not None:
                        v = float(v)
                    else:
                        v = v.replace(r'\,', ',')
                    value.append(v)
            else:
                value = value.replace(r'\,', ',')
        return value

    def __setitem__(self, key, value):
        section,option = key.split('/')
        if not self.has_section(section):
            self.add_section(section)
        self.set(section, option, value)


config = SploitegoConfigParser()

dconf = sep.join([ conf ])
lconf = sep.join([ getcwd(), 'sploitego.conf' ])

config.read([ dconf , lconf ])
config.read(config['default/configs'])
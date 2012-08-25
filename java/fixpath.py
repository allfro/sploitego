#!/usr/bin/env python

from subprocess import Popen, PIPE
from os import system, path, symlink
from distutils.sysconfig import get_config_var

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

print 'Checking PATH of JVM and Sploitego...'

if not path.exists('JVMPathChecker.class') and system('javac JVMPathChecker.java'):
    print 'Error compiling the path checker using javac.'
    exit(-1)

s = Popen(['java', 'JVMPathChecker'], stdout=PIPE)
o = s.communicate()[0][:-1].split(path.pathsep)

bd = get_config_var('BINDIR')

if bd not in o:
    print "Warning %s not in your JVM's PATH" % bd

    while True:
        i = 0
        for i, c in enumerate(o):
            print '[%d]: %s' % (i, c)

        try:
            s = int(raw_input("Please select the path where you'd like to place symlinks to Sploitego's scripts [0]: "))
            if s <= i:
                for c in ['dispatcher', 'sploitego']:
                    srcf = path.join(bd, c)
                    dstf = path.join(o[s], c)
                    if not path.exists(srcf):
                        print 'Could not find %s in %s' % (repr(c), repr(bd))
                        exit(-1)
                    print 'symlinking %s to %s...' % (srcf, dstf)
                    symlink(srcf, dstf)
                exit(0)
            raise ValueError
        except ValueError:
            print 'Invalid selection... try again.'
else:
    print 'All looks good... no further action required here.'


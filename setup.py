from subprocess import PIPE, Popen
from setuptools import setup, find_packages
from sys import argv
from os import path, system, name, environ, pathsep, sep, symlink
from distutils.sysconfig import get_config_var

scripts = [
    'src/scripts/csv2sheets',
    'src/scripts/dispatcher',
    'src/scripts/mtgdebug',
    'src/scripts/mtginstall',
    'src/scripts/mtgsh',
    'src/scripts/mtguninstall',
    'src/scripts/mtgx2csv',
    'src/scripts/pymsfconsole',
    'src/scripts/pymsfrpc',
    'src/scripts/pyqtmsfconsole',
    'src/scripts/pysudo',
    'src/scripts/mtgtransgen',
    'src/scripts/mtgpkggen',
    'src/scripts/sploitego'
]

setup(
    name='sploitego',
    author='Nadeem Douba',
    version='1.0',
    author_email='ndouba@gmail.com',
    description='Rapid transform development and transform execution framework for Maltego.',
    license='GPL',
    packages=find_packages('src'),
    package_dir={ '' : 'src' },
    scripts=scripts,
    zip_safe=False,
    package_data={
        '' : [ '*.gif', '*.png', '*.conf', '*.plate' ]
    },
    install_requires=[
#        'easygui>=0.94',
#        'gnuplot-py>=1.8',
        'msgpack-python>=0.1.12',
#        'numpy==1.5.1',
        'pexpect>=2.4',
#        'pycrypto>=2.1',
#        'pylibpcap>=0.6.2',
        'readline>=6.2.2',
#        'scapy==2.1.0',
        'argparse'
    ],
    dependency_links=[
#        'http://www.secdev.org/projects/scapy/files/',
#        'http://sourceforge.net/projects/easygui/files/0.96/',
#        'http://sourceforge.net/projects/pylibpcap/files/pylibpcap/0.6.4/',
#        'http://libdnet.googlecode.com/files/'
    ]
)


if 'install' in argv:
    print 'Checking PATH of JVM and Sploitego...'

    if system('javac java/JVMPathChecker.java'):
        print 'Error compiling the path checker using javac.'
        exit(-1)

    proc = Popen(['java', '-cp', 'java', 'JVMPathChecker'], stdout=PIPE)
    jvm_path = proc.communicate()[0][:-1].split(':')

    bindir = get_config_var('BINDIR')

    if bindir not in jvm_path:
        print "Warning %s not in your JVM's PATH" % bindir

        while True:
            i = 0
            for i, path_dir in enumerate(jvm_path):
                print '[%d]: %s' % (i, path_dir)

            try:
                selection = int(raw_input("Please select the path where you'd like to place symlinks to Sploitego's scripts [0]: "))
                if selection <= i:
                    for script in scripts:
                        srcf = path.join(bindir, script)
                        dstf = path.join(jvm_path[selection], script)
                        if not path.exists(srcf):
                            print 'Could not find %s in %s' % (repr(script), repr(bindir))
                            exit(-1)
                        elif path.exists(dstf):
                            print 'skipping %s since it already exists in %s...' % (repr(script), repr(jvm_path[selection]))
                            continue
                        print 'symlinking %s to %s...' % (srcf, dstf)
                        symlink(srcf, dstf)
                    exit(0)
                raise ValueError
            except ValueError:
                print 'Invalid selection... try again.'
    else:
        print 'All looks good... no further action required here.'


from subprocess import PIPE, Popen
from setuptools import setup, find_packages
from sys import argv
from os import path, system, symlink, pathsep, name
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

extras = [
    'numpy',
    'pycrypto',
    'readline',
    'dnet'
]

if name == 'nt':
    scripts += ['%s.bat' % s for s in scripts]



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
        'easygui',
        'gnuplot-py>=1.8',
        'msgpack-python',
#        'numpy==1.5.1',
        'pexpect>=2.4',
#        'pycrypto>=2.1',
        'pylibpcap',
#        'readline',
        'scapy==2.1.0',
        'argparse'
    ],
    dependency_links=[
        'http://sourceforge.net/projects/easygui/files/0.96/easygui-0.96.tar.gz/download',
        'http://www.secdev.org/projects/scapy/files/',
        'http://sourceforge.net/projects/pylibpcap/files/pylibpcap/0.6.4/pylibpcap-0.6.4.tar.gz/download',
    ]
)


# Fixing Sploitego script path to work with JVM

if 'install' in argv:
    print '\nChecking PATH of JVM and Sploitego...'

    if not path.exists('java/JVMPathChecker.class') and system('javac java/JVMPathChecker.java'):
        print 'Error compiling the path checker using javac.'
        exit(-1)

    proc = Popen(['java', '-cp', 'java', 'JVMPathChecker'], stdout=PIPE)
    jvm_path = proc.communicate()[0][:-1].split(pathsep)

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



print '\nChecking if other dependencies installed...'

for e in extras:
    try:
        __import__(e)
    except ImportError:
        print 'WARNING: Package %s not installed. Please download and manually install this package' % repr(e)

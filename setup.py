from setuptools import setup, find_packages
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
    'src/scripts/pysetuid'
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
        '' : [ '*.gif', '*.png', '*.conf' ]
    },
    install_requires=[
        'easygui>=0.94',
        'gnuplot-py>=1.8',
        'msgpack-python>=0.1.12',
        'numpy==1.5.1',
        'pexpect>=2.4',
        'pycrypto>=2.1',
        'pylibpcap>=0.6.2',
        'readline>=6.2.2',
        'scapy==2.1.0'
    ],
    dependency_links=[
        'http://www.secdev.org/projects/scapy/files/',
        'http://sourceforge.net/projects/easygui/files/0.96/',
        'http://sourceforge.net/projects/pylibpcap/files/pylibpcap/0.6.4/',
        'http://libdnet.googlecode.com/files/'
    ],
    extras_require={
        'msf' : [ 'sip', 'PyQt4' ],
        'scapy' : [ 'libdnet' ]
    }
)

if name == 'posix' and system('which mtginstall'):
    print 'Sploitego scripts are not in your path... fixing that!'
    script_dir = get_config_var('BINDIR')
    paths = [ path.realpath(p) for p in environ['PATH'].split(pathsep) ]

    for dst in ['/usr/local/bin', '/opt/local/bin', '/usr/bin']:
        if dst in paths:
            print 'Creating symlinks to scripts in the %s directory' % dst
            for s in scripts:
                dstf = sep.join([dst, s])
                if not path.exists(dstf):
                    srcf = sep.join([script_dir, path.basename(s)])
                    print 'Symbolically linking %s -> %s' % (srcf, dstf)
                    symlink(srcf, dstf)
            break
    print 'Fixed the problem... have fun!'


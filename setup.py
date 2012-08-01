from setuptools import setup, find_packages
from os import path, system, name, environ, pathsep, sep, listdir, chown, chmod
from shutil import copyfile

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
    script_dir = sep.join([path.dirname(path.realpath(__file__)), 'src', 'scripts'])
    scripts = listdir(script_dir)
    paths = [ path.realpath(p) for p in environ['PATH'].split(pathsep) ]

    for dst in ['/opt/local/bin', '/usr/local/bin', '/usr/bin']:
        if dst in paths:
            print 'Copying scripts to the %s directory' % dst
            for s in scripts:
                srcf = sep.join([script_dir, s])
                dstf = sep.join([dst, s])
                print 'Copying %s -> %s' % (srcf, dstf)
                copyfile(srcf, dstf)
                chown(dstf, 0, 0)
                chmod(dstf, 0755)
            break
    print 'Fixed the problem... have fun!'


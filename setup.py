from setuptools import setup, find_packages

setup(
    name='sploitego',
    author='Nadeem Douba',
    version='1.0',
    author_email='ndouba@gmail.com',
    description='Rapid transform development and transform execution framework for Maltego.',
    license='GPL',
    packages=find_packages('src'),
    package_dir={ '' : 'src' },
    scripts=[
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
    ],
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
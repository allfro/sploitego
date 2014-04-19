# !/usr/bin/env python

import sys

sys.path.insert(0, 'src')

import sploitego

from setuptools import setup, find_packages, os

scripts = [
    'src/scripts/qtmsfconsole'
]

if os.name == 'nt':
    scripts += ['%s.bat' % s for s in scripts]

setup(
    name='sploitego',
    author='Nadeem Douba',
    version=sploitego.__version__,
    author_email='ndouba@gmail.com',
    description='Penetration testing transforms for Maltego.',
    license='GPL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    scripts=scripts,
    zip_safe=False,
    package_data={
        '': ['*.gif', '*.png', '*.conf', '*.mtz', '*.machine']
    },
    install_requires=[
        'scapy==2.1.0',
        'pynessusrpc',
        'pyiptools',
        'canari',
        'dnspython',
        'lxml'
    ],
    dependency_links=[
        'http://www.secdev.org/projects/scapy/files/'
    ]
)

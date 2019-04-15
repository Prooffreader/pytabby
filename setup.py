#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""setup.py for tabbedshellmenus"""

from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    """Reads file"""
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='tabbedshellmenus',
    version='0.0.1-dev',
    license='MIT',
    description='A simple, nonopinionated python shell menu system WITH TABS',
    long_description='%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.rst'))
    ),
    author='David Taylor',
    author_email='prooffreader@gmail.com',
    url='http://github.com/Prooffreader/tabbedshellmenus',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list:
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    keywords=[
        'python', 'shell', 'terminal', 'tabs', 'tabbed', 'menu', 'menus'
    ],
    install_requires=[
        'PyYAML==5.1', 'schema==0.7.0'
    ],
    extras_require={
    },
    entry_points={
        'console_scripts': [
            'tabbedshellmenus = tabbedshellmenus.cli:main',
        ]
    },
)

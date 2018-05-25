#!/usr/bin/env python

import re

from pathlib import Path
from setuptools import find_packages, setup

rel = Path(__file__).parent

with open(str(rel / 'README.rst')) as handler:
    README = handler.read()

with open(str(rel / 'aiohttp_middlewares' / '__init__.py')) as handler:
    INIT_PY = handler.read()

VERSION = re.findall("__version__ = '([^']+)'", INIT_PY)[0]


setup(
    name='aiohttp-middlewares',
    version=VERSION,
    description='Collection of useful middlewares for aiohttp appliactions',
    long_description=README,
    author='Igor Davydenko',
    author_email='playpauseandstop@gmail.com',
    url='http://github.com/playpauseandstop/aiohttp-middlewares',
    packages=find_packages(),
    install_requires=[
        'aiohttp>=2.0,<4.0',
        'async-timeout>=1.2,<4.0',
    ],
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'License :: OSI Approved :: BSD License',
    ],
    keywords='aiohttp middlewares',
    license='BSD License',
)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiohttp_middlewares']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.5,<4.0', 'async-timeout>=1.2,<4']

setup_kwargs = {
    'name': 'aiohttp-middlewares',
    'version': '0.2.0a1',
    'description': 'Collection of useful middlewares for aiohttp applications.',
    'long_description': '===================\naiohttp-middlewares\n===================\n\n.. image:: https://img.shields.io/circleci/project/github/playpauseandstop/aiohttp-middlewares/master.svg\n    :target: https://circleci.com/gh/playpauseandstop/aiohttp-middlewares\n    :alt: CircleCI\n\n.. image:: https://img.shields.io/pypi/v/aiohttp-middlewares.svg\n    :target: https://pypi.org/project/aiohttp-middlewares/\n    :alt: Latest Version\n\n.. image:: https://img.shields.io/pypi/pyversions/aiohttp-middlewares.svg\n    :target: https://pypi.org/project/aiohttp-middlewares/\n    :alt: Python versions\n\n.. image:: https://img.shields.io/pypi/l/aiohttp-middlewares.svg\n    :target: https://github.com/playpauseandstop/aiohttp-middlewares/blob/master/LICENSE\n    :alt: BSD License\n\n.. image:: https://coveralls.io/repos/playpauseandstop/aiohttp-middlewares/badge.svg?branch=master&service=github\n    :target: https://coveralls.io/github/playpauseandstop/aiohttp-middlewares\n    :alt: Coverage\n\n.. image:: https://readthedocs.org/projects/aiohttp-middlewares/badge/?version=latest\n    :target: http://aiohttp-middlewares.readthedocs.org/en/latest/\n    :alt: Documentation\n\nCollection of useful middlewares for `aiohttp <http://aiohttp.readthedocs.org/>`_\napplications.\n\n- Works on Python 3.5+\n- Works with aiohttp 3.5+\n- BSD licensed\n- Latest documentation `on Read The Docs\n  <https://aiohttp-middlewares.readthedocs.io/>`_\n- Source, issues, and pull requests `on GitHub\n  <https://github.com/playpauseandstop/aiohttp-middlewares>`_\n',
    'author': 'Igor Davydenko',
    'author_email': 'iam@igordavydenko.com',
    'url': 'https://igordavydenko.com/projects.html#aiohttp-middlewares',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5.3,<4.0.0',
}


setup(**setup_kwargs)

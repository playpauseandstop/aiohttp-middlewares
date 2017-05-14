===================
aiohttp-middlewares
===================

.. image:: https://img.shields.io/circleci/project/playpauseandstop/aiohttp-middlewares/master.svg?maxAge=2592000
    :target: https://circleci.com/gh/playpauseandstop/aiohttp-middlewares
    :alt: CircleCI

.. image:: https://img.shields.io/pypi/v/aiohttp-middlewares.svg
    :target: https://pypi.org/project/aiohttp-middlewares/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/aiohttp-middlewares.svg
    :target: https://pypi.org/project/aiohttp-middlewares/
    :alt: Python versions

.. image:: https://img.shields.io/pypi/l/aiohttp-middlewares.svg
    :target: https://github.com/playpauseandstop/aiohttp-middlewares/blob/master/LICENSE
    :alt: BSD License

.. image:: https://coveralls.io/repos/playpauseandstop/aiohttp-middlewares/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/playpauseandstop/aiohttp-middlewares
    :alt: Coverage

Collection of useful middlewares for `aiohttp <http://aiohttp.readthedocs.org/>`_
applications.

List of middlewares
===================

Timeout
-------

Do not allow request handling exceed X seconds.

.. code-block:: python

    from aiohttp import web
    from aiohttp_middlewares import timeout_middleware

    app = web.Application(
        middlewares=[timeout_middleware(29.5, ignore={'/slow-url'})])

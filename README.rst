===================
aiohttp-middlewares
===================

.. image:: https://img.shields.io/circleci/project/playpauseandstop/aiohttp-middlewares/master.svg?maxAge=2592000
    :target: https://circleci.com/gh/playpauseandstop/aiohttp-middlewares
    :alt: CircleCI

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
    from aiohttp_middlewares import timeout_middleware_factory

    app = web.Application(
        middlewares=[
            timeout_middleware_factory(29.5, ignore=['/slow-url']),
        ])

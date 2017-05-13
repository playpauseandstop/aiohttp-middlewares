===================
aiohttp-middlewares
===================

Collection of useful middlewares for `aiohttp <http://aiohttp.readthedocs.org/>`_
applications.

List of middlewares
===================

Timeout
-------

Do not allow request handling exceed X seconds.

::

    from aiohttp import web
    from aiohttp_middlewares import timeout_middleware_factory

    app = web.Application(
        middlewares=[
            timeout_middleware_factory(29.5, ignore=['/slow-url']),
        ])

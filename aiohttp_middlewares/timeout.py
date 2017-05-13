"""
===========================
aiohttp_middlewares.timeout
===========================

Middleware to ensure that request handling does not exceeds X seconds.

Usage
=====

::

    from aiohttp import web
    from aiohttp_middlewares import (
        error_middleware_factory,
        timeout_middleware_factory,
    )

    # Basic usage
    app = web.Application(
        middlewares=[timeout_middleware_factory(29.5)])

    # Ignore slow responses from list of urls
    slow_urls = ('/slow-url', '/very-slow-url', '/very/very/slow/url')
    app = web.Application(
        middlewares=[timeout_middleware_factory(4.5, slow_urls)])

    # Handle timeout errors with error middleware
    app = web.Application(
        middlewares=[
            error_middleware_factory(),
            timeout_middleware_factory(14.5),
        ])

"""

import logging

from typing import Union

from aiohttp import web
from async_timeout import timeout

from .types import Handler, Middleware, StrCollection


logger = logging.getLogger(__name__)


def timeout_middleware_factory(seconds: Union[int, float],
                               ignore: StrCollection=None) -> Middleware:
    """Ensure that request handling does not exceed X seconds.

    This is helpful when aiohttp application served behind nginx or other
    reverse proxy with enabled read timeout. And when this read timeout exceeds
    reverse proxy generates error page instead of aiohttp app, which may result
    in bad user experience.

    For best results, please do not supply seconds value which equals read
    timeout value at reverse proxy as it may results that request handling at
    aiohttp will be ended after reverse proxy already responded with 504 error.
    Timeout context manager accepts floats, so if nginx has read timeout in
    30 seconds, it's ok to configure timeout middleware to raise timeout error
    after 29.5 seconds. In that case in most cases user for sure will see the
    error from aiohttp app instead of reverse proxy.

    Notice that timeout middleware just raised ``asyncio.Timeout`` in case of
    exceeding seconds per request, but not handling the error by itself. If you
    need to handle this error, please place ``error_middleware_factory`` in
    list of application middlewares as well. Error middleware should be placed
    before timeout middleware, so timeout errors can be catched and processed
    properly.

    In case if you need to "disable" timeout middleware for given request path,
    please supply ignore sequence as second positional argument, like::

        from aiohttp import web

        app = web.Application(
            middlewares=[timeout_middleware_factory(14.5, {'/slow-url'})],
        )

    Behind the scene, when current request path match the URL from ignore
    sequence timeout context manager will be configured to avoid break the
    execution after X seconds.
    """
    async def middleware_factory(app: web.Application,
                                 handler: Handler) -> Handler:
        """Actual timeout middleware factory."""
        async def middleware(request: web.Request) -> web.Response:
            """Wrap request handler into timeout context manager."""
            actual_seconds = seconds
            request_path = request.rel_url.path

            if request_path in (ignore or set()):
                logger.debug(
                    'Ignore {0} from timeout handling'.format(request_path))
                actual_seconds = .0

            with timeout(actual_seconds):
                return await handler(request)
        return middleware
    return middleware_factory

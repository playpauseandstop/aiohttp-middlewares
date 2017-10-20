"""
=============
aiohttp.https
=============

Change scheme for current request when aiohttp application deployed behind
reverse proxy with HTTPS enabled.

Usage
=====

::

    from aiohttp import web
    from aiohttp_middlewares import https_middleware

    # Basic usage
    app = web.Application(middlewares=[https_middleware()])

    # Specify custom headers to match, not `X-Forwarded-Proto: https`
    app = web.Application(
        middlewares=https_middleware({'Forwarded': 'https'}))

"""

import logging

from aiohttp import web

from .types import Handler, Middleware, StrDict
from .utils import get_aiohttp_version


DEFAULT_MATCH_HEADERS = {'X-Forwarded-Proto': 'https'}

logger = logging.getLogger(__name__)


def https_middleware(match_headers: StrDict=None) -> Middleware:
    """
    Change scheme for current request when aiohttp application deployed behind
    reverse proxy with HTTPS enabled.

    This middleware is required to use, when your aiohttp app deployed behind
    nginx with HTTPS enabled, after aiohttp discounted
    ``secure_proxy_ssl_header`` keyword argument in
    https://github.com/aio-libs/aiohttp/pull/2299.

    :param match_headers:
        Dict of header(s) from reverse proxy to specify that aiohttp run behind
        HTTPS. By default: ``{'X-Forwarded-Proto': 'https'}``
    """
    async def factory(app: web.Application, handler: Handler) -> Handler:
        """Actual HTTPS middleware factory."""
        async def middleware(request: web.Request) -> web.Response:
            """Change scheme of current request when HTTPS headers matched."""
            headers = DEFAULT_MATCH_HEADERS
            if match_headers is not None:
                headers = match_headers

            if get_aiohttp_version() < (2, 3):
                if len(headers) > 1:  # pragma: no cover
                    logger.warning(
                        'aiohttp <= 2.2 does not support multiple headers '
                        'for _secure_proxy_ssl_header attr',
                        extra={'headers': 'headers'})
                if headers:
                    request._secure_proxy_ssl_header = (
                        tuple(headers.items())[0])
            else:
                matched = any(
                    request.headers.get(key) == value
                    for key, value in headers.items())

                if matched:
                    logger.debug(
                        'Substitute request URL scheme to https',
                        extra={
                            'headers': headers,
                            'request_headers': dict(request.headers),
                        })
                    request = request.clone(scheme='https')

            return await handler(request)
        return middleware
    return factory

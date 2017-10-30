"""
==========================
aiohttp_middlewares.shield
==========================

Middleware to shield application handlers by method or URL.

Usage
=====

::

    from aiohttp import web
    from aiohttp_middlewares import NON_IDEMPOTENT_METHODS, shield_middleware

    # Basic usage (shield by handler method)
    app = web.Application(
        middlewares=[shield_middleware(methods=IDEMPOTENT_METHODS)])

    # Shield by handler URL
    app = web.Application(
        middlewares=[shield_middleware(urls=['/', '/about-us'])])

    # Shield by handler method, but ignore shielding list of URLs
    app = web.Application(
        middlewares=[
            shield_middleware(
                methods=NON_IDEMPOTENT_METHODS,
                ignore={'/api/documents', '/api/comments'})])

    # Combine shielding by method and URL
    SHIELD_URLS = {
        '/api/documents': ['POST', 'DELETE'],
        re.compile('/api/documents/\d+'): ['DELETE', 'PUT', 'PATCH'],
    }
    app = web.Application(
        middlewares=[shield_middleware(urls=SHIELD_URLS)])

"""

import asyncio
import logging

from aiohttp import web

from .types import Handler, Middleware, StrCollection, Urls
from .utils import match_request


logger = logging.getLogger(__name__)


def shield_middleware(*,
                      methods: StrCollection=None,
                      urls: Urls=None,
                      ignore: Urls=None) -> Middleware:
    """Ensure that handler execution would not break on ``CancelledError``.

    Shielding handlers allow to avoid breaking handler execution on
    ``CancelledError`` (this happens for example while client closes
    conneciton, but server still not ready to fullify response).

    In most cases you need to shield non-idempotent methods (``POST``, ``PUT``,
    ``PATCH``, ``DELETE``) and ignore shielding idempotent ``GET``, ``HEAD``,
    ``OPTIONS`` and ``TRACE`` requests.

    More about shielding coroutines in official Python docs,
    https://docs.python.org/3/library/asyncio-task.html#asyncio.shield

    Other possibility to allow shielding request handlers by URLs dict. In that
    case  order of dict keys is necessary as they will be processed from first
    to last added. In Python 3.6+ you can supply standard ``dict`` here, in
    Python 3.5 please supply ``collections.OrderedDict`` instance instead.

    To shield all non-idempotent methods you need to::

        from aiohttp import web

        app = web.Application(
            middlewares=shield_middleware(methods=NON_IDEMPOTENT_METHODS))

    To shield all non-idempotent methods and ``GET`` requests to
    ``/downloads/*`` URLs::

        import re

        app = web.Application(
            middlewares=shield_middleware(urls={
                re.compile(r'^/downloads/.*$'): 'GET',
                re.compile(r'.*'): NON_IDEMPOTENT_METHODS,
            }))

    :param methods:
        Methods to shield. Use ``aiohttp_middlewares.IDEMPOTENT_METHODS`` to
        shield requests to all idempotent methods (``POST``, ``PUT``,
        ``PATCH``, ``DELETE``). Do not mix with ``urls``.
    :param urls:
        URLs to shield. Supports passing collection of strings or regexps or
        dict where key is a string or regexp and value is a method or
        collection of methods to shield. Do not mix with ``methods``.
    :param ignore:
        When ``methods`` specified ignore next collection of URL strings or
        regexps from shielding. Do not mix with ``urls``.
    """
    if not methods and not urls:
        raise ValueError('None of methods or urls argument passed.')
    if methods and urls:
        raise ValueError(
            'Both methods and urls arguments passed, while only one expected.')
    if urls and ignore:
        raise ValueError('Unable to mix urls and ignore arguments.')

    # Lower case methods to shield (if any)
    methods_to_shield = {item.lower() for item in methods or []}

    async def factory(app: web.Application, handler: Handler) -> Handler:
        """Actual shield middleware factory."""
        async def middleware(request: web.Request) -> web.Response:
            """Shield handler execution if necessary."""
            request_method = request.method.lower()
            request_path = request.rel_url.path
            log_extra = {'method': request.method, 'path': request_path}

            # First attempt to process methods to shield
            if methods_to_shield:
                if request_method not in methods_to_shield:
                    return await handler(request)

                if (
                    ignore and
                    match_request(ignore, request_method, request_path)
                ):
                    logger.debug(
                        'Ignore path from handler shielding.',
                        extra=log_extra)
                    return await handler(request)

                logger.debug(
                    'Activate shield middleware by matched method',
                    extra=log_extra)
                return await asyncio.shield(handler(request))

            # Then attempt to shield handler by URLs collection / mapping
            if urls and match_request(urls, request_method, request_path):
                logger.debug(
                    'Activate shield middleware by matched path',
                    extra=log_extra)
                return await asyncio.shield(handler(request))
            return await handler(request)
        return middleware
    return factory

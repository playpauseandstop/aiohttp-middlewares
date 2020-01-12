r"""
================
Error Middleware
================

.. versionadded:: 0.2.0

Middleware to handle errors in aiohttp applications.

Usage
=====

.. code-block:: python

    import re

    from aiohttp import web
    from aiohttp_middlewares import (
        default_error_handler,
        error_context,
        error_middleware,
    )

    # Error handler for API requests
    async def api_error(request: web.Request) -> web.Response:
        with error_context(request) as context:
            return web.json_response(context.data, status=context.status)

    # Basic usage (default error handler for whole application)
    app = web.Application(middlewares=[error_middleware()])

    # Advanced usage (multiple error handlers for different
    # application parts)
    app = web.Application(
        middlewares=[
            error_middleware(
                default_handler=default_error_handler,
                config={re.compile(r"^\/api"): api_error}
            )
        ]
    )

    # Ignore aiohttp.web HTTP Not Found errors from handling via middleware
    app = web.Application(
        middlewares=[error_middleware(ignore_exceptions=web.HTTPNotFound)]
    )

"""

import logging
from contextlib import contextmanager
from typing import Dict, Iterator, Optional, Tuple, Union

import attr
from aiohttp import web

from .annotations import DictStrAny, ExceptionType, Handler, Middleware, Url
from .utils import match_path


DEFAULT_EXCEPTION = Exception("Unhandled aiohttp-middlewares exception.")
REQUEST_ERROR_KEY = "error"

Config = Dict[Url, Handler]
logger = logging.getLogger(__name__)


@attr.dataclass(frozen=True, slots=True)
class ErrorContext:
    """Context with all necessary data about the error."""

    err: Exception
    message: str
    status: int
    data: DictStrAny


async def default_error_handler(request: web.Request) -> web.Response:
    """Default error handler to respond with JSON error details.

    If, for example, ``aiohttp.web`` view handler raises
    ``ValueError("wrong value")`` exception, default error handler will produce
    JSON response of 500 status with given content:

    .. code-block:: json

        {
            "detail": "wrong value"
        }

    And to see the whole exception traceback in logs you need to enable
    ``aiohttp_middlewares`` in logging config.

    .. versionadded:: 1.0.0
    """
    with error_context(request) as context:
        logger.error(context.message, exc_info=True)
        return web.json_response(context.data, status=context.status)


@contextmanager
def error_context(request: web.Request) -> Iterator[ErrorContext]:
    """Context manager to retrieve error data inside of error handler (view).

    The context will contain:

    - Error itself
    - Error message (by default: ``str(err)``)
    - Error status (by default: ``500``)
    - Error data dict (by default: ``{"detail": str(err)}``)
    """
    err = get_error_from_request(request)

    message = getattr(err, "message", None) or str(err)
    data = getattr(err, "data", None) or {"detail": message}
    status = getattr(err, "status", None) or 500

    yield ErrorContext(err=err, message=message, status=status, data=data)


def error_middleware(
    *,
    default_handler: Handler = default_error_handler,
    config: Config = None,
    ignore_exceptions: Union[ExceptionType, Tuple[ExceptionType, ...]] = None
) -> Middleware:
    """Middleware to handle exceptions in aiohttp applications.

    To catch all possible errors, please put this middleware on top of your
    ``middlewares`` list (**but after CORS middleware if it used**) as:

    .. code-block:: python

        from aiohttp import web
        from aiohttp_middlewares import error_middleware, timeout_middleware

        app = web.Application(
            midllewares=[
                error_middleware(...),
                timeout_middleware(...)
            ]
        )

    :param default_handler:
        Default handler to called on error catched by error middleware.
    :param config:
        When application requires multiple error handlers, provide mapping in
        format ``Dict[Url, Handler]``, where ``Url`` can be an exact string
        to match path or regex and ``Handler`` is a handler to be called when
        ``Url`` matches current request path if any.
    :param ignore_exceptions:
        Do not process given exceptions via error middleware.
    """

    @web.middleware
    async def middleware(
        request: web.Request, handler: Handler
    ) -> web.StreamResponse:
        try:
            return await handler(request)
        except Exception as err:
            if ignore_exceptions and isinstance(err, ignore_exceptions):
                raise err

            set_error_to_request(request, err)
            error_handler = (
                get_error_handler(request, config) or default_handler
            )
            return await error_handler(request)

    return middleware


def get_error_from_request(request: web.Request) -> Exception:
    """Get previously stored error from request dict.

    Return default exception if nothing stored before.
    """
    return request.get(REQUEST_ERROR_KEY) or DEFAULT_EXCEPTION


def get_error_handler(
    request: web.Request, config: Optional[Config]
) -> Optional[Handler]:
    """Find error handler matching current request path if any."""
    if not config:
        return None

    path = request.rel_url.path
    for item, handler in config.items():
        if match_path(item, path):
            return handler

    return None


def set_error_to_request(request: web.Request, err: Exception) -> Exception:
    """Store catched error to request dict."""
    request[REQUEST_ERROR_KEY] = err
    return err

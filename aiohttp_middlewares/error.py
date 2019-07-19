"""
================
Error Middleware
================

Middleware to handle errors in aiohttp applications.

Usage
=====

.. code-block:: python

    import re

    from aiohttp import web
    from aiohttp_middlewares import error_context, error_middleware

    # Default error handler
    async def error(request: web.Request) -> web.Response:
        with error_context(request) as context:
            return web.Response(
                text=context.message,
                status=context.status,
                content_type="text/plain"
            )

    # Error handler for API requests
    async def api_error(request: web.Request) -> web.Response:
        with error_context(request) as context:
            return web.json_response(context.data, status=context.status)

    # Basic usage (one error handler for whole application)
    app = web.Application(
        middlewares=[
            error_middleware(default_handler=api_error)
        ]
    )

    # Advanced usage (multiple error handlers for different application parts)
    app = web.Application(
        middlewares=[
            error_middleware(
                default_handler=error,
                config={re.compile(r"^/api"): api_error}
            )
        ]
    )

"""

from contextlib import contextmanager
from typing import Dict, Iterator, Optional

import attr
from aiohttp import web
from aiohttp.web_middlewares import _Handler, _Middleware

from .annotations import DictStrAny, Url
from .utils import match_path


DEFAULT_EXCEPTION = Exception("Unhandled aiohttp-middlewares exception.")
IGNORE_LOG_STATUSES = (400, 404, 422)
ERROR_REQUEST_KEY = "error"

Config = Dict[Url, _Handler]


@attr.dataclass
class ErrorContext:
    """Context with all necessary data about the error."""

    err: Exception
    message: str
    status: int
    data: DictStrAny


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
    *, default_handler: _Handler, config: Config = None
) -> _Middleware:
    """Middleware to handle exceptions in aiohttp applications.

    To catch all possible errors, please put this middleware on top of your
    ``middlewares`` list as:

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
        format ``Dict[Url, _Handler]``, where ``Url`` can be an exact string
        to match path or regex and ``_Handler`` is a handler to be called when
        ``Url`` matches current request path if any.
    """

    @web.middleware
    async def middleware(
        request: web.Request, handler: _Handler
    ) -> web.StreamResponse:
        try:
            return await handler(request)
        except Exception as err:
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
    return request.get(ERROR_REQUEST_KEY) or DEFAULT_EXCEPTION


def get_error_handler(
    request: web.Request, config: Optional[Config]
) -> Optional[_Handler]:
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
    request[ERROR_REQUEST_KEY] = err
    return err

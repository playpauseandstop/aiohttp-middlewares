"""
=========================
aiohttp_middlewares.types
=========================

Type annotation shortcuts for the project.

"""

from typing import Awaitable, Callable

from aiohttp import web


Handler = Callable[[web.Request], web.Response]
Middleware = Callable[[web.Application, Handler], Awaitable[Handler]]

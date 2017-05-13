"""
=========================
aiohttp_middlewares.types
=========================

Type annotation shortcuts for the project.

"""

from typing import Awaitable, Callable, List, Set, Tuple, Union

from aiohttp import web


StrCollection = Union[List[str], Set[str], Tuple[str, ...]]

Handler = Callable[[web.Request], web.Response]
Middleware = Callable[[web.Application, Handler], Awaitable[Handler]]

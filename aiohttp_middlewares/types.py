"""
=========================
aiohttp_middlewares.types
=========================

Type annotation shortcuts for the project.

"""

from typing import Awaitable, Callable, Dict, List, Set, Tuple, Union

from aiohttp import web


StrCollection = Union[List[str], Set[str], Tuple[str, ...]]
StrDict = Dict[str, str]
Urls = Union[StrCollection, Dict[str, Union[StrCollection, str]]]

Handler = Callable[[web.Request], web.Response]
Middleware = Callable[[web.Application, Handler], Awaitable[Handler]]

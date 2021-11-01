"""
===============================
aiohttp_middlewares.annotations
===============================

Type annotation shortcuts for ``aiohttp_middlewares`` library.

"""

from typing import (
    Any,
    Awaitable,
    Callable,
    Collection,
    Dict,
    Pattern,
    Type,
    Union,
)

from aiohttp import web
from aiohttp.web_middlewares import _Middleware as Middleware
from yarl import URL


# Make flake8 happy
(Middleware,)

DictStrAny = Dict[str, Any]
DictStrStr = Dict[str, str]

ExceptionType = Type[Exception]
# FIXME: Drop Handler type definition after `aiohttp-middlewares` will require
# only `aiohttp>=3.8.0`
Handler = Callable[[web.Request], Awaitable[web.StreamResponse]]

IntCollection = Collection[int]
StrCollection = Collection[str]

Url = Union[str, Pattern[str], URL]
UrlCollection = Collection[Url]
UrlDict = Dict[Url, StrCollection]
Urls = Union[UrlCollection, UrlDict]

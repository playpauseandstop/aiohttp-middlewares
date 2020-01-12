"""
===============================
aiohttp_middlewares.annotations
===============================

Type annotation shortcuts for ``aiohttp_middlewares`` library.

"""

from typing import Any, Collection, Dict, Pattern, Type, Union

from aiohttp.web_middlewares import _Handler, _Middleware
from yarl import URL


DictStrAny = Dict[str, Any]
DictStrStr = Dict[str, str]

ExceptionType = Type[Exception]
Handler = _Handler
Middleware = _Middleware

IntCollection = Collection[int]
StrCollection = Collection[str]

Url = Union[str, Pattern[str], URL]
UrlCollection = Collection[Url]
UrlDict = Dict[Url, StrCollection]
Urls = Union[UrlCollection, UrlDict]

"""
===============================
aiohttp_middlewares.annotations
===============================

Type annotation shortcuts for ``aiohttp_middlewares`` library.

"""

import re  # noqa: TC003
from collections.abc import Collection
from typing import Any, TypeAlias

from aiohttp.typedefs import Handler, Middleware
from yarl import URL  # noqa: TC002

__all__ = (
    # 1st party imports
    "DictStrAny",
    "DictStrStr",
    "ExceptionType",
    "IntCollection",
    "StrCollection",
    "Url",
    "UrlCollection",
    "UrlDict",
    "Urls",
    # 3rd party imports
    "Handler",
    "Middleware",
)

DictStrAny: TypeAlias = dict[str, Any]
DictStrStr: TypeAlias = dict[str, str]

ExceptionType: TypeAlias = type[Exception]

IntCollection = Collection[int]
StrCollection = Collection[str]

Url: TypeAlias = str | re.Pattern[str] | URL
UrlCollection: TypeAlias = Collection[Url]
UrlDict = dict[Url, StrCollection]
Urls = UrlCollection | UrlDict

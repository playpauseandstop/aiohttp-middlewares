"""
===============================
aiohttp_middlewares.annotations
===============================

Type annotation shortcuts for ``aiohttp_middlewares`` library.

"""

from typing import Any, Dict, FrozenSet, List, Set, Tuple, Union
from typing.re import Pattern


DictStrAny = Dict[str, Any]
DictStrStr = Dict[str, str]

IntCollection = Union[List[int], FrozenSet[int], Set[int], Tuple[int, ...]]
StrCollection = Union[List[str], FrozenSet[str], Set[str], Tuple[str, ...]]

Url = Union[str, Pattern]
UrlCollection = Union[List[Url], Set[Url], Tuple[Url, ...]]
UrlDict = Dict[Url, Union[StrCollection, str]]
Urls = Union[UrlCollection, UrlDict]

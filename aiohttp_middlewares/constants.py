"""
=============================
aiohttp_middlewares.constants
=============================

Collection of constants for ``aiohttp_middlewares`` project.

"""

#: Set of idempotent HTTP methods
IDEMPOTENT_METHODS = frozenset({'GET', 'HEAD', 'OPTIONS', 'TRACE'})

#: Set of non-idempotent HTTP methods
NON_IDEMPOTENT_METHODS = frozenset({'DELETE', 'PATCH', 'POST', 'PUT'})

"""
===================
aiohttp_middlewares
===================

Collection of useful middlewares for aiohttp applications.

"""

__version__ = '0.1.0a2'

from .timeout import timeout_middleware

# Make flake8 happy
(
    timeout_middleware,
)

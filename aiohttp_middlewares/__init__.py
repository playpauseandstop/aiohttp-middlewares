"""
===================
aiohttp_middlewares
===================

Collection of useful middlewares for aiohttp applications.

"""

__version__ = '0.1.0b1'

from .https import https_middleware
from .timeout import timeout_middleware

# Make flake8 happy
(
    https_middleware,
    timeout_middleware,
)

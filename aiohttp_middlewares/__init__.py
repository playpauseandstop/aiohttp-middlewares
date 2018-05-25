"""
===================
aiohttp_middlewares
===================

Collection of useful middlewares for aiohttp applications.

"""

__version__ = '0.1.1'

from .constants import IDEMPOTENT_METHODS, NON_IDEMPOTENT_METHODS
from .https import https_middleware
from .shield import shield_middleware
from .timeout import timeout_middleware

# Make flake8 happy
(
    https_middleware,
    IDEMPOTENT_METHODS,
    NON_IDEMPOTENT_METHODS,
    shield_middleware,
    timeout_middleware,
)

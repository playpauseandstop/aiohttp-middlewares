"""
===========
Middlewares
===========

Collection of useful middlewares for aiohttp applications.

"""

__version__ = "1.0.0a0"

from .constants import IDEMPOTENT_METHODS, NON_IDEMPOTENT_METHODS
from .cors import cors_middleware
from .error import error_context, error_middleware
from .https import https_middleware
from .shield import shield_middleware
from .timeout import timeout_middleware
from .utils import match_path

# Make flake8 happy
(
    cors_middleware,
    error_context,
    error_middleware,
    https_middleware,
    IDEMPOTENT_METHODS,
    match_path,
    NON_IDEMPOTENT_METHODS,
    shield_middleware,
    timeout_middleware,
)

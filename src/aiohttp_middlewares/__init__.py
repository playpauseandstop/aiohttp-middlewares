"""
===========
Middlewares
===========

Collection of useful middlewares for aiohttp applications.

"""

from .constants import IDEMPOTENT_METHODS, NON_IDEMPOTENT_METHODS
from .cors import cors_middleware
from .error import (
    default_error_handler,
    error_context,
    error_middleware,
    get_error_response,
)
from .https import https_middleware
from .shield import shield_middleware
from .timeout import timeout_middleware
from .utils import match_path


__author__ = "Igor Davydenko"
__license__ = "BSD-3-Clause"
__version__ = "1.1.0"


# Make flake8 happy
(
    cors_middleware,
    default_error_handler,
    error_context,
    error_middleware,
    get_error_response,
    https_middleware,
    IDEMPOTENT_METHODS,
    match_path,
    NON_IDEMPOTENT_METHODS,
    shield_middleware,
    timeout_middleware,
)

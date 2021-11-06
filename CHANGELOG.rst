1.2.0 (2021-11-01)
==================

Release new version, which supports latest aiohttp 3.8.0 release and ensures support
of Python 3.9 & 3.10.

**Features:**

- Support latest aiohttp release (#55)

**Refactoring:**

- Move code to src directory

**Other:**

- Update pre-commit hooks
- Massive updates to internal library infrastructure
- Bump pre-commit hooks
- Update config
- Bump github actions to use
- Update library infrastructure
- Update package version
- Update common files
- (**deps-dev**) bump pytest from 6.0.1 to 6.1.0 (#29)
- (**deps-dev**) bump coverage from 5.2.1 to 5.3 (#28)
- (**deps**) bump aiohttp from 3.6.2 to 3.7.2 (#30)
- (**deps-dev**) bump pytest from 6.1.0 to 6.1.2 (#31)
- Use Python 3.10 as dev version (#52)
- (**deps**) bump actions/checkout from 2.3.4 to 2.3.5 (#53)
- Update docs requirements (#54)
- Bump requirements for docs (#56)
- Switch to Furo theme (#57)
- Update Read the Docs configuration (#58)

1.1.0 (2020-04-21)
==================

- Provide ``get_error_response`` coroutine to allow other projects to reuse
  error handling logic

1.0.0 (2020-01-14)
==================

- chore: Release **1.0.0** version which highlights updates to error middleware
  and first class support of `yarl.URL` instances within the library

1.0.0b1 (2020-01-14)
--------------------

- chore: Make default error handler available to import as,

  .. code-block:: python

      from aiohttp_middlewares import default_error_handler

1.0.0b0 (2020-01-14)
--------------------

- chore: Return empty response for CORS preflight requests

1.0.0a0 (2020-01-12)
--------------------

- feature: Provide default error handler and enable it in error middleware
- feature: Allow to ignore exceptions from handling by error middleware
- feature: First class support of ``yarl.URL`` within all library

0.3.1 (2019-11-13)
==================

- chore: Release **0.3.1** version

0.3.1a0 (2019-11-13)
--------------------

- chore: Pulbish ``aiohttp-middlewares`` to PyPI from ``py38`` image to ensure
  Python 3.8 classifier used

0.3.0 (2019-11-12)
==================

- feature: Ensure Python 3.8 support
- chore: Speedup matching text URLs for timeout & shield middlewares

0.2.0 (2019-07-23)
==================

- chore: Release **0.2.0** version with new CORS & Error middlewares and
  dropped support of Python 3.5 and aiohttp < 3.5

0.2.0b2 (2019-07-22)
--------------------

- feature: Add ``cors_middleware`` to simplify handling CORS headers for
  aiohttp apps comparing to `aiohttp-cors
  <https://github.com/aio-libs/aiohttp-cors>`_ library
- chore: ``IDEMPOTENT_METHODS`` and ``NON_IDEMPOTENT_METHODS`` are now tuple
  of strings, not frozenset

0.2.0b1 (2019-07-19)
--------------------

- fix: Fix global visibility for error context & middleware

0.2.0b0 (2019-07-19)
--------------------

- feature: Add ``error_middleware`` to allow handle errors inside of aiohttp
  applications
- chore: Drop Python 3.5 support

0.2.0a2 (2019-07-19)
--------------------

- feature: Put ``match_path`` function to ``aiohttp_middlewares.utils`` module
  scope

0.2.0a1 (2019-07-19)
--------------------

- chore: As aiohttp-middlewares heavily depends on aiohttp annotations, drop
  support of aiohttp < 3.5
- chore: Wrap all middlewares into ``@web.middleware`` decorator
- chore: Enable black code formatting
- chore: Enable pre-commit hooks

0.2.0a0 (2018-10-23)
--------------------

- Ensure Python 3.7 support
- Drop aiohttp 2 support
- Ensure support latest aiohttp version, ``3.4.4``
- Make library `PEP-561 <https://www.python.org/dev/peps/pep-0561/>`_ compatible

0.1.1 (2018-05-25)
==================

- Support `async-timeout` 3.0 version

0.1.0 (2018-02-20)
==================

- First non-beta release
- Support `aiohttp` 3.0 version

0.1.0b2 (2018-02-04)
--------------------

- New ``shield_middleware`` to wrap request handler into
  `asyncio.shield <https://docs.python.org/3/library/asyncio-task.html#asyncio.shield>`_
  helper before execution
- Allow to match URL by regexp for shield/timeout middleware

0.1.0b1 (2017-10-20)
--------------------

- New ``https_middleware`` to allow use proper scheme in ``request.url``, when
  deploying aiohttp behind reverse proxy with enabled HTTPS
- Allow passing dict of URLs with list methods to flex process of matching
  request ignored to wrapping into timeout context manager

0.1.0a2 (2017-05-14)
--------------------

- Rename ``timeout_middleware_factory`` to ``timeout_middleware``

0.1.0a1 (2017-05-13)
--------------------

- Initial release. Implements timeout middleware

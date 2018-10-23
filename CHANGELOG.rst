0.2.0 (In Development)
======================

0.2.0a1 (2018-10-23)
--------------------

- Ensure Python 3.7 support
- Drop aiohttp 2 support
- Ensure support latest aiohttp version, ``3.4.4``
- Make library [PEP-561](https://www.python.org/dev/peps/pep-0561/) compatible

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

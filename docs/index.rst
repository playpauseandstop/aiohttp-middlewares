===================
aiohttp_middlewares
===================

Collection of useful middlewares for `aiohttp <http://aiohttp.readthedocs.io>`_
applications.

- Works on Python 3.5+
- Works with aiohttp 3.5+
- BSD licensed
- Source, issues, and pull requests `on GitHub
  <https://github.com/playpauseandstop/aiohttp-middlewares>`_

Installation
============

.. code-block:: bash

    pip install aiohttp-middlewares

License
=======

*aiohttp-middlewares* is licensed under the terms of `BSD License
<https://github.com/playpauseandstop/aiohttp-middlewares/blob/LICENSE>`_.

API
===

.. automodule:: aiohttp_middlewares

.. automodule:: aiohttp_middlewares.timeout
.. autofunction:: aiohttp_middlewares.timeout.timeout_middleware

.. automodule:: aiohttp_middlewares.shield
.. autofunction:: aiohttp_middlewares.shield.shield_middleware

.. automodule:: aiohttp_middlewares.https
.. autofunction:: aiohttp_middlewares.https.https_middleware


Changelog
=========

.. include:: ../CHANGELOG.rst

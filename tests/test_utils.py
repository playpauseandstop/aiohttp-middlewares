import re

import aiohttp
import pytest

from aiohttp_middlewares.utils import get_aiohttp_version, match_request


URLS_COLLECTION = {
    '/slow-url',
    '/very-slow-url',
    re.compile('/(very-very|very-very-very)-slow-url'),
}
URLS_DICT = {
    '/slow-url': 'POST',
    '/very-slow-url': ['get', 'post'],
    re.compile('/(very-very|very-very-very)-slow-url'): {'GET', 'post', 'put'},
}


@pytest.mark.parametrize('version, expected', [
    ('2.0.7', (2, 0)),
    ('2.1.0', (2, 1)),
    ('2.2.5', (2, 2)),
    ('2.3.0a4', (2, 3)),
    ('2.3.0', (2, 3)),
    ('2.3.1a1', (2, 3)),
    ('2.3.1', (2, 3)),
])
def test_get_aiohttp_version(monkeypatch, version, expected):
    monkeypatch.setattr(aiohttp, '__version__', version)
    assert get_aiohttp_version() == expected


@pytest.mark.parametrize('urls, request_method, request_path, expected', [
    (URLS_COLLECTION, 'GET', '/', False),
    (URLS_COLLECTION, 'POST', '/slow-url', True),
    (URLS_COLLECTION, 'GET', '/very-slow-url', True),
    (URLS_COLLECTION, 'POST', '/very-slow-url', True),
    (URLS_COLLECTION, 'GET', '/very-very-slow-url', True),
    (URLS_COLLECTION, 'POST', '/very-very-slow-url', True),
    (URLS_COLLECTION, 'GET', '/very-very-very-slow-url', True),
    (URLS_COLLECTION, 'POST', '/very-very-very-slow-url', True),
    (URLS_DICT, 'GET', '/', False),
    (URLS_DICT, 'GET', '/slow-url', False),
    (URLS_DICT, 'POST', '/slow-url', True),
    (URLS_DICT, 'GET', '/very-slow-url', True),
    (URLS_DICT, 'PATCH', '/very-slow-url', False),
    (URLS_DICT, 'GET', '/very-very-slow-url', True),
    (URLS_DICT, 'POST', '/very-very-slow-url', True),
    (URLS_DICT, 'PUT', '/very-very-slow-url', True),
    (URLS_DICT, 'PATCH', '/very-very-slow-url', False),
    (URLS_DICT, 'GET', '/very-very-very-slow-url', True),
    (URLS_DICT, 'POST', '/very-very-very-slow-url', True),
    (URLS_DICT, 'PUT', '/very-very-very-slow-url', True),
    (URLS_DICT, 'PATCH', '/very-very-very-slow-url', False),
])
def test_match_request(urls, request_method, request_path, expected):
    assert match_request(urls, request_method, request_path) is expected

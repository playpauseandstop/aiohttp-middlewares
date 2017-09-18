import pytest

from aiohttp_middlewares.utils import match_request


URLS_COLLECTION = {'/slow-url', '/very-slow-url'}
URLS_DICT = {
    '/slow-url': 'POST',
    '/very-slow-url': ['get', 'post'],
}


@pytest.mark.parametrize('urls, request_method, request_path, expected', [
    (URLS_COLLECTION, 'GET', '/', False),
    (URLS_COLLECTION, 'POST', '/slow-url', True),
    (URLS_COLLECTION, 'GET', '/very-slow-url', True),
    (URLS_COLLECTION, 'POST', '/very-slow-url', True),
    (URLS_DICT, 'GET', '/', False),
    (URLS_DICT, 'GET', '/slow-url', False),
    (URLS_DICT, 'POST', '/slow-url', True),
    (URLS_DICT, 'GET', '/very-slow-url', True),
    (URLS_DICT, 'PATCH', '/very-slow-url', False),
])
def test_match_request(urls, request_method, request_path, expected):
    assert match_request(urls, request_method, request_path) is expected

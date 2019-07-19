import re

import pytest

from aiohttp_middlewares import match_path
from aiohttp_middlewares.utils import match_request


URLS_COLLECTION = {
    "/slow-url",
    "/very-slow-url",
    re.compile("/(very-very|very-very-very)-slow-url"),
}
URLS_DICT = {
    "/slow-url": "POST",
    "/very-slow-url": ["get", "post"],
    re.compile("/(very-very|very-very-very)-slow-url"): {"GET", "post", "put"},
}


@pytest.mark.parametrize(
    "url, path, expected",
    (
        ("/slow-url", "/slow-url", True),
        ("/slow-url", "/slow-url/", False),
        (re.compile("^/slow-url"), "/slow-url", True),
        (re.compile("^/slow-url"), "/slow-url/", True),
        (re.compile("^/slow-url"), "/very-slow-url", False),
    ),
)
def test_match_path(url, path, expected):
    assert match_path(url, path) == expected


@pytest.mark.parametrize(
    "urls, request_method, request_path, expected",
    (
        (URLS_COLLECTION, "GET", "/", False),
        (URLS_COLLECTION, "POST", "/slow-url", True),
        (URLS_COLLECTION, "GET", "/very-slow-url", True),
        (URLS_COLLECTION, "POST", "/very-slow-url", True),
        (URLS_COLLECTION, "GET", "/very-very-slow-url", True),
        (URLS_COLLECTION, "POST", "/very-very-slow-url", True),
        (URLS_COLLECTION, "GET", "/very-very-very-slow-url", True),
        (URLS_COLLECTION, "POST", "/very-very-very-slow-url", True),
        (URLS_DICT, "GET", "/", False),
        (URLS_DICT, "GET", "/slow-url", False),
        (URLS_DICT, "POST", "/slow-url", True),
        (URLS_DICT, "GET", "/very-slow-url", True),
        (URLS_DICT, "PATCH", "/very-slow-url", False),
        (URLS_DICT, "GET", "/very-very-slow-url", True),
        (URLS_DICT, "POST", "/very-very-slow-url", True),
        (URLS_DICT, "PUT", "/very-very-slow-url", True),
        (URLS_DICT, "PATCH", "/very-very-slow-url", False),
        (URLS_DICT, "GET", "/very-very-very-slow-url", True),
        (URLS_DICT, "POST", "/very-very-very-slow-url", True),
        (URLS_DICT, "PUT", "/very-very-very-slow-url", True),
        (URLS_DICT, "PATCH", "/very-very-very-slow-url", False),
    ),
)
def test_match_request(urls, request_method, request_path, expected):
    assert match_request(urls, request_method, request_path) is expected

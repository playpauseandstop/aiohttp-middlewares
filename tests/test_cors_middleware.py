import json
import re

import attr
import pytest
from aiohttp import web
from yarl import URL

from aiohttp_middlewares import cors_middleware
from aiohttp_middlewares.cors import (
    ACCESS_CONTROL,
    ACCESS_CONTROL_ALLOW_HEADERS,
    ACCESS_CONTROL_ALLOW_METHODS,
    ACCESS_CONTROL_ALLOW_ORIGIN,
    ACCESS_CONTROL_EXPOSE_HEADERS,
    ACCESS_CONTROL_MAX_AGE,
    ACCESS_CONTROL_REQUEST_METHOD,
    DEFAULT_ALLOW_HEADERS,
    DEFAULT_ALLOW_METHODS,
)


API_REGEX = re.compile(r"^\/api")
TEST_DENIED_ORIGIN = "https://www.google.com"
TEST_ORIGIN = "http://localhost:3000"
TEST_ORIGIN_REGEX = re.compile(r"^http\:\/\/localhost")
TEST_ORIGIN_URL = URL(TEST_ORIGIN)


async def create_http_exception(request):
    raise web.HTTPServiceUnavailable(
        text=json.dumps({"detail": "Internal service is unavailable"}),
        content_type="application/json",
    )


async def index(request):
    return web.json_response({})


def check_allow_origin(
    response,
    origin,
    *,
    allow_headers=DEFAULT_ALLOW_HEADERS,
    allow_methods=DEFAULT_ALLOW_METHODS,
):
    assert response.headers[ACCESS_CONTROL_ALLOW_ORIGIN] == origin
    if allow_headers:
        assert response.headers[ACCESS_CONTROL_ALLOW_HEADERS] == ", ".join(
            allow_headers
        )
    if allow_methods:
        assert response.headers[ACCESS_CONTROL_ALLOW_METHODS] == ", ".join(
            allow_methods
        )
    return response


def check_deny_origin(response):
    assert ACCESS_CONTROL_ALLOW_ORIGIN not in response.headers
    return response


def create_app(**kwargs):
    app = web.Application(middlewares=[cors_middleware(**kwargs)])
    app.router.add_get("/", index)
    app.router.add_post("/http-exceptions", create_http_exception)
    return app


async def test_allow_all_handler_not_found(aiohttp_client):
    client = await aiohttp_client(create_app(allow_all=True))
    response = check_allow_origin(
        await client.get("/does-not-exist", headers={"Origin": TEST_ORIGIN}),
        "*",
        allow_headers=None,
        allow_methods=None,
    )
    assert response.status == 404
    assert response.content_type == "text/plain"


@pytest.mark.parametrize(
    "config, method, extra_headers, expected_origin, expected_allow_headers, "
    "expected_allow_methods",
    (
        ({"allow_all": True}, "GET", {}, "*", None, None),
        (
            {"allow_all": True},
            "OPTIONS",
            {ACCESS_CONTROL_REQUEST_METHOD: "GET"},
            "*",
            attr.NOTHING,
            attr.NOTHING,
        ),
        (
            {"allow_all": True, "allow_credentials": True},
            "OPTIONS",
            {ACCESS_CONTROL_REQUEST_METHOD: "GET"},
            TEST_ORIGIN,
            attr.NOTHING,
            attr.NOTHING,
        ),
        ({"origins": [TEST_ORIGIN]}, "GET", {}, TEST_ORIGIN, None, None),
        (
            {"origins": (TEST_ORIGIN[::-1], TEST_ORIGIN_REGEX)},
            "GET",
            {},
            TEST_ORIGIN,
            None,
            None,
        ),
        (
            {"origins": [TEST_ORIGIN]},
            "OPTIONS",
            {ACCESS_CONTROL_REQUEST_METHOD: "GET"},
            TEST_ORIGIN,
            attr.NOTHING,
            attr.NOTHING,
        ),
        (
            {"origins": {TEST_ORIGIN_REGEX}},
            "OPTIONS",
            {ACCESS_CONTROL_REQUEST_METHOD: "GET"},
            TEST_ORIGIN,
            attr.NOTHING,
            attr.NOTHING,
        ),
        (
            {"origins": [TEST_ORIGIN_URL]},
            "OPTIONS",
            {ACCESS_CONTROL_REQUEST_METHOD: "GET"},
            TEST_ORIGIN,
            attr.NOTHING,
            attr.NOTHING,
        ),
    ),
)
async def test_allow_origin(
    aiohttp_client,
    config,
    method,
    extra_headers,
    expected_origin,
    expected_allow_headers,
    expected_allow_methods,
):
    client = await aiohttp_client(create_app(**config))

    kwargs = {}
    if expected_allow_headers is not attr.NOTHING:
        kwargs["allow_headers"] = expected_allow_headers
    if expected_allow_methods is not attr.NOTHING:
        kwargs["allow_methods"] = expected_allow_methods

    check_allow_origin(
        await client.request(
            method, "/", headers={"Origin": TEST_ORIGIN, **extra_headers}
        ),
        expected_origin,
        **kwargs,
    )


async def test_allow_origin_handler_create_http_exception(aiohttp_client):
    client = await aiohttp_client(create_app(origins=(TEST_ORIGIN,)))
    response = check_allow_origin(
        await client.post("/http-exceptions", headers={"Origin": TEST_ORIGIN}),
        TEST_ORIGIN,
        allow_headers=None,
        allow_methods=None,
    )
    assert response.status == 503
    assert response.content_type == "application/json"


@pytest.mark.parametrize(
    "origins, method, headers",
    (
        ([TEST_DENIED_ORIGIN], "GET", {"Origin": TEST_ORIGIN}),
        (
            [TEST_DENIED_ORIGIN],
            "OPTIONS",
            {"Origin": TEST_ORIGIN, ACCESS_CONTROL_REQUEST_METHOD: "GET"},
        ),
        ({API_REGEX}, "GET", {"Origin": TEST_ORIGIN}),
        ({API_REGEX}, "GET", {"Origin": TEST_ORIGIN}),
    ),
)
async def test_deny_origin(aiohttp_client, origins, method, headers):
    client = await aiohttp_client(create_app(origins=origins))
    check_deny_origin(await client.request(method, "/", headers=headers))


async def test_empty_response(aiohttp_client):
    client = await aiohttp_client(create_app(allow_all=True))
    client_url = f"http://{client.host}:{client.port}"

    response = await client.request(
        "OPTIONS",
        "/",
        headers={
            f"{ACCESS_CONTROL}-Request-Headers": (
                "x-client-uid,x-requested-with"
            ),
            ACCESS_CONTROL_REQUEST_METHOD: "GET",
            "Origin": client_url,
            "Referer": f"{client_url}/",
            "User-Agent": "Mozilla/5.0",
        },
    )

    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"
    assert response.headers["Content-Length"] == "0"
    assert await response.text() == ""


@pytest.mark.parametrize(
    "method, headers",
    (
        ("GET", {"Origin": TEST_ORIGIN}),
        (
            "OPTIONS",
            {"Origin": TEST_ORIGIN, ACCESS_CONTROL_REQUEST_METHOD: "GET"},
        ),
    ),
)
async def test_expose_headers(aiohttp_client, method, headers):
    client = await aiohttp_client(
        create_app(allow_all=True, expose_headers=["x-client-uid"])
    )
    response = await client.request(method, "/", headers=headers)
    assert response.headers[ACCESS_CONTROL_EXPOSE_HEADERS] == "x-client-uid"


@pytest.mark.parametrize(
    "max_age, method, headers, expected_max_age",
    (
        (None, "GET", {"Origin": TEST_ORIGIN}, None),
        (
            None,
            "OPTIONS",
            {"Origin": TEST_ORIGIN, ACCESS_CONTROL_REQUEST_METHOD: "GET"},
            None,
        ),
        (86400, "GET", {"Origin": TEST_ORIGIN}, None),
        (
            86400,
            "OPTIONS",
            {"Origin": TEST_ORIGIN, ACCESS_CONTROL_REQUEST_METHOD: "GET"},
            "86400",
        ),
    ),
)
async def test_max_age(
    aiohttp_client, method, headers, max_age, expected_max_age
):
    client = await aiohttp_client(create_app(allow_all=True, max_age=max_age))
    response = await client.request(method, "/", headers=headers)
    assert response.headers.get(ACCESS_CONTROL_MAX_AGE) == expected_max_age


@pytest.mark.parametrize("url", ("/", "/does-not-exist"))
async def test_no_origin(aiohttp_client, url):
    client = await aiohttp_client(create_app(allow_all=True))
    check_deny_origin(await client.get(url))


async def test_url_blacklisted(aiohttp_client):
    client = await aiohttp_client(
        create_app(allow_all=True, urls=[re.compile(r"\/api")])
    )
    check_deny_origin(await client.get("/", headers={"Origin": TEST_ORIGIN}))


async def test_url_whitelisted(aiohttp_client):
    app = create_app(allow_all=True, urls=[API_REGEX])
    app.router.add_get("/api/", index)
    client = await aiohttp_client(app)
    check_allow_origin(
        await client.get("/api/", headers={"Origin": TEST_ORIGIN}),
        "*",
        allow_headers=None,
        allow_methods=None,
    )

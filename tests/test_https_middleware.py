import pytest
from aiohttp import web

from aiohttp_middlewares import https_middleware


def create_app(match_headers):
    app = web.Application(middlewares=[https_middleware(match_headers)])
    app.router.add_route("GET", "/", handler)
    return app


async def handler(request):
    return web.json_response(request.url.scheme)


@pytest.mark.parametrize(
    "match_headers, request_headers, expected",
    [
        (None, None, "http"),
        (None, {"X-Forwarded-Proto": "http"}, "http"),
        (None, {"X-Forwarded-Proto": "https"}, "https"),
        ({}, None, "http"),
        ({}, {"X-Forwarded-Proto": "http"}, "http"),
        ({"Forwarded": "https"}, None, "http"),
        ({"Forwarded": "https"}, {"X-Forwarded-Proto": "http"}, "http"),
        ({"Forwarded": "https"}, {"X-Forwarded-Proto": "https"}, "http"),
        ({"Forwarded": "https"}, {"Forwarded": "http"}, "http"),
        ({"Forwarded": "https"}, {"Forwarded": "https"}, "https"),
    ],
)
async def test_https_middleware(
    aiohttp_client, match_headers, request_headers, expected
):
    client = await aiohttp_client(create_app(match_headers))
    response = await client.get("/", headers=request_headers)
    assert await response.json() == expected

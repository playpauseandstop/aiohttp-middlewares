import pytest

from aiohttp import web

from aiohttp_middlewares import https_middleware
from aiohttp_middlewares.utils import get_aiohttp_version


def create_app(match_headers):
    app = web.Application(middlewares=[https_middleware(match_headers)])
    app.router.add_route('GET', '/', handler)
    return app


async def handler(request):
    return web.json_response(request.url.scheme)


@pytest.mark.parametrize('match_headers, request_headers, expected', [
    (None, None, 'http'),
    (None, {'X-Forwarded-Proto': 'http'}, 'http'),
    (None, {'X-Forwarded-Proto': 'https'}, 'https'),
    ({}, None, 'http'),
    ({}, {'X-Forwarded-Proto': 'http'}, 'http'),
    ({'Forwarded': 'https'}, None, 'http'),
    ({'Forwarded': 'https'}, {'X-Forwarded-Proto': 'http'}, 'http'),
    ({'Forwarded': 'https'}, {'X-Forwarded-Proto': 'https'}, 'http'),
    ({'Forwarded': 'https'}, {'Forwarded': 'http'}, 'http'),
    ({'Forwarded': 'https'}, {'Forwarded': 'https'}, 'https'),
])
async def test_https_middleware(test_client,
                                match_headers,
                                request_headers,
                                expected):
    client = await test_client(create_app(match_headers))
    response = await client.get('/', headers=request_headers)
    assert await response.json() == expected


@pytest.mark.skipif(
    get_aiohttp_version() != (2, 0) and get_aiohttp_version() < (2, 3),
    reason='aiohttp 2.0 & 2.3+')
async def test_https_middleware_aiohttp20_23_empty_match_headers(test_client):
    client = await test_client(create_app({}))
    response = await client.get('/', headers={'X-Forwarded-Proto': 'https'})
    assert await response.json() == 'http'


@pytest.mark.skipif(
    get_aiohttp_version() not in ((2, 1), (2, 2)),
    reason='aiohttp 2.1 & 2.2')
async def test_https_middleware_aiohttp21_22_empty_match_headers(test_client):
    client = await test_client(create_app({}))
    response = await client.get('/', headers={'X-Forwarded-Proto': 'https'})
    assert await response.json() == 'https'

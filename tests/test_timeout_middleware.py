import asyncio

import pytest

from aiohttp import web

from aiohttp_middlewares import timeout_middleware


HALF_A_SECOND = .5
SECOND = 1


def create_app(seconds, ignore=None):
    app = web.Application(middlewares=[
        timeout_middleware(seconds, ignore=ignore)])
    app.router.add_route('GET', '/', handler)
    app.router.add_route('GET', '/slow', slow_handler)
    return app


async def handler(request):
    return web.json_response()


async def slow_handler(request):
    await asyncio.sleep(SECOND)
    return web.json_response()


@pytest.mark.parametrize('seconds, ignore, url, expected', [
    (SECOND - HALF_A_SECOND, None, '/', 200),
    (SECOND - HALF_A_SECOND, None, '/slow', 504),
    (SECOND + HALF_A_SECOND, None, '/', 200),
    (SECOND + HALF_A_SECOND, None, '/slow', 200),
    (SECOND - HALF_A_SECOND, ['/slow'], '/', 200),
    (SECOND - HALF_A_SECOND, ['/slow'], '/slow', 200),
])
async def test_timeout_middleware(test_client, seconds, ignore, url, expected):
    client = await test_client(create_app(seconds, ignore))
    response = await client.get(url)
    assert response.status == expected

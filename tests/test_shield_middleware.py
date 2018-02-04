import asyncio
import re

import pytest
from aiohttp import web
from aiohttp.test_utils import make_mocked_request

from aiohttp_middlewares import NON_IDEMPOTENT_METHODS, shield_middleware


def create_app(*, methods=None, urls=None, ignore=None):
    app = web.Application(
        middlewares=[
            shield_middleware(methods=methods, urls=urls, ignore=ignore)])

    app.router.add_get('/one', handler)
    app.router.add_post('/one', handler)
    app.router.add_get('/two', handler)
    app.router.add_post('/two', handler)
    app.router.add_patch('/three', handler)

    return app


async def handler(request):
    return web.json_response(True)


def test_shield_middleware_no_arguments():
    with pytest.raises(ValueError):
        shield_middleware()


def test_shield_middleware_mixed_methods_and_urls():
    with pytest.raises(ValueError):
        shield_middleware(methods=NON_IDEMPOTENT_METHODS, urls=['/one'])


def test_shield_middleware_mixed_urls_and_ignore():
    with pytest.raises(ValueError):
        shield_middleware(urls=['/one'], ignore=['/two'])


@pytest.mark.parametrize('method, url', [
    ('GET', '/one'),
    ('GET', '/two'),
    ('POST', '/one'),
    ('POST', '/two'),
    ('PATCH', '/three'),
])
async def test_shield_request_by_method(test_client, url, method):
    app = create_app(methods=NON_IDEMPOTENT_METHODS, ignore=['/three'])
    client = await test_client(app)

    response = await client.request(method, url)
    assert response.status == 200
    assert await response.json() is True


@pytest.mark.parametrize('method, url', [
    ('GET', '/one'),
    ('GET', '/two'),
    ('POST', '/one'),
    ('POST', '/two'),
    ('PATCH', '/three'),
])
async def test_shield_request_by_url(test_client, url, method):
    app = create_app(urls={
        '/one': ['POST'],
        re.compile(r'/(two|three)'): {'post', 'patch'},
    })
    client = await test_client(app)

    response = await client.request(method, url)
    assert response.status == 200
    assert await response.json() is True


@pytest.mark.parametrize('method, value', [
    ('DELETE', False),
    ('GET', False),
    ('POST', True),
    ('PUT', False),
])
async def test_shield_middleware_funcitonal(loop, method, value):
    flag = False
    client_ready = asyncio.Event()
    handler_ready = asyncio.Event()

    async def handler(request):
        handler_ready.set()

        # Cancellation point.
        # When not shielded, CancelledError will be raised here.
        await client_ready.wait()

        nonlocal flag
        flag = True

        return web.Response(status=200)

    factory = shield_middleware(methods=frozenset({'POST'}))
    wrapped_handler = await factory(web.Application(), handler)

    # Run handler in a task.
    task = loop.create_task(wrapped_handler(make_mocked_request(method, '/')))
    await handler_ready.wait()

    # Cancel the handler.
    task.cancel()
    client_ready.set()
    # Wait for completion.
    await asyncio.wait([task])

    assert flag is value

import re

import pytest
from aiohttp import web

from aiohttp_middlewares import (
    error_context,
    error_middleware,
    get_error_response,
)


class LegalException(Exception):
    def __init__(self):
        super().__init__("Not available for legal reasons")
        self.status = 451
        self.data = {"paid": False, "pay_at": "https://payment.url/"}


@web.middleware
async def custom_error_middleware(request, handler):
    try:
        return await handler(request)
    except Exception as err:  # noqa: PIE786
        return await get_error_response(request, err, default_handler=error)


async def api_error(request):
    with error_context(request) as context:
        return web.json_response(context.data, status=context.status)


async def error(request):
    with error_context(request) as context:
        return web.Response(
            text=context.message,
            status=context.status,
            content_type="text/plain",
        )


async def legal(request):
    raise LegalException()


async def no_error_context(request):
    return web.Response(text="Server Error", status=500)


async def test_custom_middleware(aiohttp_client):
    app = web.Application(middlewares=[custom_error_middleware])
    client = await aiohttp_client(app)

    response = await client.get("/does-not-exist.exe")
    assert response.content_type == "text/plain"
    assert response.status == 404
    assert await response.text() == "Not Found"


async def test_default_handler(aiohttp_client):
    app = web.Application(middlewares=[error_middleware()])
    client = await aiohttp_client(app)

    response = await client.get("/does-not-exist.exe")
    assert response.content_type == "application/json"
    assert response.status == 404
    assert await response.json() == {"detail": "Not Found"}


@pytest.mark.parametrize(
    "ignore_exceptions",
    (web.HTTPNotFound, (web.HTTPNotFound,), (ValueError, web.HTTPNotFound)),
)
async def test_ignore_exceptions(aiohttp_client, ignore_exceptions):
    app = web.Application(
        middlewares=[error_middleware(ignore_exceptions=ignore_exceptions)]
    )
    client = await aiohttp_client(app)

    response = await client.get("/does-not-exist.exe")
    assert response.content_type == "text/plain"
    assert response.status == 404
    assert await response.text() == "404: Not Found"


@pytest.mark.parametrize(
    "path, expected_status, expected_content_type, expected_text",
    (
        ("/", 404, "text/plain", "Not Found"),
        ("/api/", 404, "application/json", '{"detail": "Not Found"}'),
        (
            "/api/legal/",
            451,
            "application/json",
            '{"paid": false, "pay_at": "https://payment.url/"}',
        ),
        ("/legal/", 451, "text/plain", "Not available for legal reasons"),
        ("/no-error-context/", 500, "text/plain", "Server Error"),
    ),
)
async def test_multiple_handlers(
    aiohttp_client, path, expected_status, expected_content_type, expected_text
):
    app = web.Application(
        middlewares=[
            error_middleware(
                default_handler=error,
                config={
                    "/no-error-context/": no_error_context,
                    re.compile(r"^/api"): api_error,
                },
            )
        ]
    )
    app.router.add_get("/legal/", legal)
    app.router.add_get("/api/legal/", legal)

    client = await aiohttp_client(app)
    response = await client.get(path)
    assert response.status == expected_status
    assert response.content_type == expected_content_type
    assert await response.text() == expected_text


async def test_single_handler(aiohttp_client):
    app = web.Application(
        middlewares=[error_middleware(default_handler=error)]
    )
    client = await aiohttp_client(app)

    response = await client.get("/does-not-exist.exe")
    assert response.content_type == "text/plain"
    assert response.status == 404
    assert await response.text() == "Not Found"

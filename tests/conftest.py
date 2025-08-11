"""Common fixtures for the tests."""

import asyncio

import pytest


# 3rd party fixtures
@pytest.fixture(scope="session")
def event_loop_policy():
    """Use standard asyncio library for async test cases."""
    return asyncio.DefaultEventLoopPolicy()

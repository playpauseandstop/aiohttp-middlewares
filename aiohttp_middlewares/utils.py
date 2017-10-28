from typing import Tuple

import aiohttp

from .types import Url, Urls


def get_aiohttp_version() -> Tuple[int, int]:
    """Return tuple of current aiohttp MAJOR.MINOR version."""
    return tuple(  # type: ignore
        int(item) for item in aiohttp.__version__.split('.')[:2])


def match_request(urls: Urls, method: str, path: str) -> bool:
    """Check whether request method and path matches given URLs or not."""
    def match_item(item: Url, path: str) -> bool:
        """Check whether current path is equal to given URL str or regexp."""
        try:
            return bool(item.match(path))  # type: ignore
        except (AttributeError, TypeError):
            return item == path

    found = [item for item in urls if match_item(item, path)]
    if not found:
        return False

    if not isinstance(urls, dict):
        return True

    found_item = urls[found[0]]
    method = method.lower()
    if isinstance(found_item, str):
        return found_item.lower() == method

    return any(True for item in found_item if item.lower() == method)

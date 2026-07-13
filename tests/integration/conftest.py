from collections.abc import AsyncGenerator
import os

import pytest
from aiowialon import Wialon

# Wialon SDK playground token — safe to commit, public demo server
PLAYGROUND_TOKEN = "5dce19710a5e26ab8b7b8986cb3c49e58C291791B7F0A7AEB8AFBFCEED7DC03BC48FF5F8"
PLAYGROUND_HOST = "hst-api.wialon.com"


@pytest.fixture
def token() -> str:
    return os.environ.get("WIALON_TOKEN", PLAYGROUND_TOKEN)


@pytest.fixture
def host() -> str:
    return os.environ.get("WIALON_HOST", PLAYGROUND_HOST)


@pytest.fixture
async def wialon(token, host) -> AsyncGenerator[Wialon, None]:
    async with Wialon(host=host, token=token) as w:
        yield w


@pytest.fixture
async def logged_in_wialon(wialon: Wialon) -> AsyncGenerator[Wialon, None]:
    await wialon.login()
    yield wialon
    await wialon.logout()

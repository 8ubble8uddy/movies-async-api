import asyncio
from typing import Iterator

import pytest


@pytest.fixture(scope='session')
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    """
    Получить новый объект `event_loop` для корректной работы асинхронного кода.

    Yields:
        asyncio.AbstractEventLoop: Объект `event_loop`
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    try:
        yield loop
    finally:
        loop.close()

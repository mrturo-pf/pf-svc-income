"""Shared fixtures for HTTP client tests."""

import asyncio

import pytest


@pytest.fixture(autouse=True)
def _instant_backoff(monkeypatch: pytest.MonkeyPatch) -> None:
    """Skip retry backoff delays so HTTP client tests run instantly."""

    async def _no_sleep(_seconds: float) -> None:
        return None

    monkeypatch.setattr(asyncio, "sleep", _no_sleep)

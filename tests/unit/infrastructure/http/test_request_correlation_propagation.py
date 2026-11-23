"""Tests for outbound correlation-header propagation."""

import asyncio

import httpx
import pytest
import respx
import structlog

from payroll.infrastructure.http._http_client import (
    PfRatesClientBase,
    _pf_reference_request,
)

from payroll.interfaces.api.request_correlation import get_or_create_request_id

_VALID_ID = "550e8400-e29b-41d4-a716-446655440000"
_BASE_URL = "https://reference.test"


@pytest.fixture(autouse=True)
def _identity_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """Provide a deterministic backend identity token in unit tests."""
    monkeypatch.setattr(
        "payroll.infrastructure.http._http_client.id_token.fetch_id_token",
        lambda _request, audience: f"token-for:{audience}",
    )


@pytest.mark.asyncio
async def test_outbound_headers_use_current_request_id() -> None:
    """Each outbound call includes the ID bound by inbound middleware."""
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=_VALID_ID)
    try:
        client = PfRatesClientBase("https://reference.test")

        assert await client._request_headers() == {
            "X-Request-ID": _VALID_ID,
            "Authorization": "Bearer token-for:https://reference.test",
        }
    finally:
        structlog.contextvars.clear_contextvars()


@pytest.mark.asyncio
@respx.mock
async def test_retry_reuses_one_request_id(monkeypatch: pytest.MonkeyPatch) -> None:
    """Network retries keep the same outbound correlation header."""

    async def _no_sleep(_seconds: float) -> None:
        return None

    monkeypatch.setattr(asyncio, "sleep", _no_sleep)
    route = respx.get(f"{_BASE_URL}/health").mock(
        side_effect=[httpx.ReadTimeout("timeout"), httpx.Response(200)]
    )
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=_VALID_ID)
    try:
        client = PfRatesClientBase(_BASE_URL)
        headers = await client._request_headers()
        response = await _pf_reference_request(
            f"{_BASE_URL}/health", None, headers, label="health"
        )

        assert response is not None
        assert route.call_count == 2
        assert {call.request.headers["X-Request-ID"] for call in route.calls} == {
            _VALID_ID
        }
    finally:
        structlog.contextvars.clear_contextvars()


@pytest.mark.asyncio
async def test_outbound_context_generates_one_id_for_repeated_attempts() -> None:
    """Work outside HTTP still gets one ID reused by retry attempts."""
    structlog.contextvars.clear_contextvars()
    try:
        first = get_or_create_request_id()
        second = get_or_create_request_id()

        assert first == second
        headers = await PfRatesClientBase("https://reference.test")._request_headers()
        assert headers["X-Request-ID"] == first
    finally:
        structlog.contextvars.clear_contextvars()

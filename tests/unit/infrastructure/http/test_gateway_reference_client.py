"""Tests for gateway-based reference service calls."""

import pytest
import structlog

from payroll.infrastructure.http._http_client import PfSvcReferenceClientBase


@pytest.mark.asyncio
async def test_reference_service_url_uses_identity_token_without_client_key() -> None:
    """Backend calls use identity tokens and never require a client API key."""
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id="550e8400-e29b-41d4-a716-446655440000"
    )
    try:
        headers = await PfSvcReferenceClientBase(
            "https://pf-svc-reference-yqd4p7fzaa-uc.a.run.app"
        )._request_headers()

        assert headers == {
            "X-Request-ID": "550e8400-e29b-41d4-a716-446655440000",
            "Authorization": "Bearer token-for:https://pf-svc-reference-yqd4p7fzaa-uc.a.run.app",
        }
    finally:
        structlog.contextvars.clear_contextvars()

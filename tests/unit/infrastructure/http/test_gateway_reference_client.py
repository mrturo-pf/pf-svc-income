"""Tests for gateway-based reference service calls."""

import pytest
import structlog

from payroll.infrastructure.http._http_client import PfRatesClientBase


@pytest.mark.asyncio
async def test_gateway_reference_url_uses_application_headers_only() -> None:
    """Gateway calls preserve app auth and correlation without direct ADC tokens."""
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id="550e8400-e29b-41d4-a716-446655440000"
    )
    try:
        headers = await PfRatesClientBase(
            "https://pf-backend-gateway-poc-88uq0qjn.uc.gateway.dev/reference",
            "api-key",
        )._request_headers()

        assert headers == {
            "X-API-Key": "api-key",
            "X-Request-ID": "550e8400-e29b-41d4-a716-446655440000",
        }
    finally:
        structlog.contextvars.clear_contextvars()

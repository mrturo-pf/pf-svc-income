"""Integration tests for the local authentication boundary."""

from fastapi.testclient import TestClient

from payroll.interfaces.api.main import app


def test_business_route_does_not_require_client_api_key() -> None:
    """Local direct requests are not rejected for missing client API keys."""
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/payroll")
    assert response.status_code != 403


def test_business_route_ignores_legacy_client_api_key() -> None:
    """The service does not validate legacy client API-key values."""
    client = TestClient(
        app, headers={"X-API-Key": "legacy-value"}, raise_server_exceptions=False
    )
    response = client.get("/reference-data/pension-institutions")
    assert response.status_code != 403


def test_health_returns_200_without_any_key() -> None:
    """/health is public: no client API key is required."""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200

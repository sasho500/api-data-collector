import httpx
import pytest

from api_collector.domain.exceptions import (
    ApiTimeoutError,
    AuthenticationError,
    InvalidResponseError,
)
from api_collector.infrastructure.http_client import ApiClient


def test_get_json_returns_response_data() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Authorization"] == "Bearer test-token"
        assert request.url.params["limit"] == "10"

        return httpx.Response(
            status_code=200,
            json={
                "results": [
                    {
                        "id": 1,
                        "name": "router-demo-01",
                    }
                ]
            },
        )

    transport = httpx.MockTransport(handler)

    with ApiClient(
        base_url="https://example.com/api",
        token="test-token",
        timeout=30,
        transport=transport,
    ) as client:
        result = client.get_json(
            endpoint="devices",
            params={"limit": 10},
        )

    assert result == {
        "results": [
            {
                "id": 1,
                "name": "router-demo-01",
            }
        ]
    }


def test_timeout_is_converted_to_project_exception() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout(
            "Request timed out.",
            request=request,
        )

    transport = httpx.MockTransport(handler)

    with ApiClient(
        base_url="https://example.com/api",
        transport=transport,
    ) as client:
        with pytest.raises(
            ApiTimeoutError,
            match="API request timed out",
        ):
            client.get_json("devices")


def test_unauthorized_response_raises_authentication_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=401,
            request=request,
        )

    transport = httpx.MockTransport(handler)

    with ApiClient(
        base_url="https://example.com/api",
        transport=transport,
    ) as client:
        with pytest.raises(AuthenticationError):
            client.get_json("devices")


def test_invalid_json_raises_invalid_response_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=200,
            content=b"this is not JSON",
            request=request,
        )

    transport = httpx.MockTransport(handler)

    with ApiClient(
        base_url="https://example.com/api",
        transport=transport,
    ) as client:
        with pytest.raises(
            InvalidResponseError,
            match="did not return valid JSON",
        ):
            client.get_json("devices")
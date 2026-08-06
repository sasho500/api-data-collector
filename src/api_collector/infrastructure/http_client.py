from types import TracebackType
from typing import Any, Mapping, Self, cast

import httpx

from api_collector.domain.exceptions import (
    ApiConnectionError,
    ApiResponseError,
    ApiTimeoutError,
    AuthenticationError,
    AuthorizationError,
    InvalidResponseError,
    RateLimitError,
    ResourceNotFoundError,
)


JsonPayload = dict[str, Any] | list[Any]
QueryValue = str | int | float | bool | None
QueryParameters = Mapping[str, QueryValue]


class ApiClient:
    """Reusable synchronous client for communicating with REST APIs."""

    def __init__(
        self,
        base_url: str,
        token: str | None = None,
        timeout: int = 30,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")

        headers = {
            "Accept": "application/json",
        }

        if token:
            headers["Authorization"] = f"Bearer {token}"

        self._client = httpx.Client(
            headers=headers,
            timeout=float(timeout),
            transport=transport,
        )

    def get_json(
        self,
        endpoint: str,
        params: QueryParameters | None = None,
    ) -> JsonPayload:
        """Send a GET request and return a JSON object or JSON list."""

        url = self._build_url(endpoint)

        try:
            response = self._client.get(
                url,
                params=params,
            )
        except httpx.TimeoutException as error:
            raise ApiTimeoutError(
                f"API request timed out while requesting '{url}'."
            ) from error
        except httpx.RequestError as error:
            raise ApiConnectionError(
                f"Could not communicate with API endpoint '{url}'."
            ) from error

        self._check_status(response)

        try:
            payload: Any = response.json()
        except ValueError as error:
            raise InvalidResponseError(
                f"API endpoint '{url}' did not return valid JSON."
            ) from error

        if not isinstance(payload, (dict, list)):
            raise InvalidResponseError(
                f"API endpoint '{url}' returned an unsupported JSON structure."
            )

        return cast(JsonPayload, payload)

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""

        self._client.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def _build_url(self, endpoint: str) -> str:
        """Combine the configured base URL with an API endpoint."""

        normalized_endpoint = endpoint.lstrip("/")

        return f"{self._base_url}/{normalized_endpoint}"

    @staticmethod
    def _check_status(response: httpx.Response) -> None:
        """Convert unsuccessful HTTP statuses to project exceptions."""

        status_code = response.status_code
        url = str(response.request.url)

        if 200 <= status_code < 300:
            return

        if status_code == 401:
            raise AuthenticationError(
                f"Authentication failed while requesting '{url}'."
            )

        if status_code == 403:
            raise AuthorizationError(
                f"Access to API endpoint '{url}' is forbidden."
            )

        if status_code == 404:
            raise ResourceNotFoundError(
                f"API resource '{url}' was not found."
            )

        if status_code == 429:
            raise RateLimitError(
                f"API rate limit was reached while requesting '{url}'."
            )

        raise ApiResponseError(
            f"API endpoint '{url}' returned HTTP status {status_code}."
        )
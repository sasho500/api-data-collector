class ApiClientError(RuntimeError):
    """Base exception for errors raised by the REST API client."""


class ApiTimeoutError(ApiClientError):
    """Raised when an API request exceeds the configured timeout."""


class ApiConnectionError(ApiClientError):
    """Raised when the client cannot communicate with the API."""


class AuthenticationError(ApiClientError):
    """Raised when the API rejects the supplied credentials."""


class AuthorizationError(ApiClientError):
    """Raised when the authenticated user does not have permission."""


class ResourceNotFoundError(ApiClientError):
    """Raised when the requested API resource does not exist."""


class RateLimitError(ApiClientError):
    """Raised when the API rate limit has been reached."""


class ApiResponseError(ApiClientError):
    """Raised when the API returns another unsuccessful HTTP status."""


class InvalidResponseError(ApiClientError):
    """Raised when the API response cannot be parsed as valid JSON."""
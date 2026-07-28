import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv


class ConfigError(ValueError):
    """Custom exception for configuration errors."""
    pass

def _get_required_variable(name: str) -> str:

    value = os.getenv(name)

    if value is None or not value.strip():
        raise ConfigError(f"Required environment variable '{name}' is missing.")

    return value.strip()


def _get_positive_integer(name: str, default: int) -> int:

    raw_value = os.getenv(name, str(default))

    try:
        value = int(raw_value)
    except ValueError as error:
        raise ConfigError(
            f"Environment variable '{name}' must be an integer. "
            f"Received: {raw_value!r}"
        ) from error

    if value <= 0:
        raise ConfigError(
            f"Environment variable '{name}' must be greater than 0."
        )

    return value


def _validate_url(url: str) -> str:

    parsed_url = urlparse(url)

    if parsed_url.scheme not in {"http", "https"}:
        raise ConfigError(
            "API_BASE_URL must start with 'http://' or 'https://'."
        )

    if not parsed_url.netloc:
        raise ConfigError("API_BASE_URL must contain a valid hostname.")

    return url.rstrip("/")


@dataclass(frozen=True, slots=True)
class Settings:

    api_base_url: str
    api_token: str | None
    request_timeout: int
    max_retries: int
    page_size: int
    output_directory: Path
    log_level: str

    @classmethod
    def from_env(
        cls,
        env_file: str | Path | None = None,
    ) -> "Settings":

        load_dotenv(dotenv_path=env_file, override=False)

        api_base_url = _validate_url(
            _get_required_variable("API_BASE_URL")
        )

        api_token_value = os.getenv("API_TOKEN")
        api_token = (
            api_token_value.strip()
            if api_token_value and api_token_value.strip()
            else None
        )

        request_timeout = _get_positive_integer(
            "REQUEST_TIMEOUT",
            default=30,
        )

        max_retries = _get_positive_integer(
            "MAX_RETRIES",
            default=3,
        )

        page_size = _get_positive_integer(
            "PAGE_SIZE",
            default=100,
        )

        output_directory = Path(
            os.getenv("OUTPUT_DIRECTORY", "reports")
        )

        log_level = os.getenv("LOG_LEVEL", "INFO").strip().upper()

        allowed_log_levels = {
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
        }

        if log_level not in allowed_log_levels:
            raise ConfigError(
                "LOG_LEVEL must be one of: "
                + ", ".join(sorted(allowed_log_levels))
            )

        return cls(
            api_base_url=api_base_url,
            api_token=api_token,
            request_timeout=request_timeout,
            max_retries=max_retries,
            page_size=page_size,
            output_directory=output_directory,
            log_level=log_level,
        )
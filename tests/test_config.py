from pathlib import Path

import pytest

from api_collector.config import ConfigError, Settings


def test_loads_valid_configuration(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_BASE_URL", "https://example.com/api/")
    monkeypatch.setenv("API_TOKEN", "test-token")
    monkeypatch.setenv("REQUEST_TIMEOUT", "60")
    monkeypatch.setenv("MAX_RETRIES", "5")
    monkeypatch.setenv("PAGE_SIZE", "250")
    monkeypatch.setenv("OUTPUT_DIRECTORY", "output")
    monkeypatch.setenv("LOG_LEVEL", "debug")

    settings = Settings.from_env(env_file="missing.env")

    assert settings.api_base_url == "https://example.com/api"
    assert settings.api_token == "test-token"
    assert settings.request_timeout == 60
    assert settings.max_retries == 5
    assert settings.page_size == 250
    assert settings.output_directory == Path("output")
    assert settings.log_level == "DEBUG"


def test_uses_default_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_BASE_URL", "https://example.com/api")

    monkeypatch.delenv("API_TOKEN", raising=False)
    monkeypatch.delenv("REQUEST_TIMEOUT", raising=False)
    monkeypatch.delenv("MAX_RETRIES", raising=False)
    monkeypatch.delenv("PAGE_SIZE", raising=False)
    monkeypatch.delenv("OUTPUT_DIRECTORY", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)

    settings = Settings.from_env(env_file="missing.env")

    assert settings.api_token is None
    assert settings.request_timeout == 30
    assert settings.max_retries == 3
    assert settings.page_size == 100
    assert settings.output_directory == Path("reports")
    assert settings.log_level == "INFO"


def test_missing_api_base_url_raises_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("API_BASE_URL", raising=False)

    with pytest.raises(
        ConfigError,
        match="Required environment variable 'API_BASE_URL' is missing",
    ):
        Settings.from_env(env_file="missing.env")


def test_invalid_api_url_raises_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("API_BASE_URL", "example.com/api")

    with pytest.raises(
        ConfigError,
        match="API_BASE_URL must start",
    ):
        Settings.from_env(env_file="missing.env")


def test_invalid_page_size_raises_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("API_BASE_URL", "https://example.com/api")
    monkeypatch.setenv("PAGE_SIZE", "abc")

    with pytest.raises(
        ConfigError,
        match="PAGE_SIZE.*must be an integer",
    ):
        Settings.from_env(env_file="missing.env")


def test_negative_timeout_raises_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("API_BASE_URL", "https://example.com/api")
    monkeypatch.setenv("REQUEST_TIMEOUT", "-10")

    with pytest.raises(
        ConfigError,
        match="REQUEST_TIMEOUT.*greater than 0",
    ):
        Settings.from_env(env_file="missing.env")


def test_invalid_log_level_raises_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("API_BASE_URL", "https://example.com/api")
    monkeypatch.setenv("LOG_LEVEL", "DETAILS")

    with pytest.raises(
        ConfigError,
        match="LOG_LEVEL must be one of",
    ):
        Settings.from_env(env_file="missing.env")
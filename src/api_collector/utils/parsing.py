from collections.abc import Mapping
from typing import Any


def get_nested(
    data: Mapping[str, Any],
    *keys: str,
    default: Any = None,
) -> Any:
    """Safely retrieve a value from a nested mapping."""

    current_value: Any = data

    for key in keys:
        if not isinstance(current_value, Mapping):
            return default

        if key not in current_value:
            return default

        current_value = current_value[key]

    return current_value


def normalize_text(
    value: Any,
    default: str | None = None,
) -> str | None:
    """Convert a value to clean text or return the default value."""

    if value is None:
        return default

    text = str(value).strip()

    if not text:
        return default

    return text
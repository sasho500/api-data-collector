from collections.abc import Mapping
from typing import Any, cast

from api_collector.adapters.base import (
    BaseApiAdapter,
    JsonPayload,
)
from api_collector.domain.exceptions import AdapterError
from api_collector.domain.models import DeviceRecord
from api_collector.utils.parsing import (
    get_nested,
    normalize_text,
)


class MockApiAdapter(BaseApiAdapter):
    """Convert records from the mock API to DeviceRecord objects."""

    source_name = "mock"

    def extract_records(
        self,
        payload: JsonPayload,
    ) -> list[Mapping[str, Any]]:
        """Extract records from a list or from a 'results' property."""

        raw_records: Any

        if isinstance(payload, list):
            raw_records = payload
        elif isinstance(payload, Mapping):
            raw_records = payload.get("results", [])
        else:
            raise AdapterError(
                "Mock API payload must be a JSON object or JSON list."
            )

        if not isinstance(raw_records, list):
            raise AdapterError(
                "The 'results' property must contain a JSON list."
            )

        records: list[Mapping[str, Any]] = []

        for index, item in enumerate(raw_records):
            if not isinstance(item, Mapping):
                raise AdapterError(
                    f"Record at index {index} must be a JSON object."
                )

            records.append(
                cast(Mapping[str, Any], item)
            )

        return records

    def normalize(
        self,
        record: Mapping[str, Any],
    ) -> DeviceRecord:
        """Convert one mock API record to the common device model."""

        return DeviceRecord(
            source=self.source_name,
            record_id=normalize_text(
                record.get("id")
            ),
            record_name=normalize_text(
                record.get("name")
            ),
            status=normalize_text(
                record.get("status")
            ),
            ip_address=normalize_text(
                get_nested(
                    record,
                    "network",
                    "ip_address",
                )
            ),
            manufacturer=normalize_text(
                get_nested(
                    record,
                    "hardware",
                    "manufacturer",
                )
            ),
            model=normalize_text(
                get_nested(
                    record,
                    "hardware",
                    "model",
                )
            ),
            serial_number=normalize_text(
                get_nested(
                    record,
                    "hardware",
                    "serial_number",
                )
            ),
        )
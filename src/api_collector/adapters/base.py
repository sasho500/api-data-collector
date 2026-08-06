from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any

from api_collector.domain.models import DeviceRecord


JsonPayload = Mapping[str, Any] | list[Any]


class BaseApiAdapter(ABC):
    """Contract that all API adapters must follow."""

    source_name: str

    @abstractmethod
    def extract_records(
        self,
        payload: JsonPayload,
    ) -> list[Mapping[str, Any]]:
        """Extract raw records from an API response."""

    @abstractmethod
    def normalize(
        self,
        record: Mapping[str, Any],
    ) -> DeviceRecord:
        """Convert one raw API record to the common device model."""

    def normalize_many(
        self,
        payload: JsonPayload,
    ) -> list[DeviceRecord]:
        """Extract and normalize all records from an API response."""

        raw_records = self.extract_records(payload)

        return [
            self.normalize(record)
            for record in raw_records
        ]
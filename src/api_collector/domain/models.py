from dataclasses import dataclass, field
from datetime import datetime, timezone


def current_utc_time() -> datetime:
    """Return the current timezone-aware UTC time."""

    return datetime.now(timezone.utc)


@dataclass(frozen=True, slots=True)
class DeviceRecord:
    """Normalized representation of a device received from an API."""

    source: str
    record_id: str | None
    record_name: str | None
    status: str | None
    ip_address: str | None
    manufacturer: str | None
    model: str | None
    serial_number: str | None
    collected_at: datetime = field(default_factory=current_utc_time)

    def to_dict(self) -> dict[str, str]:
        """Convert the normalized record to a CSV-compatible dictionary."""

        return {
            "SOURCE": self.source,
            "RECORD_ID": self.record_id or "",
            "RECORD_NAME": self.record_name or "",
            "STATUS": self.status or "",
            "IP_ADDRESS": self.ip_address or "",
            "MANUFACTURER": self.manufacturer or "",
            "MODEL": self.model or "",
            "SERIAL_NUMBER": self.serial_number or "",
            "COLLECTED_AT": self.collected_at.isoformat(),
        }
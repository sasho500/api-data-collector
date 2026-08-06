import pytest

from api_collector.adapters.mock_api import MockApiAdapter
from api_collector.domain.exceptions import AdapterError


def test_adapter_normalizes_complete_record() -> None:
    adapter = MockApiAdapter()

    raw_record = {
        "id": 101,
        "name": "  router-demo-01  ",
        "status": "active",
        "network": {
            "ip_address": "192.0.2.10",
        },
        "hardware": {
            "manufacturer": "Cisco",
            "model": "ISR 4331",
            "serial_number": "ABC123",
        },
    }

    result = adapter.normalize(raw_record)

    assert result.source == "mock"
    assert result.record_id == "101"
    assert result.record_name == "router-demo-01"
    assert result.status == "active"
    assert result.ip_address == "192.0.2.10"
    assert result.manufacturer == "Cisco"
    assert result.model == "ISR 4331"
    assert result.serial_number == "ABC123"


def test_adapter_handles_missing_nested_fields() -> None:
    adapter = MockApiAdapter()

    raw_record = {
        "id": 102,
        "name": "switch-demo-01",
    }

    result = adapter.normalize(raw_record)

    assert result.record_id == "102"
    assert result.record_name == "switch-demo-01"
    assert result.ip_address is None
    assert result.manufacturer is None
    assert result.model is None
    assert result.serial_number is None


def test_adapter_extracts_records_from_results() -> None:
    adapter = MockApiAdapter()

    payload = {
        "results": [
            {
                "id": 101,
                "name": "router-demo-01",
            },
            {
                "id": 102,
                "name": "switch-demo-01",
            },
        ]
    }

    records = adapter.extract_records(payload)

    assert len(records) == 2
    assert records[0]["id"] == 101
    assert records[1]["id"] == 102


def test_adapter_accepts_top_level_list() -> None:
    adapter = MockApiAdapter()

    payload = [
        {
            "id": 101,
            "name": "router-demo-01",
        }
    ]

    records = adapter.extract_records(payload)

    assert len(records) == 1
    assert records[0]["name"] == "router-demo-01"


def test_normalize_many_returns_device_records() -> None:
    adapter = MockApiAdapter()

    payload = {
        "results": [
            {
                "id": 101,
                "name": "router-demo-01",
            },
            {
                "id": 102,
                "name": "switch-demo-01",
            },
        ]
    }

    records = adapter.normalize_many(payload)

    assert len(records) == 2
    assert records[0].record_name == "router-demo-01"
    assert records[1].record_name == "switch-demo-01"


def test_adapter_rejects_invalid_results_structure() -> None:
    adapter = MockApiAdapter()

    payload = {
        "results": "not-a-list",
    }

    with pytest.raises(
        AdapterError,
        match="'results' property must contain a JSON list",
    ):
        adapter.extract_records(payload)


def test_adapter_rejects_non_object_record() -> None:
    adapter = MockApiAdapter()

    payload = {
        "results": [
            {
                "id": 101,
            },
            "invalid-record",
        ]
    }

    with pytest.raises(
        AdapterError,
        match="Record at index 1 must be a JSON object",
    ):
        adapter.extract_records(payload)
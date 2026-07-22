import datetime
from unittest.mock import Mock

import pytest
from django.utils import timezone

from utils.ical import generate_ics, snake_case_name


def _make_mock_reservation(client_name="John Doe", slot_name="Morning", date=None, equipment="Harness"):
    r = Mock()
    r.client = Mock()
    r.client.__str__ = Mock(return_value=client_name)
    r.class_slot = Mock()
    r.class_slot.__str__ = Mock(return_value=slot_name)
    r.class_slot.time = datetime.time(9, 0)
    r.date = date or timezone.localdate()
    r.equipment = Mock()
    r.equipment.__str__ = Mock(return_value=equipment)
    return r


class TestSnakeCaseName:
    def test_basic(self):
        assert snake_case_name("John", "Doe") == "john_doe"

    def test_accents(self):
        assert snake_case_name("José", "González") == "jose_gonzalez"

    def test_empty(self):
        result = snake_case_name("", "")
        assert result == "" or result == "_"


def _unfold(ics_bytes):
    return ics_bytes.replace(b"\r\n ", b"")


class TestGenerateIcs:
    def test_returns_bytes(self):
        r = _make_mock_reservation()
        result = generate_ics([r], prodid="-//test//Test//EN")
        assert isinstance(result, bytes)
        assert result.startswith(b"BEGIN:VCALENDAR")

    def test_includes_prodid(self):
        r = _make_mock_reservation()
        result = generate_ics([r], prodid="-//test//Custom//EN")
        assert b"-//test//Custom//EN" in result

    def test_includes_event(self):
        r = _make_mock_reservation()
        result = generate_ics([r])
        assert b"BEGIN:VEVENT" in result
        assert b"END:VEVENT" in result

    def test_includes_reservation_fields(self):
        r = _make_mock_reservation(client_name="Alice", slot_name="Evening", equipment="Rope")
        result = _unfold(generate_ics([r]))
        assert b"Alice" in result
        assert b"Evening" in result
        assert b"Rope" in result

    def test_multiple_reservations(self):
        r1 = _make_mock_reservation(client_name="Alice", slot_name="Morning")
        r2 = _make_mock_reservation(client_name="Bob", slot_name="Evening")
        result = generate_ics([r1, r2])
        assert result.count(b"BEGIN:VEVENT") == 2
        assert result.count(b"END:VEVENT") == 2

    def test_extra_fields_fn(self):
        r = _make_mock_reservation()
        def extra_fn(_res):
            return {"Pago": "PAY-001"}
        result = _unfold(generate_ics([r], extra_fields_fn=extra_fn))
        assert b"Pago: PAY-001" in result

    def test_empty_reservations(self):
        result = generate_ics([], prodid="-//test//Empty//EN")
        assert b"BEGIN:VCALENDAR" in result
        assert b"BEGIN:VEVENT" not in result

    def test_timezone_included(self):
        r = _make_mock_reservation()
        result = generate_ics([r])
        assert b"America/Denver" in result

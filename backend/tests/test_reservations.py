import datetime
import json
from datetime import date

import pytest
from django.contrib.auth.models import User
from django.test import Client as HttpClient

from apps.classes.models import ClassSlot
from apps.reservations.views import auto_date_for_slot


@pytest.fixture
def http_client():
    return HttpClient()


@pytest.fixture
def staff_user(db):
    return User.objects.create_user(username="staff", password="pass", is_staff=True)


@pytest.fixture
def logged_client(http_client, staff_user):
    http_client.force_login(staff_user)
    return http_client


@pytest.fixture
def class_slots(db):
    ClassSlot.objects.create(day_of_week=0, time="17:30")  # Monday 17:30
    ClassSlot.objects.create(day_of_week=0, time="18:30")  # Monday 18:30
    ClassSlot.objects.create(day_of_week=1, time="17:30")  # Tuesday 17:30
    ClassSlot.objects.create(day_of_week=1, time="18:30")  # Tuesday 18:30
    ClassSlot.objects.create(day_of_week=2, time="17:30")  # Wednesday 17:30
    ClassSlot.objects.create(day_of_week=2, time="18:30")  # Wednesday 18:30
    ClassSlot.objects.create(day_of_week=3, time="17:30")  # Thursday 17:30
    ClassSlot.objects.create(day_of_week=4, time="17:30")  # Friday 17:30
    ClassSlot.objects.create(day_of_week=4, time="18:30")  # Friday 18:30


@pytest.mark.django_db
class TestAutoDate:
    """TDD tests for auto-date calculation — must fail before implementation."""

    def _slot_id(self, day, time_str):
        return ClassSlot.objects.get(day_of_week=day, time=time_str).pk

    def test_same_day_goes_to_next_week(self, class_slots):
        """T001: Slot day matches today → next week."""
        slot_id = self._slot_id(date.today().weekday(), "17:30")
        result = auto_date_for_slot(slot_id)
        assert result is not None
        result_date = date.fromisoformat(result)
        diff = (result_date - date.today()).days
        assert diff == 7, f"Expected exactly 7 days ahead (next week), got {diff}"

    def test_future_day_goes_to_next_week(self, class_slots, monkeypatch):
        """T002: Slot day is a future day this week → next week (not this week)."""

        class MockDate(datetime.date):
            @classmethod
            def today(cls):
                return datetime.date(2026, 7, 13)  # Monday

        monkeypatch.setattr("apps.reservations.views.date", MockDate)
        frozen_today = MockDate.today()
        future_day = 2  # Wednesday
        expected_diff = future_day - 0 + 7  # 9 days
        slot_id = self._slot_id(future_day, "17:30")
        result = auto_date_for_slot(slot_id)
        assert result is not None
        result_date = date.fromisoformat(result)
        diff = (result_date - frozen_today).days
        assert diff == expected_diff, f"Expected diff {expected_diff} (next week), got {diff}"
        assert result_date.weekday() == future_day, (
            f"Expected weekday {future_day}, got {result_date.weekday()}"
        )

    def test_past_day_goes_to_next_week(self, class_slots):
        """T003: Slot day is a past day this week → next week."""
        today = date.today().weekday()
        past_day = (today - 1) % 5  # Yesterday (wrapping to Fri if today is Mon)
        slot_id = self._slot_id(past_day, "17:30")
        result = auto_date_for_slot(slot_id)
        assert result is not None
        result_date = date.fromisoformat(result)
        diff = (result_date - date.today()).days
        # Must be in the future, and the day-of-week must match the slot
        assert diff >= 6, f"Expected at least 6 days ahead, got {diff}"
        assert result_date.weekday() == past_day, (
            f"Expected weekday {past_day}, got {result_date.weekday()}"
        )

    def test_invalid_slot_returns_none(self):
        """T004: Non-existent slot returns None."""
        result = auto_date_for_slot(99999)
        assert result is None

    def test_same_day_always_goes_to_next_week(self, class_slots):
        """T008: Same-day slot regardless of time → next week."""
        slot_id = self._slot_id(date.today().weekday(), "18:30")
        result = auto_date_for_slot(slot_id)
        assert result is not None
        result_date = date.fromisoformat(result)
        assert (result_date - date.today()).days == 7, (
            "Same-day should always go to next week"
        )


@pytest.mark.django_db
class TestReservationCreatePage:
    """Integration tests for the reservation create page."""

    def test_class_slots_json_in_context(self, logged_client, class_slots):
        """T009: Class slots JSON is present in the page."""
        response = logged_client.get("/reservations/create/")
        assert response.status_code == 200
        assert "slots_data" in response.context
        data = response.context["slots_data"]
        assert len(data) > 0
        assert "id" in data[0]
        assert "day_of_week" in data[0]
        assert "time" in data[0]

    def test_auto_date_js_in_page(self, logged_client):
        """Auto-date JS script tag is present."""
        response = logged_client.get("/reservations/create/")
        assert response.status_code == 200
        html = response.content.decode()
        assert "auto-date.js" in html
        assert "class-slots-data" in html

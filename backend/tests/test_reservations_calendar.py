import datetime

import pytest
from django.contrib.auth.models import User
from django.test import Client as HttpClient
from django.urls import reverse

from apps.classes.models import ClassSlot
from apps.clients.models import Client
from apps.equipment.models import Equipment
from apps.payments.models import Payment, PaymentReservation
from apps.reservations.models import Reservation


@pytest.fixture
def http_client():
    return HttpClient()


@pytest.fixture
def staff_user(db):
    return User.objects.create_user(username="staff", password="pass", is_staff=True)


@pytest.fixture
def logged_client(http_client, staff_user):
    http_client.login(username="staff", password="pass")
    return http_client


@pytest.fixture
def client_obj(db):
    return Client.objects.create(first_name="John", last_name="Doe")


@pytest.fixture
def class_slot(db):
    return ClassSlot.objects.create(day_of_week=0, time=datetime.time(9, 0))


@pytest.fixture
def equipment(db):
    return Equipment.objects.create(name="Harness", status="in-service")


@pytest.fixture
def payment(db, client_obj, staff_user):
    return Payment.objects.create(
        client=client_obj,
        payment_identifier="PAY-001",
        amount=100.00,
        date=datetime.date.today(),
        payment_type="cash",
        class_slot_count=2,
        created_by=staff_user,
    )


@pytest.fixture
def reservations(db, client_obj, class_slot, equipment, payment):
    today = datetime.date.today()
    created = []
    for i, day_offset in enumerate([1, 2, 3]):
        r = Reservation.objects.create(
            client=client_obj,
            class_slot=class_slot,
            date=today + datetime.timedelta(days=day_offset),
            equipment=equipment,
            status="reserved",
        )
        if i < 2:
            PaymentReservation.objects.create(payment=payment, reservation=r)
        created.append(r)
    return created


class TestReservationsCalendarDownload:
    def _get_calendar(self, client, start_date=None, end_date=None):
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return client.get(reverse("reservations:reservation-calendar"), params)

    def test_unauthenticated_redirects_to_login(self, http_client, reservations):
        response = self._get_calendar(http_client, "2026-01-01", "2026-12-31")
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_download_returns_ics_content_type(self, logged_client, reservations):
        today = datetime.date.today()
        response = self._get_calendar(
            logged_client,
            today.isoformat(),
            (today + datetime.timedelta(days=10)).isoformat(),
        )
        assert response.status_code == 200
        assert response["Content-Type"].startswith("text/calendar")

    def test_download_ics_contains_vevent(self, logged_client, reservations):
        today = datetime.date.today()
        response = self._get_calendar(
            logged_client,
            today.isoformat(),
            (today + datetime.timedelta(days=10)).isoformat(),
        )
        content = response.content.replace(b"\r\n ", b"")
        assert b"BEGIN:VEVENT" in content
        assert b"END:VEVENT" in content
        assert content.count(b"BEGIN:VEVENT") == len(reservations)

    def test_download_contains_payment_identifier(self, logged_client, reservations):
        today = datetime.date.today()
        response = self._get_calendar(
            logged_client,
            today.isoformat(),
            (today + datetime.timedelta(days=10)).isoformat(),
        )
        content = response.content.replace(b"\r\n ", b"")
        assert b"PAY-001" in content

    def test_download_filename_format(self, logged_client, reservations):
        today = datetime.date.today()
        response = self._get_calendar(
            logged_client,
            today.isoformat(),
            (today + datetime.timedelta(days=10)).isoformat(),
        )
        disposition = response["Content-Disposition"]
        assert disposition.startswith("attachment;")
        assert disposition.endswith(".ics\"")

    def test_empty_range_shows_message(self, logged_client):
        response = self._get_calendar(
            logged_client,
            "2020-01-01",
            "2020-01-31",
        )
        assert response.status_code in (200, 302)

    def test_missing_parameters(self, logged_client):
        response = self._get_calendar(logged_client)
        assert response.status_code in (302, 400)

    def test_unassociated_reservations(self, logged_client, client_obj, class_slot, equipment):
        today = datetime.date.today()
        Reservation.objects.create(
            client=client_obj,
            class_slot=class_slot,
            date=today + datetime.timedelta(days=5),
            equipment=equipment,
            status="reserved",
        )
        response = self._get_calendar(
            logged_client,
            today.isoformat(),
            (today + datetime.timedelta(days=10)).isoformat(),
        )
        content = response.content.replace(b"\r\n ", b"")
        assert b"Reservaci" in content

    def test_multiple_payments_in_range(self, logged_client, client_obj, class_slot, equipment, staff_user, reservations, payment):
        today = datetime.date.today()
        payment2 = Payment.objects.create(
            client=client_obj,
            payment_identifier="PAY-002",
            amount=50.00,
            date=datetime.date.today(),
            payment_type="cash",
            class_slot_count=1,
            created_by=staff_user,
        )
        r = Reservation.objects.create(
            client=client_obj,
            class_slot=class_slot,
            date=today + datetime.timedelta(days=4),
            equipment=equipment,
            status="reserved",
        )
        PaymentReservation.objects.create(payment=payment2, reservation=r)
        response = self._get_calendar(
            logged_client,
            today.isoformat(),
            (today + datetime.timedelta(days=10)).isoformat(),
        )
        content = response.content.replace(b"\r\n ", b"")
        assert b"PAY-001" in content
        assert b"PAY-002" in content

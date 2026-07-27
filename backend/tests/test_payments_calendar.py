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
    http_client.force_login(staff_user)
    return http_client


@pytest.fixture
def client(db):
    return Client.objects.create(first_name="John", last_name="Doe")


@pytest.fixture
def class_slot(db):
    return ClassSlot.objects.create(day_of_week=0, time=datetime.time(10, 0))


@pytest.fixture
def equipment(db):
    return Equipment.objects.create(name="Treadmill", equipment_type="treadmill")


@pytest.fixture
def payment(db, client, staff_user):
    return Payment.objects.create(
        client=client,
        amount=100.00,
        payment_type="CC",
        date=datetime.date(2026, 7, 21),
        class_slot_count=3,
        created_by=staff_user,
    )


@pytest.fixture
def reservation(db, client, class_slot, equipment, staff_user):
    return Reservation.objects.create(
        client=client,
        equipment=equipment,
        class_slot=class_slot,
        date="2026-07-21",
        created_by=staff_user,
    )


@pytest.fixture
def payment_reservation(db, payment, reservation):
    return PaymentReservation.objects.create(
        payment=payment,
        reservation=reservation,
    )


@pytest.mark.django_db
class TestPaymentCalendarDownload:

    def test_download_returns_ics_content_type(self, logged_client, payment, payment_reservation):
        url = reverse("payments:calendar", args=[payment.pk])
        response = logged_client.get(url)
        assert response.status_code == 200
        assert response["Content-Type"] == "text/calendar; charset=utf-8"

    def test_download_filename_format(self, logged_client, payment, payment_reservation):
        url = reverse("payments:calendar", args=[payment.pk])
        response = logged_client.get(url)
        disposition = response["Content-Disposition"]
        assert disposition.startswith("attachment;")
        assert "john_doe" in disposition
        assert payment.payment_identifier in disposition
        assert "20260721" in disposition
        assert disposition.endswith(".ics\"")

    def test_download_contains_vevent(self, logged_client, payment, payment_reservation):
        url = reverse("payments:calendar", args=[payment.pk])
        response = logged_client.get(url)
        content = response.content.decode()
        assert "VEVENT" in content
        assert "John" in content
        assert "Doe" in content
        assert "Treadmill" in content
        assert payment.payment_identifier in content
        assert "Pago" in content

    def test_unauthenticated_redirects_to_login(self, http_client, payment, payment_reservation):
        url = reverse("payments:calendar", args=[payment.pk])
        response = http_client.get(url)
        assert response.status_code == 302

    def test_nonexistent_payment_returns_404(self, logged_client):
        url = reverse("payments:calendar", args=[9999])
        response = logged_client.get(url)
        assert response.status_code == 404

    def test_empty_payment_shows_message(self, logged_client, payment):
        url = reverse("payments:calendar", args=[payment.pk])
        response = logged_client.get(url, follow=True)
        assert response.status_code == 200
        content = response.content.decode()
        assert "No reservations are associated" in content

    def test_single_reservation_filename(self, logged_client, payment, payment_reservation):
        url = reverse("payments:calendar", args=[payment.pk])
        response = logged_client.get(url)
        disposition = response["Content-Disposition"]
        parts = disposition.split("_")
        first_date = parts[-2]
        last_date = parts[-1].replace(".ics\"", "")
        assert first_date == last_date

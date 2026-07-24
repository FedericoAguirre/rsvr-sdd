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
def client_obj(db):
    return Client.objects.create(first_name="John", last_name="Doe")


@pytest.fixture
def class_slot(db):
    return ClassSlot.objects.create(day_of_week=0, time=datetime.time(10, 0))


@pytest.fixture
def equipment(db):
    return Equipment.objects.create(name="Treadmill", equipment_type="treadmill")


@pytest.fixture
def reservation(db, client_obj, class_slot, equipment, staff_user):
    return Reservation.objects.create(
        client=client_obj,
        equipment=equipment,
        class_slot=class_slot,
        date="2026-06-15",
        created_by=staff_user,
    )


@pytest.mark.django_db
class TestClientCalendarDownload:

    def test_download_returns_ics_content_type(self, logged_client, client_obj, reservation):
        url = reverse("clients:client-calendar", args=[client_obj.pk])
        response = logged_client.get(url, {"start_date": "2026-06-01", "end_date": "2026-06-30"})
        assert response.status_code == 200
        assert response["Content-Type"] == "text/calendar; charset=utf-8"

    def test_download_filename_format(self, logged_client, client_obj, reservation):
        url = reverse("clients:client-calendar", args=[client_obj.pk])
        response = logged_client.get(url, {"start_date": "2026-06-01", "end_date": "2026-06-30"})
        disposition = response["Content-Disposition"]
        assert disposition.startswith("attachment;")
        assert "cal_john_doe_20260601_20260630.ics" in disposition

    def test_download_ics_contains_vevent(self, logged_client, client_obj, reservation):
        url = reverse("clients:client-calendar", args=[client_obj.pk])
        response = logged_client.get(url, {"start_date": "2026-06-01", "end_date": "2026-06-30"})
        content = response.content.decode()
        assert "VEVENT" in content
        assert "John" in content
        assert "Doe" in content
        assert "Treadmill" in content

    def test_unauthenticated_redirects_to_login(self, http_client, client_obj, reservation):
        url = reverse("clients:client-calendar", args=[client_obj.pk])
        response = http_client.get(url, {"start_date": "2026-06-01", "end_date": "2026-06-30"})
        assert response.status_code == 302

    def test_nonexistent_client_returns_404(self, logged_client):
        url = reverse("clients:client-calendar", args=[9999])
        response = logged_client.get(url, {"start_date": "2026-06-01", "end_date": "2026-06-30"})
        assert response.status_code == 404

    def test_empty_range_shows_message(self, logged_client, client_obj):
        url = reverse("clients:client-calendar", args=[client_obj.pk])
        response = logged_client.get(url, {"start_date": "2026-01-01", "end_date": "2026-01-31"})
        assert response.status_code == 302
        follow_response = logged_client.get(response.url)
        content = follow_response.content.decode()
        assert "Sin reservas" in content

    def test_invalid_date_order_shows_error(self, logged_client, client_obj, reservation):
        url = reverse("clients:client-calendar", args=[client_obj.pk])
        response = logged_client.get(url, {"start_date": "2026-06-30", "end_date": "2026-06-01"})
        assert response.status_code == 302
        follow_response = logged_client.get(response.url)
        content = follow_response.content.decode()
        assert "anterior a la fecha de fin" in content

    def test_download_with_payment_identifier(self, logged_client, client_obj, class_slot, equipment, staff_user):
        reservation = Reservation.objects.create(
            client=client_obj, equipment=equipment, class_slot=class_slot,
            date="2026-06-15", created_by=staff_user,
        )
        payment = Payment.objects.create(
            client=client_obj, payment_identifier="PAY-001", amount=100.00,
            date="2026-06-15", payment_type="cash", class_slot_count=1,
            created_by=staff_user,
        )
        PaymentReservation.objects.create(payment=payment, reservation=reservation)
        url = reverse("clients:client-calendar", args=[client_obj.pk])
        response = logged_client.get(url, {"start_date": "2026-06-01", "end_date": "2026-06-30"})
        content = response.content.replace(b"\r\n ", b"")
        assert b"PAY-001" in content

    def test_download_without_payment_shows_unassociated(self, logged_client, client_obj, class_slot, equipment, staff_user):
        Reservation.objects.create(
            client=client_obj, equipment=equipment, class_slot=class_slot,
            date="2026-06-15", created_by=staff_user,
        )
        url = reverse("clients:client-calendar", args=[client_obj.pk])
        response = logged_client.get(url, {"start_date": "2026-06-01", "end_date": "2026-06-30"})
        content = response.content.replace(b"\r\n ", b"")
        assert b"Reservaci" in content

    def test_special_chars_in_client_name_handled(self, logged_client, class_slot, equipment, staff_user):
        client = Client.objects.create(first_name="María José", last_name="González")
        Reservation.objects.create(
            client=client, equipment=equipment, class_slot=class_slot,
            date="2026-06-15", created_by=staff_user,
        )
        url = reverse("clients:client-calendar", args=[client.pk])
        response = logged_client.get(url, {"start_date": "2026-06-01", "end_date": "2026-06-30"})
        assert response.status_code == 200
        disposition = response["Content-Disposition"]
        assert "maria_jose_gonzalez" in disposition.lower()

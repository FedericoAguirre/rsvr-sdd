import datetime

import pytest
from django.contrib.auth.models import User
from django.test import Client as HttpClient

from apps.classes.models import ClassSlot
from apps.clients.models import Client
from apps.equipment.models import Equipment
from apps.payments.models import Payment, PaymentReservation
from apps.reservations.models import Reservation

pytestmark = pytest.mark.django_db


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
    return Client.objects.create(
        first_name="Jane", last_name="Smith", mobile="+9876543210",
    )


@pytest.fixture
def class_slot(db):
    return ClassSlot.objects.create(day_of_week=1, time=datetime.time(10, 0))


@pytest.fixture
def equipment_item(db):
    return Equipment.objects.create(name="Treadmill", equipment_type="treadmill")


@pytest.fixture
def reservation(client, class_slot, equipment_item, staff_user):
    return Reservation.objects.create(
        client=client,
        class_slot=class_slot,
        equipment=equipment_item,
        date="2026-07-16",
        status="reserved",
        created_by=staff_user,
    )


@pytest.fixture
def payment(client, staff_user):
    return Payment.objects.create(
        client=client,
        amount=200.00,
        payment_type="CASH",
        date=datetime.date(2026, 7, 16),
        class_slot_count=4,
        created_by=staff_user,
    )


@pytest.fixture
def payment_reservation(payment, reservation):
    return PaymentReservation.objects.create(
        payment=payment, reservation=reservation
    )


class TestReservationsGridColumnOrder:
    def test_columns_in_correct_order(self, logged_client, client, payment_reservation):
        response = logged_client.get(f"/payments/{payment_reservation.payment.pk}/")
        html = response.content.decode()
        thead_start = html.find("<thead>")
        thead_end = html.find("</thead>")
        assert thead_start != -1, "<thead> not found"
        assert thead_end != -1, "</thead> not found"
        thead_html = html[thead_start:thead_end]
        clase_idx = thead_html.find("Bloque de clase")
        fecha_idx = thead_html.find("Fecha")
        equipo_idx = thead_html.find("Equipo")
        estado_idx = thead_html.find("Estado")
        assert clase_idx != -1, "Bloque de clase column not found in <thead>"
        assert fecha_idx != -1, "Fecha column not found in <thead>"
        assert equipo_idx != -1, "Equipo column not found in <thead>"
        assert estado_idx != -1, "Estado column not found in <thead>"
        assert (
            clase_idx < fecha_idx < equipo_idx < estado_idx
        ), f"Expected Bloque de clase < Fecha < Equipo < Estado in <thead>, got positions: Bloque de clase={clase_idx}, Fecha={fecha_idx}, Equipo={equipo_idx}, Estado={estado_idx}"

    def test_table_has_striped_class(self, logged_client, client, payment_reservation):
        response = logged_client.get(f"/payments/{payment_reservation.payment.pk}/")
        html = response.content.decode()
        assert "table-striped" in html, "table-striped class not found on page"


class TestReservationsGridEmpty:
    def test_no_reservations_hides_section(self, logged_client, client, payment):
        response = logged_client.get(f"/payments/{payment.pk}/")
        html = response.content.decode()
        assert "Reservas asociadas" not in html

import datetime

import pytest
from django.contrib.auth.models import User
from django.test import Client as HttpClient

from apps.clients.models import Client
from apps.classes.models import ClassSlot
from apps.equipment.models import Equipment
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


class TestReservationHistoryColumnOrder:
    def test_columns_in_correct_order(self, logged_client, client, reservation):
        response = logged_client.get(f"/clients/{client.pk}/")
        html = response.content.decode()
        thead_start = html.find("<thead>")
        thead_end = html.find("</thead>")
        assert thead_start != -1, "<thead> not found"
        assert thead_end != -1, "</thead> not found"
        thead_html = html[thead_start:thead_end]
        clase_idx = thead_html.find("Clase")
        fecha_idx = thead_html.find("Fecha")
        equipo_idx = thead_html.find("Equipo")
        assert clase_idx != -1, "Clase column not found in <thead>"
        assert fecha_idx != -1, "Fecha column not found in <thead>"
        assert equipo_idx != -1, "Equipo column not found in <thead>"
        assert (
            clase_idx < fecha_idx < equipo_idx
        ), f"Expected Clase < Fecha < Equipo in <thead>, got positions: Clase={clase_idx}, Fecha={fecha_idx}, Equipo={equipo_idx}"

    def test_empty_history_renders(self, logged_client, client):
        response = logged_client.get(f"/clients/{client.pk}/")
        html = response.content.decode()
        assert "Sin reservas" in html or "No reservations" in html

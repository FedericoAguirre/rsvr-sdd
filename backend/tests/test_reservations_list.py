import datetime

import pytest
from django.test import Client as HttpClient
from django.contrib.auth.models import User
from apps.clients.models import Client
from apps.equipment.models import Equipment
from apps.classes.models import ClassSlot
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
def class_slot(db):
    return ClassSlot.objects.create(day_of_week=0, time=datetime.time(10, 0))


@pytest.fixture
def equipment_list(db):
    names = ["Treadmill", "Bike", "Elliptical", "Rower"]
    types = ["treadmill", "bike", "elliptical", "rower"]
    return [
        Equipment.objects.create(name=name, equipment_type=etype)
        for name, etype in zip(names, types)
    ]


@pytest.fixture
def client_list(db):
    return [
        Client.objects.create(first_name="Alice", last_name="A"),
        Client.objects.create(first_name="Bob", last_name="B"),
        Client.objects.create(first_name="Charlie", last_name="C"),
        Client.objects.create(first_name="Diana", last_name="D"),
    ]


@pytest.fixture
def reservations_for_slot(db, class_slot, equipment_list, client_list, staff_user):
    date = "2026-06-15"
    for i, (equip, client) in enumerate(zip(equipment_list, client_list)):
        Reservation.objects.create(
            client=client,
            equipment=equip,
            class_slot=class_slot,
            date=date,
            created_by=staff_user,
        )


@pytest.mark.django_db
class TestReservationsList:

    def test_list_page_renders_header(self, logged_client, class_slot, reservations_for_slot):
        response = logged_client.get(
            f"/reservations/list/?class_slot={class_slot.pk}&date=2026-06-15"
        )
        content = response.content.decode()
        assert str(class_slot) in content
        assert "2026-06-15" in content

    def test_equipment_ordered_alphabetically(self, logged_client, class_slot, reservations_for_slot):
        response = logged_client.get(
            f"/reservations/list/?class_slot={class_slot.pk}&date=2026-06-15"
        )
        content = response.content.decode()
        bike_pos = content.index("Bike")
        elliptical_pos = content.index("Elliptical")
        rower_pos = content.index("Rower")
        treadmill_pos = content.index("Treadmill")
        assert bike_pos < elliptical_pos, "Bike should come before Elliptical"
        assert elliptical_pos < rower_pos, "Elliptical should come before Rower"
        assert rower_pos < treadmill_pos, "Rower should come before Treadmill"

    def test_empty_state_shows_header_and_empty_table(self, logged_client, class_slot):
        response = logged_client.get(
            f"/reservations/list/?class_slot={class_slot.pk}&date=2026-06-15"
        )
        content = response.content.decode()
        assert str(class_slot) in content
        assert "2026-06-15" in content

    def test_unauthenticated_user_redirected(self, http_client, class_slot):
        response = http_client.get(
            f"/reservations/list/?class_slot={class_slot.pk}&date=2026-06-15"
        )
        assert response.status_code == 302
        assert "/accounts/login/" in response.url


@pytest.mark.django_db
class TestReservationsListPDF:

    def test_pdf_download_content_type(self, logged_client, class_slot, reservations_for_slot):
        response = logged_client.get(
            f"/reservations/list/pdf/?class_slot={class_slot.pk}&date=2026-06-15"
        )
        assert response.status_code == 200
        assert response["Content-Type"] == "application/pdf"

    def test_pdf_empty_list(self, logged_client, class_slot):
        response = logged_client.get(
            f"/reservations/list/pdf/?class_slot={class_slot.pk}&date=2026-06-15"
        )
        assert response.status_code == 200
        assert response["Content-Type"] == "application/pdf"

    def test_export_button_visible_on_list_page(self, logged_client, class_slot, reservations_for_slot):
        response = logged_client.get(
            f"/reservations/list/?class_slot={class_slot.pk}&date=2026-06-15"
        )
        content = response.content.decode()
        assert "/reservations/list/pdf/" in content

import datetime

import pytest
from django.contrib.auth.models import User
from django.test import Client as HttpClient

from apps.clients.models import Client
from apps.equipment.models import Equipment
from apps.payments.models import Payment

pytestmark = pytest.mark.django_db


# ── Fixtures ──────────────────────────────────────────────────────────────────


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
def equipment(db):
    return Equipment.objects.create(name="Treadmill", equipment_type="treadmill")


@pytest.fixture
def payment(client, staff_user):
    return Payment.objects.create(
        client=client,
        amount=200.00,
        payment_type="CASH",
        date=datetime.date.today(),
        class_slot_count=4,
        reference="REF-ASSOC",
        created_by=staff_user,
    )


# ── Tests ─────────────────────────────────────────────────────────────────────


class TestAssociateButtonPresence:
    def test_associate_button_appears_on_detail_page(self, logged_client, payment):
        response = logged_client.get(f"/payments/{payment.pk}/")
        html = response.content.decode()
        assert "Asociar" in html
        assert "Editar" in html

    def test_associate_button_before_edit_in_dom(self, logged_client, payment):
        response = logged_client.get(f"/payments/{payment.pk}/")
        html = response.content.decode()
        card_header_start = html.find('class="card-header')
        card_header = html[card_header_start:]
        associate_idx = card_header.find("Asociar")
        edit_idx = card_header.find("Editar")
        assert associate_idx != -1, "Associate button not found in card header"
        assert edit_idx != -1, "Edit button not found in card header"
        assert associate_idx < edit_idx, (
            f"Asociar (pos {associate_idx}) must appear before Editar (pos {edit_idx}) "
            f"in card header DOM"
        )

    def test_associate_button_href_to_associate_url(self, logged_client, payment):
        response = logged_client.get(f"/payments/{payment.pk}/")
        html = response.content.decode()
        associate_url = f"/payments/{payment.pk}/associate/"
        assert associate_url in html, (
            f"Expected {associate_url} in payment detail page"
        )


class TestAssociateGetView:
    def test_get_associate_returns_200(self, logged_client, payment):
        response = logged_client.get(f"/payments/{payment.pk}/associate/")
        assert response.status_code == 200

    def test_get_associate_includes_context(self, logged_client, payment, client):
        response = logged_client.get(f"/payments/{payment.pk}/associate/")
        assert "available_reservations" in response.context
        assert "payment" in response.context
        assert response.context["payment"].pk == payment.pk
        assert "remaining_slots" in response.context

import pytest
from django.contrib.auth.models import User
from django.test import Client as HttpClient

from apps.clients.models import Client
from apps.payments.models import Payment

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
def payment(client, staff_user):
    return Payment.objects.create(
        client=client,
        amount=200.00,
        payment_type="CASH",
        date="2026-07-08",
        class_slot_count=4,
        reference="REF-BTN",
        created_by=staff_user,
    )


class TestNewPaymentButtonPresence:
    def test_button_appears_on_client_detail_page(self, logged_client, client):
        response = logged_client.get(f"/clients/{client.pk}/")
        html = response.content.decode()
        assert "Nuevo pago" in html

    def test_button_after_new_reservation_in_dom(self, logged_client, client):
        response = logged_client.get(f"/clients/{client.pk}/")
        html = response.content.decode()
        new_res_idx = html.find("Nueva Reserva")
        new_pay_idx = html.find("Nuevo pago")
        assert new_res_idx != -1, "New Reservation button not found in page"
        assert new_pay_idx != -1, "New Payment button not found in page"
        assert new_res_idx < new_pay_idx, (
            f"New Reservation (pos {new_res_idx}) must appear before "
            f"New Payment (pos {new_pay_idx}) in DOM"
        )

    def test_button_href_contains_client_param(self, logged_client, client):
        response = logged_client.get(f"/clients/{client.pk}/")
        html = response.content.decode()
        expected_url = f"/payments/create/?client={client.pk}"
        assert expected_url in html, (
            f"Expected {expected_url} in client detail page"
        )


class TestClientPreselection:
    def test_client_preselected_via_query_param(self, logged_client, client):
        response = logged_client.get(f"/payments/create/?client={client.pk}")
        form = response.context.get("form")
        assert form is not None, "Form not found in response context"
        initial_client = form.initial.get("client")
        assert initial_client is not None, "Client should be preselected"
        assert int(initial_client) == client.pk, (
            f"Expected client {client.pk}, got {initial_client}"
        )

    def test_client_empty_on_direct_access(self, logged_client, client):
        response = logged_client.get("/payments/create/")
        form = response.context.get("form")
        assert form is not None, "Form not found in response context"
        initial_client = form.initial.get("client")
        assert initial_client is None or initial_client == "", (
            "Client should not be preselected on direct access"
        )

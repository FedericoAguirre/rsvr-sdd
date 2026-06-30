import datetime

import pytest
from django.contrib.auth.models import User
from django.test import Client as HttpClient

from apps.clients.models import Client
from apps.payments.models import Payment


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
def active_client(db):
    return Client.objects.create(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        mobile="+1234567890",
        is_active=True,
    )


@pytest.fixture
def inactive_client(db):
    return Client.objects.create(
        first_name="Jane",
        last_name="Smith",
        email="jane@example.com",
        mobile="+0987654321",
        is_active=False,
    )


@pytest.fixture
def payment_for_active(logged_client, active_client, staff_user):
    return Payment.objects.create(
        client=active_client,
        amount=50.00,
        payment_type="CC",
        date=datetime.date.today(),
        class_slot_count=2,
        reference="PAY-ACTIVE",
        created_by=staff_user,
    )


@pytest.fixture
def payment_for_inactive(logged_client, inactive_client, staff_user):
    return Payment.objects.create(
        client=inactive_client,
        amount=75.00,
        payment_type="CASH",
        date=datetime.date.today(),
        class_slot_count=1,
        reference="PAY-INACTIVE",
        created_by=staff_user,
    )


@pytest.mark.django_db
class TestPaymentClientSearch:

    def test_search_by_client_name(
        self, logged_client, payment_for_active, payment_for_inactive,
    ):
        response = logged_client.get("/payments/", {"q": "John"})
        assert response.status_code == 200
        assert payment_for_active.payment_identifier in response.content.decode()
        assert payment_for_inactive.payment_identifier not in response.content.decode()

    def test_search_by_client_email(
        self, logged_client, payment_for_active, active_client,
    ):
        payment = Payment.objects.create(
            client=active_client, amount=30.00, payment_type="DC",
            date=datetime.date.today(), class_slot_count=1,
            reference="PAY-EMAIL", created_by=User.objects.first(),
        )
        response = logged_client.get("/payments/", {"q": "john@example.com"})
        assert response.status_code == 200
        assert payment.payment_identifier in response.content.decode()

    def test_search_by_client_mobile(
        self, logged_client, payment_for_active, active_client,
    ):
        payment = Payment.objects.create(
            client=active_client, amount=20.00, payment_type="CASH",
            date=datetime.date.today(), class_slot_count=1,
            reference="PAY-MOBILE", created_by=User.objects.first(),
        )
        response = logged_client.get("/payments/", {"q": "+1234567890"})
        assert response.status_code == 200
        assert payment.payment_identifier in response.content.decode()

    def test_minimum_three_characters(self, logged_client, payment_for_active):
        response = logged_client.get("/payments/", {"q": "Jo"})
        assert response.status_code == 200
        assert payment_for_active.payment_identifier in response.content.decode()

    def test_case_insensitive_matching(self, logged_client, payment_for_active):
        response = logged_client.get("/payments/", {"q": "john"})
        assert response.status_code == 200
        assert payment_for_active.payment_identifier in response.content.decode()
        response2 = logged_client.get("/payments/", {"q": "JOHN"})
        assert response2.status_code == 200
        assert payment_for_active.payment_identifier in response2.content.decode()

    def test_inactive_client_excluded(
        self, logged_client, payment_for_active, payment_for_inactive,
    ):
        response = logged_client.get("/payments/", {"q": "Jane"})
        assert response.status_code == 200
        assert payment_for_inactive.payment_identifier not in response.content.decode()

    def test_no_results_shows_not_found_message(
        self, logged_client, payment_for_active,
    ):
        response = logged_client.get("/payments/", {"q": "ZZZZZZ"})
        assert response.status_code == 200
        content = response.content.decode()
        assert "No se encontraron pagos que coincidan con su búsqueda" in content

    def test_clear_search_shows_all_payments(
        self, logged_client, payment_for_active, inactive_client,
    ):
        Payment.objects.create(
            client=inactive_client, amount=60.00, payment_type="DC",
            date=datetime.date.today(), class_slot_count=1,
            created_by=User.objects.first(),
        )
        response = logged_client.get("/payments/", {"q": ""})
        assert response.status_code == 200
        assert payment_for_active.payment_identifier in response.content.decode()

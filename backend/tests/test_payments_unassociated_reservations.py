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
def client_obj(db):
    return Client.objects.create(
        first_name="Alice", last_name="Smith",
        email="alice@example.com", mobile="+1111111111", is_active=True,
    )


@pytest.fixture
def equipment(db):
    from apps.equipment.models import Equipment
    return Equipment.objects.create(name="Test Harness", equipment_type="climber")


@pytest.fixture
def class_slot(db):
    from apps.classes.models import ClassSlot
    import datetime
    return ClassSlot.objects.create(day_of_week=0, time=datetime.time(10, 0))


@pytest.fixture
def payment_data(client_obj, staff_user):
    return {
        "client": client_obj,
        "amount": 100.00,
        "payment_type": "CASH",
        "date": datetime.date.today(),
        "class_slot_count": 5,
        "created_by": staff_user,
    }


@pytest.fixture
def reservation_date():
    return datetime.date(2026, 7, 24)


@pytest.mark.django_db
class TestUnassociatedReservations:

    def test_unassociated_reservations_appear_on_page(
        self, logged_client, client_obj, equipment, class_slot, staff_user, reservation_date,
    ):
        from apps.reservations.models import Reservation
        r = Reservation.objects.create(
            client=client_obj, equipment=equipment,
            class_slot=class_slot, date=reservation_date,
            created_by=staff_user,
        )
        response = logged_client.get(f"/payments/client/{client_obj.id}/")
        assert response.status_code == 200
        html = response.content.decode()
        assert str(r.equipment) in html
        assert "reservations without payment" in html.lower() or "reservaciones sin pago" in html.lower()

    def test_associated_reservations_do_not_appear(
        self, logged_client, client_obj, equipment, class_slot, staff_user, payment_data, reservation_date,
    ):
        from apps.reservations.models import Reservation
        from apps.payments.models import PaymentReservation
        payment = Payment.objects.create(**payment_data)
        r = Reservation.objects.create(
            client=client_obj, equipment=equipment,
            class_slot=class_slot, date=reservation_date,
            created_by=staff_user,
        )
        PaymentReservation.objects.create(payment=payment, reservation=r)
        response = logged_client.get(f"/payments/client/{client_obj.id}/")
        assert response.status_code == 200
        html = response.content.decode()
        assert str(r.equipment) not in html

    def test_empty_state_when_all_associated(
        self, logged_client, client_obj, equipment, class_slot, staff_user, payment_data,
    ):
        from apps.reservations.models import Reservation
        from apps.payments.models import PaymentReservation
        payment = Payment.objects.create(**payment_data)
        r = Reservation.objects.create(
            client=client_obj, equipment=equipment,
            class_slot=class_slot, date=datetime.date.today(),
            created_by=staff_user,
        )
        PaymentReservation.objects.create(payment=payment, reservation=r)
        response = logged_client.get(f"/payments/client/{client_obj.id}/")
        html = response.content.decode()
        assert "no tiene reservaciones sin pago" in html.lower() or "no reservations" in html.lower()

    def test_empty_state_when_no_reservations(
        self, logged_client, client_obj,
    ):
        response = logged_client.get(f"/payments/client/{client_obj.id}/")
        assert response.status_code == 200
        html = response.content.decode()
        assert "no tiene reservaciones sin pago" in html.lower() or "no reservations" in html.lower()

    def test_payment_history_unaffected(
        self, logged_client, client_obj, staff_user, payment_data,
    ):
        payment = Payment.objects.create(**payment_data)
        response = logged_client.get(f"/payments/client/{client_obj.id}/")
        assert response.status_code == 200
        html = response.content.decode()
        assert payment.payment_identifier in html

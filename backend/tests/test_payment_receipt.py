import datetime
import io
import time

import pytest
from django.contrib.auth.models import User
from django.test import Client as HttpClient
from pdfminer.high_level import extract_text

from apps.classes.models import ClassSlot
from apps.clients.models import Client
from apps.equipment.models import Equipment
from apps.payments.models import Payment, PaymentReservation
from apps.payments.receipt import build_receipt
from apps.reservations.models import Reservation

pytestmark = pytest.mark.django_db


@pytest.fixture
def operator(db):
    return User.objects.create_user(username="operator", password="pass")


@pytest.fixture
def http_client():
    return HttpClient()


@pytest.fixture
def logged_client(http_client, operator):
    http_client.force_login(operator)
    return http_client


@pytest.fixture
def client(db):
    return Client.objects.create(
        first_name="José",
        last_name="Álvarez",
        mobile="+1234567890",
    )


@pytest.fixture
def class_slot(db):
    return ClassSlot.objects.create(day_of_week=1, time=datetime.time(10, 0))


@pytest.fixture
def equipment_item(db):
    return Equipment.objects.create(name="Cuerda / A", equipment_type="other")


@pytest.fixture
def payment(client, operator):
    return Payment.objects.create(
        client=client,
        amount="200.00",
        payment_type="CASH",
        date=datetime.date(2026, 7, 16),
        class_slot_count=4,
        created_by=operator,
        payment_identifier="PAY-2026-001",
        reference="REF/2026:7",
    )


@pytest.fixture
def reservation(client, class_slot, equipment_item, operator):
    return Reservation.objects.create(
        client=client,
        class_slot=class_slot,
        equipment=equipment_item,
        date=datetime.date(2026, 7, 16),
        status="reserved",
        created_by=operator,
    )


@pytest.fixture
def linked_payment(payment, reservation):
    PaymentReservation.objects.create(payment=payment, reservation=reservation)
    return payment


class TestPaymentReceiptPDF:
    def test_authenticated_download_returns_pdf_with_payment_and_reservation_data(
        self, logged_client, linked_payment, reservation
    ):
        response = logged_client.get(
            f"/api/payments/{linked_payment.pk}/receipt/"
        )

        assert response.status_code == 200
        assert response["Content-Type"] == "application/pdf"
        assert response["Content-Disposition"].startswith("attachment;")
        assert "payment_José_Álvarez_PAY-2026-001.pdf" in response[
            "Content-Disposition"
        ]

        text = extract_text(io.BytesIO(response.content))
        assert "José Álvarez" in text
        assert "Identificador de pago" in text
        assert linked_payment.payment_identifier in text
        assert linked_payment.reference not in text
        assert "200.00" in text
        assert "Efectivo" in text
        assert "16/07/2026" in text
        assert "4" in text
        assert str(reservation.class_slot) in text
        assert "Cuerda / A" in text
        assert "Reservado" in text

    def test_receipt_projection_uses_payment_identifier(self, payment):
        payment.refresh_from_db()
        receipt = build_receipt(payment)

        assert receipt["identifier"] == payment.payment_identifier
        assert payment.reference not in receipt.values()

    def test_empty_payment_includes_localized_empty_state(
        self, logged_client, payment
    ):
        response = logged_client.get(f"/api/payments/{payment.pk}/receipt/")

        assert response.status_code == 200
        text = extract_text(io.BytesIO(response.content))
        assert "No se encontraron reservaciones" in text

    def test_missing_reference_keeps_identifier_and_sanitizes_client_name(
        self, logged_client, payment
    ):
        payment.reference = None
        payment.save(update_fields=["reference"])

        response = logged_client.get(f"/api/payments/{payment.pk}/receipt/")

        assert response.status_code == 200
        assert "payment_José_Álvarez_PAY-2026-001.pdf" in response[
            "Content-Disposition"
        ]

    def test_filename_sanitizes_payment_identifier(self, payment):
        payment.refresh_from_db()
        payment.payment_identifier = "PAY/2026 001\x00"

        receipt = build_receipt(payment)

        assert receipt["filename"] == "payment_José_Álvarez_PAY_2026_001.pdf"
        assert "/" not in receipt["filename"]
        assert payment.reference not in receipt["filename"]

    def test_missing_payment_returns_not_found(self, logged_client):
        response = logged_client.get("/api/payments/999999/receipt/")

        assert response.status_code == 404

    def test_unauthenticated_download_redirects_to_login(self, http_client, payment):
        response = http_client.get(f"/api/payments/{payment.pk}/receipt/")

        assert response.status_code == 302
        assert "/accounts/login/" in response["Location"]

    def test_fifty_reservations_generate_within_ten_seconds(
        self, logged_client, payment, client, class_slot, operator
    ):
        equipment = Equipment.objects.bulk_create(
            [
                Equipment(name=f"Equipment {index}", equipment_type="other")
                for index in range(50)
            ]
        )
        reservations = Reservation.objects.bulk_create(
            [
                Reservation(
                    client=client,
                    class_slot=class_slot,
                    equipment=item,
                    date=datetime.date(2026, 7, 16),
                    status="reserved",
                    created_by=operator,
                )
                for item in equipment
            ]
        )
        PaymentReservation.objects.bulk_create(
            [
                PaymentReservation(payment=payment, reservation=item)
                for item in reservations
            ]
        )

        started = time.perf_counter()
        response = logged_client.get(f"/api/payments/{payment.pk}/receipt/")
        elapsed = time.perf_counter() - started

        assert response.status_code == 200
        assert len(response.content) > 0
        assert elapsed < 10


class TestPaymentReceiptMarkdown:
    def test_markdown_contains_same_receipt_values(
        self, logged_client, linked_payment, reservation
    ):
        response = logged_client.get(
            f"/api/payments/{linked_payment.pk}/receipt/markdown/"
        )

        assert response.status_code == 200
        assert response["Content-Type"] == "text/markdown; charset=utf-8"
        text = response.content.decode()
        assert "José Álvarez" in text
        assert "**Identificador de pago:** PAY-2026-001" in text
        assert "REF/2026:7" not in text
        assert "Cuerda / A" in text
        assert str(reservation.class_slot) in text
        assert "| Bloque de clase | Fecha | Equipo | Estado |" in text

    def test_empty_markdown_includes_empty_state(self, logged_client, payment):
        response = logged_client.get(
            f"/api/payments/{payment.pk}/receipt/markdown/"
        )

        assert response.status_code == 200
        text = response.content.decode()
        assert "**Identificador de pago:** PAY-2026-001" in text
        assert "No se encontraron reservaciones" in text

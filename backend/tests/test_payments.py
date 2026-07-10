import datetime
import io
import json

import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client as HttpClient

from apps.clients.models import Client
from apps.payments.forms import PaymentForm
from apps.payments.models import PAYMENT_TYPE_CHOICES, Payment


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
        first_name="John", last_name="Doe", mobile="+1234567890",
    )


@pytest.fixture
def payment_data(client, staff_user):
    return {
        "client": client,
        "amount": 100.00,
        "payment_type": "CC",
        "date": datetime.date.today(),
        "class_slot_count": 4,
        "reference": "REF001",
        "notes": "Test payment",
        "created_by": staff_user,
    }


# ── T013: Payment model creation with valid data ─────────────────────────────


@pytest.mark.django_db
class TestPaymentCreation:
    def test_create_payment_with_valid_data(self, payment_data):
        payment = Payment.objects.create(**payment_data)
        assert payment.pk is not None
        assert payment.amount == 100.00
        assert payment.payment_type == "CC"
        assert payment.class_slot_count == 4

    def test_payment_identifier_is_auto_generated(self, payment_data):
        payment = Payment.objects.create(**payment_data)
        assert payment.payment_identifier is not None
        assert len(payment.payment_identifier) >= 10
        assert payment.payment_identifier.startswith("CC")
        assert payment.payment_identifier.endswith("001")


# ── T014: Identifier auto-generation format and uniqueness ────────────────────


@pytest.mark.django_db
class TestPaymentIdentifier:
    def test_format_matches_expected_pattern(self, payment_data):
        payment = Payment.objects.create(**payment_data)
        ident = payment.payment_identifier
        # Format: PREFIX(CC) + YYYYMMDD(8) + INITIALS(2) + NNN(3) = 15 chars
        assert len(ident) >= 15
        assert ident[-3:].isdigit()
        assert ident.startswith("CC")
        assert "JD" in ident  # John Doe initials

    def test_identifier_is_unique(self, payment_data):
        Payment.objects.create(**payment_data)
        with pytest.raises(Exception):
            Payment.objects.create(
                **{**payment_data, "payment_identifier": payment_data["payment_identifier"]},
            )

    def test_daily_counter_resets_per_type(self, payment_data, staff_user):
        Payment.objects.create(**payment_data)
        Payment.objects.create(**{**payment_data, "payment_type": "CASH"})
        p1 = Payment.objects.get(payment_type="CC")
        p2 = Payment.objects.get(payment_type="CASH")
        assert p1.payment_identifier.endswith("001")
        assert p2.payment_identifier.endswith("001")


# ── T015: Payment validation ──────────────────────────────────────────────────


@pytest.mark.django_db
class TestPaymentValidation:
    def test_negative_amount_fails(self, payment_data):
        payment_data["amount"] = -10
        payment = Payment(**payment_data)
        with pytest.raises(Exception):
            payment.full_clean()

    def test_zero_class_slot_count_fails(self, payment_data):
        payment_data["class_slot_count"] = 0
        payment = Payment(**payment_data)
        with pytest.raises(Exception):
            payment.full_clean()

    def test_missing_client_fails(self, payment_data):
        payment_data.pop("client")
        payment = Payment(**payment_data)
        with pytest.raises(Exception):
            payment.full_clean()


# ── T016: Optional fields ────────────────────────────────────────────────────


@pytest.mark.django_db
class TestPaymentOptionalFields:
    def test_empty_optional_fields(self, payment_data):
        payment_data["reference"] = None
        payment_data["notes"] = None
        payment_data["evidence"] = None
        payment = Payment.objects.create(**payment_data)
        assert payment.reference is None
        assert payment.notes is None

    def test_optional_fields_saved(self, payment_data):
        img = SimpleUploadedFile("test.png", b"fake-image-data", content_type="image/png")
        payment_data["reference"] = "REF-OPT"
        payment_data["notes"] = "Some notes"
        payment_data["evidence"] = img
        payment = Payment.objects.create(**payment_data)
        assert payment.reference == "REF-OPT"
        assert payment.notes == "Some notes"
        assert payment.evidence is not None


# ── T017: Limited edit ────────────────────────────────────────────────────────


@pytest.mark.django_db
class TestPaymentLimitedEdit:
    def test_only_reference_notes_evidence_editable(self, payment_data):
        payment = Payment.objects.create(**payment_data)
        payment.reference = "UPDATED-REF"
        payment.notes = "Updated notes"
        payment.save()
        payment.refresh_from_db()
        assert payment.reference == "UPDATED-REF"
        assert payment.notes == "Updated notes"

    def test_readonly_fields_unchanged_on_form_submit(self, payment_data, staff_user):
        payment = Payment.objects.create(**payment_data)
        orig_ident = payment.payment_identifier
        orig_client = payment.client
        payment.refresh_from_db()
        assert payment.payment_identifier == orig_ident
        assert payment.client == orig_client


# ── T018: Soft-delete ─────────────────────────────────────────────────────────


@pytest.mark.django_db
class TestPaymentSoftDelete:
    def test_soft_delete_sets_flag(self, payment_data):
        payment = Payment.objects.create(**payment_data)
        payment.is_deleted = True
        payment.save()
        payment.refresh_from_db()
        assert payment.is_deleted is True

    def test_soft_deleted_excluded_from_default_queryset(self, payment_data):
        Payment.objects.create(**payment_data)
        assert Payment.objects.filter(is_deleted=False).count() == 1


# ── T019: PaymentForm validation ──────────────────────────────────────────────


@pytest.mark.django_db
class TestPaymentForm:
    def test_valid_form(self, client, staff_user):
        form = PaymentForm(data={
            "client": client.id,
            "amount": 50.00,
            "payment_type": "CASH",
            "date": datetime.date.today(),
            "class_slot_count": 2,
            "payment_identifier": "",
        })
        assert form.is_valid(), form.errors

    def test_missing_required_field_fails(self, client):
        form = PaymentForm(data={"client": client.id})
        assert not form.is_valid()
        assert "amount" in form.errors

    def test_negative_amount_form_fails(self, client):
        form = PaymentForm(data={
            "client": client.id,
            "amount": -10,
            "payment_type": "CASH",
            "date": datetime.date.today(),
            "class_slot_count": 2,
            "payment_identifier": "",
        })
        assert not form.is_valid()

    def test_zero_class_slot_count_form_fails(self, client):
        form = PaymentForm(data={
            "client": client.id,
            "amount": 50,
            "payment_type": "CASH",
            "date": datetime.date.today(),
            "class_slot_count": 0,
            "payment_identifier": "",
        })
        assert not form.is_valid()


# ── T030-T032: US2 — Client Payment History ──────────────────────────────────


@pytest.mark.django_db
class TestPaymentHistory:
    def test_list_returns_paginated_payments(self, logged_client, payment_data):
        for i in range(3):
            p = Payment.objects.create(**{**payment_data, "payment_type": "CASH"})
        response = logged_client.get("/payments/")
        assert response.status_code == 200
        assert "payments" in response.context

    def test_empty_history_shows_message(self, logged_client, client):
        response = logged_client.get(f"/payments/client/{client.id}/")
        assert response.status_code == 200

    def test_client_filter_in_list(self, logged_client, payment_data, client):
        Payment.objects.create(**payment_data)
        response = logged_client.get(f"/payments/?client={client.id}")
        assert response.status_code == 200


# ── T038-T042: US3 — Payment-Reservation Association ─────────────────────────


@pytest.mark.django_db
class TestPaymentReservation:
    def test_payment_detail_shows_associated_reservations(self, logged_client, payment_data):
        payment = Payment.objects.create(**payment_data)
        response = logged_client.get(f"/payments/{payment.pk}/")
        assert response.status_code == 200


# ── T080-T081: US1 — Form widget styling and layout ────────────────────────────


@pytest.mark.django_db
class TestPaymentFormStyling:
    """TDD tests for FR-001 and FR-003 — written before implementation."""

    def test_all_widgets_have_form_control(self):
        """FR-003: Every widget in Meta.widgets must have form-control class."""
        for field_name, widget in PaymentForm.Meta.widgets.items():
            assert "class" in widget.attrs, (
                f"{field_name} widget missing 'class' attr"
            )
            assert "form-control" in widget.attrs["class"], (
                f"{field_name} widget missing 'form-control'"
            )

    def test_create_page_renders_col_md_6(self, logged_client):
        """FR-001: Payment create page renders fields with col-md-6."""
        response = logged_client.get("/payments/create/")
        assert response.status_code == 200
        html = response.content.decode()
        assert "col-md-6" in html, "Expected col-md-6 in rendered form fields"
        # The button row still uses col-12, but field wrappers should not
        field_wrappers = [line for line in html.split("\n") if 'class="col-12"' in line]
        # Only the button row (1 instance) should remain
        assert len(field_wrappers) == 1, (
            f"Expected exactly 1 col-12 (button row), found {len(field_wrappers)}"
        )


# ── T004-T006: US1 — Reports Menu (superuser visibility) ────────────────────


@pytest.mark.django_db
class TestReportsMenuSuperuser:
    """TDD tests — must fail before Reports dropdown is implemented."""

    def test_superuser_sees_reports_link(self, http_client):
        admin = User.objects.create_superuser(username="admin", password="pass")
        http_client.force_login(admin)
        response = http_client.get("/reservations/")
        assert response.status_code == 200
        assert "Reportes" in response.content.decode()

    def test_superuser_sees_reports_payments_dropdown(self, http_client):
        admin = User.objects.create_superuser(username="admin2", password="pass")
        http_client.force_login(admin)
        response = http_client.get("/reservations/")
        assert response.status_code == 200
        html = response.content.decode()
        assert "Reportes" in html
        assert "dropdown-item" in html
        assert "/payments/reports/" in html

    def test_reports_payments_link_navigates_correctly(self, http_client):
        admin = User.objects.create_superuser(username="admin3", password="pass")
        http_client.force_login(admin)
        response = http_client.get("/payments/reports/")
        assert response.status_code == 200


# ── T010-T012: US2 — Reports Menu (non-superuser hidden) ────────────────────


@pytest.mark.django_db
class TestReportsMenuNonSuperuser:
    """TDD tests — must fail once US1 passes, guard still needed."""

    def test_non_superuser_does_not_see_reports(self, http_client, staff_user):
        http_client.force_login(staff_user)
        response = http_client.get("/reservations/")
        assert response.status_code == 200
        assert "Reportes" not in response.content.decode()

    def test_non_superuser_does_not_see_payments_dropdown(self, http_client, staff_user):
        http_client.force_login(staff_user)
        response = http_client.get("/reservations/")
        assert response.status_code == 200
        assert "dropdown-toggle" not in response.content.decode()

    def test_non_superuser_blocked_from_reports_page(self, http_client, staff_user):
        http_client.force_login(staff_user)
        response = http_client.get("/payments/reports/")
        assert response.status_code == 403


# ── T050-T052: US4 — Payment Reports ─────────────────────────────────────────


@pytest.mark.django_db
class TestPaymentReports:
    def test_operator_denied(self, http_client, staff_user):
        http_client.force_login(staff_user)
        response = http_client.get("/payments/reports/")
        assert response.status_code == 403

    def test_superuser_allowed(self, http_client, payment_data):
        admin = User.objects.create_superuser(username="admin", password="pass")
        http_client.force_login(admin)
        Payment.objects.create(**{**payment_data, "created_by": admin})
        response = http_client.get("/payments/reports/?grouping=month")
        assert response.status_code == 200

    def test_reports_with_date_range(self, http_client, payment_data):
        admin = User.objects.create_superuser(username="admin2", password="pass")
        http_client.force_login(admin)
        Payment.objects.create(**{**payment_data, "created_by": admin})
        response = http_client.get("/payments/reports/?grouping=day&start=2026-01-01&end=2026-12-31")
        assert response.status_code == 200

    def test_reports_day_grouping_with_date_range(self, http_client, client, staff_user):
        admin = User.objects.create_superuser(username="admin3", password="pass")
        http_client.force_login(admin)
        Payment.objects.create(
            client=client, amount=150.00, payment_type="CASH",
            date=datetime.date(2026, 6, 24), class_slot_count=2,
            reference="REF-DAY", created_by=staff_user,
        )
        response = http_client.get(
            "/payments/reports/?grouping=day&start=2026-06-20&end=2026-06-30",
        )
        assert response.status_code == 200
        html = response.content.decode()
        assert "report-data" in html
        import re
        match = re.search(
            r'<script id="report-data"[^>]*>(.*?)</script>', html, re.DOTALL,
        )
        assert match is not None, "report-data script tag not found"
        report_data = json.loads(match.group(1))
        assert isinstance(report_data, list), (
            f"Expected report_data to be a list, got {type(report_data)}: {report_data!r}"
        )
        assert len(report_data) > 0, (
            "Expected report_data to contain payment data, got empty list"
        )
        assert any(
            row["payment_type"] == "CASH" and float(row["total"]) == 150.0
            for row in report_data
        ), f"No CASH payment with total 150.0 found in {report_data}"

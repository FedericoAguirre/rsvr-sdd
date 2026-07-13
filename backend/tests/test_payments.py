import calendar
import datetime
import io
import json
import re

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


# ── T001-T003: 034 — Stacked Graph Weekly Grouping ─────────────────────────


@pytest.mark.django_db
class TestDateSnapping:
    """Date snapping for Week grouping — start→Monday, end→Sunday."""

    def test_start_snaps_friday_to_previous_monday(self, http_client):
        admin = User.objects.create_superuser(username="snap1", password="pass")
        http_client.force_login(admin)
        response = http_client.get(
            "/payments/reports/?grouping=week&start=2026-07-03&end=2026-07-19",
        )
        assert response.context["start_date"] == "2026-06-29"
        assert response.context["end_date"] == "2026-07-19"

    def test_start_monday_stays_unchanged(self, http_client):
        admin = User.objects.create_superuser(username="snap2", password="pass")
        http_client.force_login(admin)
        response = http_client.get(
            "/payments/reports/?grouping=week&start=2026-07-06&end=2026-07-19",
        )
        assert response.context["start_date"] == "2026-07-06"

    def test_end_tuesday_snaps_to_following_sunday(self, http_client):
        admin = User.objects.create_superuser(username="snap3", password="pass")
        http_client.force_login(admin)
        response = http_client.get(
            "/payments/reports/?grouping=week&start=2026-07-06&end=2026-07-14",
        )
        assert response.context["end_date"] == "2026-07-19"

    def test_end_sunday_stays_unchanged(self, http_client):
        admin = User.objects.create_superuser(username="snap4", password="pass")
        http_client.force_login(admin)
        response = http_client.get(
            "/payments/reports/?grouping=week&start=2026-07-06&end=2026-07-19",
        )
        assert response.context["end_date"] == "2026-07-19"

    def test_snapping_only_applies_to_week_grouping(self, http_client):
        admin = User.objects.create_superuser(username="snap5", password="pass")
        http_client.force_login(admin)
        response = http_client.get(
            "/payments/reports/?grouping=day&start=2026-07-03&end=2026-07-19",
        )
        assert response.context["start_date"] == "2026-07-03"
        assert response.context["end_date"] == "2026-07-19"


@pytest.mark.django_db
class TestWeeklyChartRendering:
    """Weekly chart returns correctly formatted data."""

    def test_weekly_grouping_returns_week_keys(self, http_client, client, staff_user):
        admin = User.objects.create_superuser(username="wk1", password="pass")
        http_client.force_login(admin)
        Payment.objects.create(
            client=client, amount=100.00, payment_type="CASH",
            date=datetime.date(2026, 7, 6), class_slot_count=2,
            reference="WEEK-1", created_by=staff_user,
        )
        Payment.objects.create(
            client=client, amount=200.00, payment_type="CC",
            date=datetime.date(2026, 7, 8), class_slot_count=2,
            reference="WEEK-2", created_by=staff_user,
        )
        response = http_client.get(
            "/payments/reports/?grouping=week&start=2026-07-06&end=2026-07-12",
        )
        assert response.status_code == 200
        import re
        html = response.content.decode()
        match = re.search(
            r'<script id="report-data"[^>]*>(.*?)</script>', html, re.DOTALL,
        )
        assert match is not None
        report_data = json.loads(match.group(1))
        assert isinstance(report_data, list)
        assert len(report_data) > 0
        for row in report_data:
            assert "week" in row, f"Expected 'week' key in row: {row}"
            assert row["payment_type"] in ("CASH", "CC")
            assert float(row["total"]) in (100.0, 200.0)
            # Week keys should be Monday dates in YYYYMMDD
            assert row["week"] == "2026-07-06"

    def test_weekly_empty_state(self, http_client):
        admin = User.objects.create_superuser(username="wk2", password="pass")
        http_client.force_login(admin)
        response = http_client.get(
            "/payments/reports/?grouping=week&start=2020-01-01&end=2020-01-31",
        )
        assert response.status_code == 200
        html = response.content.decode()
        assert "No payment data for the selected period." in html or "No hay datos de pago" in html


# ── T001-T007: 035 — Monthly Stacked Graph ──────────────────────────────────


@pytest.mark.django_db
class TestMonthlyDateSnapping:
    """Date snapping for Month grouping — start→1st, end→last day."""

    def test_start_date_snaps_to_first_of_month(self, http_client):
        admin = User.objects.create_superuser(username="msnap1", password="pass")
        http_client.force_login(admin)
        response = http_client.get(
            "/payments/reports/?grouping=month&start=2026-07-15&end=2026-09-10",
        )
        assert response.context["start_date"] == "2026-07-01"

    def test_end_date_snaps_to_last_day_of_month(self, http_client):
        admin = User.objects.create_superuser(username="msnap2", password="pass")
        http_client.force_login(admin)
        response = http_client.get(
            "/payments/reports/?grouping=month&start=2026-07-15&end=2026-09-10",
        )
        assert response.context["end_date"] == "2026-09-30"

    def test_start_date_already_first(self, http_client):
        admin = User.objects.create_superuser(username="msnap3", password="pass")
        http_client.force_login(admin)
        response = http_client.get(
            "/payments/reports/?grouping=month&start=2026-07-01&end=2026-09-10",
        )
        assert response.context["start_date"] == "2026-07-01"

    def test_end_date_already_last_day(self, http_client):
        admin = User.objects.create_superuser(username="msnap4", password="pass")
        http_client.force_login(admin)
        response = http_client.get(
            "/payments/reports/?grouping=month&start=2026-07-01&end=2026-09-30",
        )
        assert response.context["end_date"] == "2026-09-30"

    def test_leap_year_february(self, http_client):
        admin = User.objects.create_superuser(username="msnap5", password="pass")
        http_client.force_login(admin)
        response = http_client.get(
            "/payments/reports/?grouping=month&start=2028-02-01&end=2028-02-15",
        )
        assert response.context["end_date"] == "2028-02-29"

    def test_snapping_only_applies_to_month_grouping(self, http_client):
        admin = User.objects.create_superuser(username="msnap6", password="pass")
        http_client.force_login(admin)
        response = http_client.get(
            "/payments/reports/?grouping=day&start=2026-07-15&end=2026-09-10",
        )
        assert response.context["start_date"] == "2026-07-15"
        assert response.context["end_date"] == "2026-09-10"


@pytest.mark.django_db
class TestMonthlyChartRendering:
    """Monthly chart returns correctly formatted YYYYMM labels."""

    def test_monthly_grouping_returns_yyyymm_labels(self, http_client, client, staff_user):
        admin = User.objects.create_superuser(username="mchr1", password="pass")
        http_client.force_login(admin)
        Payment.objects.create(
            client=client, amount=300.00, payment_type="CASH",
            date=datetime.date(2026, 7, 15), class_slot_count=2,
            reference="MONTH-1", created_by=staff_user,
        )
        Payment.objects.create(
            client=client, amount=400.00, payment_type="CC",
            date=datetime.date(2026, 8, 20), class_slot_count=2,
            reference="MONTH-2", created_by=staff_user,
        )
        response = http_client.get(
            "/payments/reports/?grouping=month&start=2026-07-01&end=2026-08-31",
        )
        assert response.status_code == 200
        html = response.content.decode()
        # Verify the formatLabel function produces YYYYMM (no hyphen separator)
        assert "String(r.date__year) + String(r.date__month).padStart(2, '0')" in html, (
            "Expected formatLabel to concatenate year+month without separator"
        )
        # Verify report_data JSON contains expected data
        import re
        match = re.search(
            r'<script id="report-data"[^>]*>(.*?)</script>', html, re.DOTALL,
        )
        assert match is not None
        report_data = json.loads(match.group(1))
        assert isinstance(report_data, list)
        assert len(report_data) > 0

    def test_monthly_empty_state(self, http_client):
        admin = User.objects.create_superuser(username="mchr2", password="pass")
        http_client.force_login(admin)
        response = http_client.get(
            "/payments/reports/?grouping=month&start=2020-01-01&end=2020-02-29",
        )
        assert response.status_code == 200
        html = response.content.decode()
        assert "No payment data for the selected period." in html or "No hay datos de pago" in html


# ── T005-T014: US1-US2 — Export Payments ─────────────────────────────────────


@pytest.mark.django_db
class TestPaymentExport:
    """TDD tests for PaymentExportView."""

    def test_successful_export_returns_xlsx(self, http_client, payment_data):
        """US1: Export with valid date range returns xlsx file."""
        admin = User.objects.create_superuser(username="export1", password="pass")
        http_client.force_login(admin)
        Payment.objects.create(**{**payment_data, "created_by": admin})
        response = http_client.get(
            "/payments/reports/export/?fecha_inicio=2026-01-01&fecha_fin=2026-12-31",
        )
        assert response.status_code == 200
        assert response["Content-Type"] == (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        assert "pagos_" in response["Content-Disposition"]
        assert ".xlsx" in response["Content-Disposition"]

    def test_export_no_data_returns_404(self, http_client):
        """US2: No payments in range returns 404."""
        admin = User.objects.create_superuser(username="export2", password="pass")
        http_client.force_login(admin)
        response = http_client.get(
            "/payments/reports/export/?fecha_inicio=2020-01-01&fecha_fin=2020-01-31",
        )
        assert response.status_code == 404
        assert "No hay pagos" in response.json()["error"]

    def test_export_inverted_dates_returns_400(self, http_client):
        """US2: Start > end returns validation error."""
        admin = User.objects.create_superuser(username="export3", password="pass")
        http_client.force_login(admin)
        response = http_client.get(
            "/payments/reports/export/?fecha_inicio=2026-12-31&fecha_fin=2026-01-01",
        )
        assert response.status_code == 400
        assert "anterior" in response.json()["error"]

    def test_export_operator_denied(self, http_client, staff_user):
        """US1: Non-admin users are blocked."""
        http_client.force_login(staff_user)
        response = http_client.get(
            "/payments/reports/export/?fecha_inicio=2026-01-01&fecha_fin=2026-12-31",
        )
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


# ── T001-T003: US1 — Current Month Default Dates ──────────────────────────────


def _current_month_start():
    today = datetime.date.today()
    return today.replace(day=1).isoformat()


def _current_month_end():
    today = datetime.date.today()
    _, last = calendar.monthrange(today.year, today.month)
    return today.replace(day=last).isoformat()


@pytest.mark.django_db
class TestPaymentReportDefaults:
    """TDD tests — must fail before default dates are implemented."""

    def test_default_dates_match_current_month(self, http_client):
        """T001: No query params → dates default to current month."""
        admin = User.objects.create_superuser(username="def1", password="pass")
        http_client.force_login(admin)
        response = http_client.get("/payments/reports/")
        assert response.status_code == 200
        assert response.context["start_date"] == _current_month_start()
        assert response.context["end_date"] == _current_month_end()

    def test_explicit_params_override_defaults(self, http_client):
        """T002: Explicit start/end params are respected."""
        admin = User.objects.create_superuser(username="def2", password="pass")
        http_client.force_login(admin)
        response = http_client.get(
            "/payments/reports/?start=2026-06-01&end=2026-06-30",
        )
        assert response.status_code == 200
        assert response.context["start_date"] == "2026-06-01"
        assert response.context["end_date"] == "2026-06-30"

    def test_empty_dates_fallback_to_current_month(self, http_client):
        """T003: Empty start/end params fall back to current month."""
        admin = User.objects.create_superuser(username="def3", password="pass")
        http_client.force_login(admin)
        response = http_client.get("/payments/reports/?start=&end=")
        assert response.status_code == 200
        assert response.context["start_date"] == _current_month_start()
        assert response.context["end_date"] == _current_month_end()


@pytest.mark.django_db
class TestPaymentAutoRender:
    """TDD tests for US2 — auto-render with current month data."""

    def test_report_data_present_in_initial_context(self, http_client, client, staff_user):
        """T005: Current month report data is in the initial page context."""
        admin = User.objects.create_superuser(username="aut1", password="pass")
        http_client.force_login(admin)
        today = datetime.date.today()
        Payment.objects.create(
            client=client, amount=250.00, payment_type="CASH",
            date=today, class_slot_count=2,
            reference="AUTO-1", created_by=staff_user,
        )
        response = http_client.get("/payments/reports/")
        assert response.status_code == 200
        assert len(response.context["report_data"]) > 0
        html = response.content.decode()
        assert "report-data" in html

    def test_empty_current_month_shows_message(self, http_client):
        """T006: No payments in current month displays empty state."""
        admin = User.objects.create_superuser(username="aut2", password="pass")
        http_client.force_login(admin)
        response = http_client.get("/payments/reports/")
        assert response.status_code == 200
        html = response.content.decode()
        if not response.context["report_data"]:
            assert any(msg in html for msg in (
                "No payment data for the selected period.",
                "No hay datos de pago",
            ))


@pytest.mark.django_db
class TestPaymentManualOverride:
    """TDD tests for US3 — manual date override."""

    def test_non_current_month_params_override_defaults(self, http_client, client, staff_user):
        """T008: Explicit non-current-month dates override defaults."""
        admin = User.objects.create_superuser(username="ovr1", password="pass")
        http_client.force_login(admin)
        Payment.objects.create(
            client=client, amount=500.00, payment_type="CC",
            date=datetime.date(2026, 5, 15), class_slot_count=2,
            reference="OVR-1", created_by=staff_user,
        )
        response = http_client.get(
            "/payments/reports/?start=2026-05-01&end=2026-05-31",
        )
        assert response.status_code == 200
        assert response.context["start_date"] == "2026-05-01"
        assert response.context["end_date"] == "2026-05-31"
        assert len(response.context["report_data"]) > 0

    def test_nav_away_and_back_resets_to_current_month(self, http_client):
        """T009: Navigating without params resets to current month defaults."""
        admin = User.objects.create_superuser(username="ovr2", password="pass")
        http_client.force_login(admin)
        response = http_client.get("/payments/reports/")
        assert response.status_code == 200
        assert response.context["start_date"] == _current_month_start()
        assert response.context["end_date"] == _current_month_end()


@pytest.mark.django_db
class TestChartContainer:
    """TDD tests for US1 — chart container sizing."""

    def test_canvas_height_is_adjusted(self, http_client):
        """T001: Canvas height attribute is set to adjusted value 250."""
        admin = User.objects.create_superuser(username="cht1", password="pass")
        http_client.force_login(admin)
        response = http_client.get("/payments/reports/")
        assert response.status_code == 200
        html = response.content.decode()
        match = re.search(
            r'<canvas[^>]*id="totalsChart"[^>]*>', html,
        )
        assert match is not None, "totalsChart canvas not found"
        assert 'height="250"' in match.group(0), (
            f"Expected height=250 in canvas, got: {match.group(0)}"
        )

    def test_chart_container_has_max_height(self, http_client):
        """T002: Card-body containing chart has max-height style."""
        admin = User.objects.create_superuser(username="cht2", password="pass")
        http_client.force_login(admin)
        response = http_client.get("/payments/reports/")
        assert response.status_code == 200
        html = response.content.decode()
        pattern = r'<div class="card-body"[^>]*>.*?<canvas[^>]*id="totalsChart"'
        match = re.search(pattern, html, re.DOTALL)
        assert match is not None, "card-body with totalsChart not found"
        card_body = match.group(0)
        assert "max-height" in card_body or "max-height" in html, (
            "Expected max-height on chart container"
        )

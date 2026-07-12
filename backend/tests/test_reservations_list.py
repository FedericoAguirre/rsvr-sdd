import datetime
import io
import json

import pytest
from django.contrib.auth.models import User
from django.test import Client as HttpClient
from pdfminer.high_level import extract_text

from apps.classes.models import ClassSlot
from apps.clients.models import Client
from apps.equipment.models import Equipment
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
class TestReservationsListPDF:

    def _expected_filename(self, class_slot, date_str):
        safe = str(class_slot).replace(" ", "_").translate(
            str.maketrans("", "", "/" + chr(0) + '<>:"|?*')
        )
        date_compact = date_str.replace("-", "")
        return f"reservations_{safe}_{date_compact}.pdf"

    def test_pdf_download_content_type(self, logged_client, class_slot, reservations_for_slot):
        response = logged_client.get(
            f"/reservations/pdf/?class_slot={class_slot.pk}&date=2026-06-15"
        )
        assert response.status_code == 200
        assert response["Content-Type"] == "application/pdf"
        expected = self._expected_filename(class_slot, "2026-06-15")
        assert response["Content-Disposition"] == f'attachment; filename="{expected}"'

    def test_pdf_empty_list(self, logged_client, class_slot):
        response = logged_client.get(
            f"/reservations/pdf/?class_slot={class_slot.pk}&date=2026-06-15"
        )
        assert response.status_code == 200
        assert response["Content-Type"] == "application/pdf"
        expected = self._expected_filename(class_slot, "2026-06-15")
        assert response["Content-Disposition"] == f'attachment; filename="{expected}"'

    def test_filename_with_missing_date_uses_no_date_fallback(self, logged_client, class_slot):
        response = logged_client.get(
            f"/reservations/pdf/?class_slot={class_slot.pk}&date="
        )
        assert response.status_code == 200
        assert "no_date" in response["Content-Disposition"]

    def test_pdf_filename_with_missing_class_slot_fallback(self, logged_client):
        response = logged_client.get(
            "/reservations/pdf/?date=2026-06-15"
        )
        assert response.status_code == 200
        safe = "unknown"
        assert safe in response["Content-Disposition"]

    def test_export_button_visible_on_main_page(self, logged_client, class_slot, reservations_for_slot):
        response = logged_client.get(
            f"/reservations/?class_slot={class_slot.pk}&date=2026-06-15"
        )
        content = response.content.decode()
        assert "/reservations/pdf/" in content

    def test_pdf_content_contains_reservation_data(self, logged_client, class_slot, reservations_for_slot):
        response = logged_client.get(
            f"/reservations/pdf/?class_slot={class_slot.pk}&date=2026-06-15"
        )
        assert response.status_code == 200
        text = extract_text(io.BytesIO(response.content))
        assert "Treadmill" in text
        assert "Alice" in text
        assert str(class_slot) in text

    def test_pdf_empty_state_shows_no_reservations_message(self, logged_client, class_slot):
        response = logged_client.get(
            f"/reservations/pdf/?class_slot={class_slot.pk}&date=2026-06-15"
        )
        assert response.status_code == 200
        text = extract_text(io.BytesIO(response.content))
        assert "No se encontraron reservaciones" in text


@pytest.mark.django_db
class TestMainPageWithSlotFilter:

    def test_class_slot_and_date_filter_shows_equipment_client_pairs(
        self, logged_client, class_slot, reservations_for_slot
    ):
        response = logged_client.get(
            f"/reservations/?class_slot={class_slot.pk}&date=2026-06-15"
        )
        content = response.content.decode()
        assert "Treadmill" in content
        assert "Alice" in content
        assert str(class_slot) in content
        assert "2026-06-15" in content

    def test_new_reservation_button_visible_with_filter(
        self, logged_client, class_slot, reservations_for_slot
    ):
        response = logged_client.get(
            f"/reservations/?class_slot={class_slot.pk}&date=2026-06-15"
        )
        content = response.content.decode()
        assert "/reservations/create/" in content

    def test_main_page_shows_class_slot_dropdown(
        self, logged_client, class_slot
    ):
        response = logged_client.get("/reservations/")
        content = response.content.decode()
        assert "class_slot" in content
        assert str(class_slot) in content

    def test_main_page_empty_state_when_no_reservations(
        self, logged_client, class_slot
    ):
        response = logged_client.get(
            f"/reservations/?class_slot={class_slot.pk}&date=2026-06-15"
        )
        content = response.content.decode()
        assert "No se encontraron reservaciones" in content


@pytest.mark.django_db
class TestReservationStatusChange:

    def test_change_status_to_used(self, logged_client, reservations_for_slot):
        reservation = Reservation.objects.first()
        response = logged_client.post(
            f"/reservations/{reservation.pk}/status/", {"status": "used"}
        )
        assert response.status_code == 302
        reservation.refresh_from_db()
        assert reservation.status == "used"

    def test_change_status_to_unused(self, logged_client, reservations_for_slot):
        reservation = Reservation.objects.first()
        response = logged_client.post(
            f"/reservations/{reservation.pk}/status/", {"status": "unused"}
        )
        assert response.status_code == 302
        reservation.refresh_from_db()
        assert reservation.status == "unused"

    def test_change_status_back_to_reserved(self, logged_client, reservations_for_slot):
        reservation = Reservation.objects.first()
        reservation.status = "used"
        reservation.save()
        response = logged_client.post(
            f"/reservations/{reservation.pk}/status/", {"status": "reserved"}
        )
        assert response.status_code == 302
        reservation.refresh_from_db()
        assert reservation.status == "reserved"

    def test_re_set_same_status(self, logged_client, reservations_for_slot):
        reservation = Reservation.objects.first()
        reservation.status = "used"
        reservation.save()
        response = logged_client.post(
            f"/reservations/{reservation.pk}/status/", {"status": "used"}
        )
        assert response.status_code == 302
        reservation.refresh_from_db()
        assert reservation.status == "used"

    def test_invalid_status_value(self, logged_client, reservations_for_slot):
        reservation = Reservation.objects.first()
        response = logged_client.post(
            f"/reservations/{reservation.pk}/status/", {"status": "invalid"}
        )
        assert response.status_code == 302
        reservation.refresh_from_db()
        assert reservation.status == "reserved"

    def test_unauthenticated_user_redirected(self, http_client, reservations_for_slot):
        reservation = Reservation.objects.first()
        response = http_client.post(
            f"/reservations/{reservation.pk}/status/", {"status": "used"}
        )
        assert response.status_code == 302
        assert "/accounts/login/" in response.url


@pytest.mark.django_db
class TestHTMXStatusChange:

    def test_htmx_request_returns_row_partial(self, logged_client, reservations_for_slot):
        reservation = Reservation.objects.first()
        response = logged_client.post(
            f"/reservations/{reservation.pk}/status/",
            {"status": "used"},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 200
        content = response.content.decode()
        assert f'id="row-{reservation.pk}"' in content
        assert "bg-primary" in content

    def test_non_htmx_request_still_redirects(self, logged_client, reservations_for_slot):
        reservation = Reservation.objects.first()
        response = logged_client.post(
            f"/reservations/{reservation.pk}/status/", {"status": "used"}
        )
        assert response.status_code == 302
        assert f"/reservations/{reservation.pk}/" in response.url

    def test_htmx_invalid_status_returns_400(self, logged_client, reservations_for_slot):
        reservation = Reservation.objects.first()
        response = logged_client.post(
            f"/reservations/{reservation.pk}/status/",
            {"status": "invalid"},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 400

    def test_htmx_unauthenticated_redirects(self, http_client, reservations_for_slot):
        reservation = Reservation.objects.first()
        response = http_client.post(
            f"/reservations/{reservation.pk}/status/",
            {"status": "used"},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_htmx_reserved_to_used_updates_badge(self, logged_client, reservations_for_slot):
        reservation = Reservation.objects.first()
        assert reservation.status == "reserved"
        response = logged_client.post(
            f"/reservations/{reservation.pk}/status/",
            {"status": "used"},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 200
        content = response.content.decode()
        assert "bg-primary" in content
        reservation.refresh_from_db()
        assert reservation.status == "used"

    def test_htmx_used_to_unused_updates_badge(self, logged_client, reservations_for_slot):
        reservation = Reservation.objects.first()
        reservation.status = "used"
        reservation.save()
        response = logged_client.post(
            f"/reservations/{reservation.pk}/status/",
            {"status": "unused"},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 200
        content = response.content.decode()
        assert "bg-secondary" in content
        reservation.refresh_from_db()
        assert reservation.status == "unused"

    def test_htmx_response_has_status_changed_trigger(self, logged_client, reservations_for_slot):
        reservation = Reservation.objects.first()
        response = logged_client.post(
            f"/reservations/{reservation.pk}/status/",
            {"status": "used"},
            HTTP_HX_REQUEST="true",
        )
        assert response.headers.get("HX-Trigger") == "statusChanged"

    def test_htmx_same_status_noop(self, logged_client, reservations_for_slot):
        reservation = Reservation.objects.first()
        reservation.status = "used"
        reservation.save()
        response = logged_client.post(
            f"/reservations/{reservation.pk}/status/",
            {"status": "used"},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 200
        reservation.refresh_from_db()
        assert reservation.status == "used"

    def test_htmx_json_body_updates_status(self, logged_client, reservations_for_slot):
        reservation = Reservation.objects.first()
        assert reservation.status == "reserved"
        response = logged_client.post(
            f"/reservations/{reservation.pk}/status/",
            json.dumps({"status": "used"}),
            content_type="application/json",
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 200
        content = response.content.decode()
        assert "bg-primary" in content
        reservation.refresh_from_db()
        assert reservation.status == "used"


@pytest.mark.django_db
class TestReservationStatusFilter:

    def test_filter_by_status_shows_only_matching(self, logged_client, class_slot, reservations_for_slot):
        reservation = Reservation.objects.first()
        reservation.status = "used"
        reservation.save()
        response = logged_client.get(
            f"/reservations/?class_slot={class_slot.pk}&date=2026-06-15&status=used"
        )
        content = response.content.decode()
        assert "Usado" in content


@pytest.mark.django_db
class TestReservationStatusInPDF:

    def test_status_in_pdf_export(self, logged_client, class_slot, reservations_for_slot):
        reservation = Reservation.objects.first()
        reservation.status = "used"
        reservation.save()
        response = logged_client.get(
            f"/reservations/pdf/?class_slot={class_slot.pk}&date=2026-06-15"
        )
        assert response.status_code == 200
        text = extract_text(io.BytesIO(response.content))
        assert "Usado" in text


@pytest.mark.django_db
class TestStatusBadgeRendering:

    def test_status_badge_class_filter(self, db):
        from apps.reservations.templatetags.reservation_extras import status_badge_class
        assert "bg-success" in status_badge_class("reserved")
        assert "bg-primary" in status_badge_class("used")
        assert "bg-secondary" in status_badge_class("unused")

    def test_badge_appears_in_list_view_per_status(self, logged_client, class_slot, equipment_list, client_list, staff_user):
        date = "2026-06-15"
        statuses = ["reserved", "used", "unused"]
        for i, status in enumerate(statuses):
            Reservation.objects.create(
                client=client_list[i],
                equipment=equipment_list[i],
                class_slot=class_slot,
                date=date,
                status=status,
                created_by=staff_user,
            )
        response = logged_client.get(
            f"/reservations/?class_slot={class_slot.pk}&date=2026-06-15"
        )
        content = response.content.decode()
        assert 'bg-success' in content
        assert 'bg-primary' in content
        assert 'bg-secondary' in content


@pytest.mark.django_db
class TestFilterStatePreservation:

    def test_class_slot_has_selected_attribute_after_filter(
        self, logged_client, class_slot, reservations_for_slot
    ):
        response = logged_client.get(
            f"/reservations/?class_slot={class_slot.pk}&date=2026-06-15&status=used"
        )
        content = response.content.decode()
        assert f'value="{class_slot.pk}" selected' in content

    def test_date_input_preserves_value_after_filter(
        self, logged_client, class_slot, reservations_for_slot
    ):
        response = logged_client.get(
            f"/reservations/?class_slot={class_slot.pk}&date=2026-06-15"
        )
        content = response.content.decode()
        assert 'value="2026-06-15"' in content

    def test_status_dropdown_has_selected_attribute_after_filter(
        self, logged_client, class_slot, reservations_for_slot
    ):
        response = logged_client.get(
            f"/reservations/?class_slot={class_slot.pk}&date=2026-06-15&status=used"
        )
        content = response.content.decode()
        assert 'value="used" selected' in content

    def test_clear_filters_removes_class_slot_selected(
        self, logged_client, class_slot, reservations_for_slot
    ):
        response = logged_client.get("/reservations/")
        content = response.content.decode()
        assert 'selected' not in content.split('<select name="class_slot"')[1].split('</select>')[0]

    def test_clear_filters_resets_status_to_all(
        self, logged_client, class_slot, reservations_for_slot
    ):
        response = logged_client.get("/reservations/")
        content = response.content.decode()
        status_section = content.split('<select name="status"')[1].split('</select>')[0]
        assert 'selected' not in status_section

    def test_clear_filters_button_exists(
        self, logged_client, class_slot
    ):
        response = logged_client.get("/reservations/")
        content = response.content.decode()
        assert "Clear Filters" in content
        assert "/reservations/" in content

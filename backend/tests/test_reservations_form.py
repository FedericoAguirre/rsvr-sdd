import datetime

import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import Client as HttpClient

from apps.classes.models import ClassSlot
from apps.clients.models import Client
from apps.equipment.models import Equipment
from apps.reservations.forms import ReservationForm
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
def equipment_item(db):
    return Equipment.objects.create(name="Treadmill", equipment_type="treadmill")


@pytest.fixture
def client_item(db):
    return Client.objects.create(first_name="Alice", last_name="A")


@pytest.fixture
def existing_reservation(db, class_slot, equipment_item, client_item, staff_user):
    return Reservation.objects.create(
        client=client_item,
        equipment=equipment_item,
        class_slot=class_slot,
        date="2026-07-01",
        status="reserved",
        created_by=staff_user,
    )


@pytest.mark.django_db
class TestReservationFormDuplicateDetection:
    def test_clean_raises_error_for_duplicate(self, existing_reservation, class_slot, equipment_item, client_item):
        form = ReservationForm(
            data={
                "client": client_item.pk,
                "equipment": equipment_item.pk,
                "class_slot": class_slot.pk,
                "date": "2026-07-01",
                "notes": "",
            }
        )
        assert not form.is_valid()
        error_text = str(form.errors)
        has_en = "UNAVAILABLE" in error_text
        has_es = "NO DISPONIBLE" in error_text
        assert has_en or has_es, f"Expected UNAVAILABLE or NO DISPONIBLE in {error_text}"

    def test_clean_passes_for_unique_combination(self, existing_reservation, class_slot, equipment_item, client_item):
        form = ReservationForm(
            data={
                "client": client_item.pk,
                "equipment": equipment_item.pk,
                "class_slot": class_slot.pk,
                "date": "2026-07-02",
                "notes": "",
            }
        )
        assert form.is_valid()

    def test_clean_does_not_add_custom_error_for_non_reserved_status(self, existing_reservation, class_slot, equipment_item, client_item, staff_user):
        existing_reservation.status = "used"
        existing_reservation.save()
        form = ReservationForm(
            data={
                "client": client_item.pk,
                "equipment": equipment_item.pk,
                "class_slot": class_slot.pk,
                "date": "2026-07-01",
                "notes": "",
            }
        )
        form.is_valid()
        non_field = str(form.non_field_errors())
        assert "UNAVAILABLE" not in non_field

    def test_alert_includes_equipment_date_and_class_slot(self, existing_reservation, class_slot, equipment_item, client_item):
        form = ReservationForm(
            data={
                "client": client_item.pk,
                "equipment": equipment_item.pk,
                "class_slot": class_slot.pk,
                "date": "2026-07-01",
                "notes": "",
            }
        )
        assert not form.is_valid()
        error_text = str(form.errors)
        assert "Treadmill" in error_text
        assert "2026-07-01" in error_text
        assert str(class_slot) in error_text

    def test_alert_contains_aria_role(self, existing_reservation, class_slot, equipment_item, client_item):
        form = ReservationForm(
            data={
                "client": client_item.pk,
                "equipment": equipment_item.pk,
                "class_slot": class_slot.pk,
                "date": "2026-07-01",
                "notes": "",
            }
        )
        form.is_valid()
        from django.template import Template, Context
        template = Template(
            "{% if form.non_field_errors %}"
            '<div class="alert alert-warning alert-dismissible fade show" role="alert" aria-live="assertive">'
            "{% for error in form.non_field_errors %}"
            '<p class="mb-0">{{ error }}</p>'
            "{% endfor %}"
            '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
            "</div>"
            "{% endif %}"
        )
        rendered = template.render(Context({"form": form}))
        assert 'role="alert"' in rendered

    def test_multi_equipment_validation(self, class_slot, equipment_item, client_item, staff_user):
        bike = Equipment.objects.create(name="Bike", equipment_type="bike")
        Reservation.objects.create(
            client=client_item,
            equipment=bike,
            class_slot=class_slot,
            date="2026-07-01",
            status="reserved",
            created_by=staff_user,
        )
        form = ReservationForm(
            data={
                "client": client_item.pk,
                "equipment": bike.pk,
                "class_slot": class_slot.pk,
                "date": "2026-07-01",
                "notes": "",
            }
        )
        assert not form.is_valid()


@pytest.mark.django_db
class TestReservationAlertIntegration:
    def test_duplicate_alert_shown_on_form_submit(self, logged_client, existing_reservation, class_slot, equipment_item, client_item):
        response = logged_client.post(
            "/reservations/create/",
            {
                "client": client_item.pk,
                "equipment": equipment_item.pk,
                "class_slot": class_slot.pk,
                "date": "2026-07-01",
                "notes": "",
            },
        )
        assert response.status_code == 200
        content = response.content.decode()
        assert "NO DISPONIBLE" in content or "UNAVAILABLE" in content

    def test_unique_reservation_submits_successfully(self, logged_client, class_slot, equipment_item, client_item):
        response = logged_client.post(
            "/reservations/create/",
            {
                "client": client_item.pk,
                "equipment": equipment_item.pk,
                "class_slot": class_slot.pk,
                "date": "2026-07-02",
                "notes": "",
            },
        )
        assert response.status_code == 302

    def test_alert_has_warning_css_class(self, logged_client, existing_reservation, class_slot, equipment_item, client_item):
        response = logged_client.post(
            "/reservations/create/",
            {
                "client": client_item.pk,
                "equipment": equipment_item.pk,
                "class_slot": class_slot.pk,
                "date": "2026-07-01",
                "notes": "",
            },
        )
        content = response.content.decode()
        assert 'class="alert alert-warning alert-dismissible fade show"' in content

    def test_spanish_locale_shows_spanish_alert(self, http_client, staff_user, existing_reservation, class_slot, equipment_item, client_item):
        http_client.force_login(staff_user)
        response = http_client.post(
            "/reservations/create/",
            {
                "client": client_item.pk,
                "equipment": equipment_item.pk,
                "class_slot": class_slot.pk,
                "date": "2026-07-01",
                "notes": "",
            },
            HTTP_ACCEPT_LANGUAGE="es",
        )
        content = response.content.decode()
        assert "NO DISPONIBLE" in content

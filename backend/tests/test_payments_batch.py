import datetime
import json
from zoneinfo import ZoneInfo

import pytest
from django.contrib.auth.models import User
from django.test import Client as HttpClient
from django.utils import timezone

from apps.clients.models import Client
from apps.payments.models import Payment, PaymentReservation


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
        first_name="John",
        last_name="Doe",
        mobile="+1234567890",
    )


@pytest.fixture
def equipment(db):
    from apps.equipment.models import Equipment

    return Equipment.objects.create(
        name="Cinta 1", equipment_type="treadmill", status="in-service"
    )


@pytest.fixture
def class_slot(db):
    from apps.classes.models import ClassSlot

    return ClassSlot.objects.create(day_of_week=0, time="19:15", is_active=True)


@pytest.fixture
def payment_data(client, staff_user):
    return {
        "client": client,
        "amount": 100.00,
        "payment_type": "CC",
        "date": datetime.date.today(),
        "class_slot_count": 3,
        "reference": "BATCH-REF",
        "created_by": staff_user,
    }


@pytest.fixture
def payment(db, payment_data):
    return Payment.objects.create(**payment_data)


@pytest.mark.django_db
class TestBatchModalAppears:
    """T009: Batch modal appears after payment creation."""

    def test_modal_shown_on_payment_create(self, logged_client, client):
        response = logged_client.post(
            "/payments/create/",
            {
                "client": client.id,
                "amount": 100,
                "payment_type": "CASH",
                "date": datetime.date.today(),
                "class_slot_count": 3,
                "payment_identifier": "",
            },
            follow=True,
        )
        assert response.status_code == 200
        content = response.content.decode()
        assert "batchModal" in content


@pytest.mark.django_db
class TestBatchModalContextData:
    """T010: Batch modal context data returns the expected fields."""

    def test_batch_data_returns_context(
        self, logged_client, payment, equipment, class_slot
    ):
        response = logged_client.get(f"/payments/{payment.pk}/batch-data/")
        assert response.status_code == 200
        data = response.json()
        assert data["payment_id"] == payment.pk
        assert data["block_class_count"] == payment.class_slot_count
        assert len(data["equipment_list"]) > 0
        assert len(data["class_slots"]) > 0
        assert "date_range" in data
        assert "start" in data["date_range"]
        assert "end" in data["date_range"]
        assert isinstance(data["equipment_list"], list)
        assert isinstance(data["class_slots"], list)
        assert isinstance(data["reserved_dates"], list)


@pytest.mark.django_db
class TestPaymentDayBatchWindow:
    """Payment-day slots determine the start of the batch window."""

    @pytest.fixture
    def payment_day_slots(self, db):
        from apps.classes.models import ClassSlot

        return [
            ClassSlot.objects.create(day_of_week=1, time="19:15", is_active=True),
            ClassSlot.objects.create(day_of_week=1, time="20:15", is_active=True),
            ClassSlot.objects.create(day_of_week=2, time="19:15", is_active=True),
            ClassSlot.objects.create(day_of_week=2, time="20:15", is_active=True),
        ]

    @staticmethod
    def set_payment_time(payment, hour, minute):
        created_at = timezone.make_aware(
            datetime.datetime(2026, 8, 11, hour, minute),
            ZoneInfo("America/Denver"),
        )
        payment.created_at = created_at
        payment.save(update_fields=["created_at"])

    def test_1700_includes_payment_day_and_ends_august_31(
        self, logged_client, payment, payment_day_slots
    ):
        payment.class_slot_count = 5
        payment.date = datetime.date(2026, 8, 11)
        payment.save(update_fields=["class_slot_count", "date"])
        self.set_payment_time(payment, 17, 0)

        response = logged_client.get(f"/payments/{payment.pk}/batch-data/")

        assert response.json()["date_range"] == {
            "start": "2026-08-11",
            "end": "2026-08-31",
        }

    def test_1900_includes_payment_day_and_ends_august_31(
        self, logged_client, payment, payment_day_slots
    ):
        payment.class_slot_count = 5
        payment.date = datetime.date(2026, 8, 11)
        payment.save(update_fields=["class_slot_count", "date"])
        self.set_payment_time(payment, 19, 0)

        response = logged_client.get(f"/payments/{payment.pk}/batch-data/")

        assert response.json()["date_range"] == {
            "start": "2026-08-11",
            "end": "2026-08-31",
        }

    def test_1920_keeps_only_upcoming_payment_day_time_in_validation(
        self, logged_client, payment, equipment, payment_day_slots
    ):
        payment.class_slot_count = 1
        payment.date = datetime.date(2026, 8, 11)
        payment.save(update_fields=["class_slot_count", "date"])
        self.set_payment_time(payment, 19, 20)

        response = logged_client.post(
            f"/payments/{payment.pk}/batch-create/",
            json.dumps(
                {
                    "payment_id": payment.pk,
                    "equipment_id": equipment.id,
                    "class_slot_id": payment_day_slots[0].id,
                    "dates": ["2026-08-11"],
                }
            ),
            content_type="application/json",
        )

        assert response.status_code == 400
        assert "dates" in response.json()["errors"]

    def test_2020_starts_next_day_and_ends_september_1(
        self, logged_client, payment, payment_day_slots
    ):
        payment.class_slot_count = 5
        payment.date = datetime.date(2026, 8, 11)
        payment.save(update_fields=["class_slot_count", "date"])
        self.set_payment_time(payment, 20, 20)

        response = logged_client.get(f"/payments/{payment.pk}/batch-data/")

        assert response.json()["date_range"] == {
            "start": "2026-08-12",
            "end": "2026-09-01",
        }

    def test_latest_client_reservation_still_moves_window_forward(
        self, logged_client, payment, payment_day_slots, equipment, staff_user
    ):
        from apps.reservations.models import Reservation

        payment.date = datetime.date(2026, 8, 11)
        payment.save(update_fields=["date"])
        self.set_payment_time(payment, 17, 0)
        Reservation.objects.create(
            client=payment.client,
            equipment=equipment,
            class_slot=payment_day_slots[2],
            date=datetime.date(2026, 8, 20),
            created_by=staff_user,
        )

        response = logged_client.get(f"/payments/{payment.pk}/batch-data/")

        assert response.json()["date_range"] == {
            "start": "2026-08-25",
            "end": "2026-09-14",
        }


@pytest.mark.django_db
class TestBatchValidationRegression:
    def test_duplicate_dates_are_rejected(
        self, logged_client, payment, equipment, class_slot
    ):
        payment.class_slot_count = 2
        payment.save(update_fields=["class_slot_count"])
        response = logged_client.post(
            f"/payments/{payment.pk}/batch-create/",
            json.dumps(
                {
                    "payment_id": payment.pk,
                    "equipment_id": equipment.id,
                    "class_slot_id": class_slot.id,
                    "dates": [
                        payment.date.isoformat(),
                        payment.date.isoformat(),
                    ],
                }
            ),
            content_type="application/json",
        )

        assert response.status_code == 400
        assert "dates" in response.json()["errors"]

    def test_inactive_class_slot_is_rejected(
        self, logged_client, payment, equipment, db
    ):
        from apps.classes.models import ClassSlot

        inactive_slot = ClassSlot.objects.create(
            day_of_week=0,
            time="20:15",
            is_active=False,
        )
        response = logged_client.post(
            f"/payments/{payment.pk}/batch-create/",
            json.dumps(
                {
                    "payment_id": payment.pk,
                    "equipment_id": equipment.id,
                    "class_slot_id": inactive_slot.id,
                    "dates": [payment.date.isoformat()] * payment.class_slot_count,
                }
            ),
            content_type="application/json",
        )

        assert response.status_code == 400
        assert "class_slot_id" in response.json()["errors"]


@pytest.mark.django_db
class TestBatchCreation:
    """T011: Batch creation creates N reservations linked to payment."""

    def test_batch_creates_n_reservations(
        self, logged_client, payment, equipment, class_slot
    ):
        start = payment.date
        next_monday = start + datetime.timedelta(days=(7 - start.weekday()) % 7 or 7)
        dates = [
            (next_monday + datetime.timedelta(weeks=i)).isoformat()
            for i in range(payment.class_slot_count)
        ]
        response = logged_client.post(
            f"/payments/{payment.pk}/batch-create/",
            json.dumps(
                {
                    "payment_id": payment.pk,
                    "equipment_id": equipment.id,
                    "class_slot_id": class_slot.id,
                    "dates": dates,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["created"] == payment.class_slot_count
        assert (
            PaymentReservation.objects.filter(payment=payment).count()
            == payment.class_slot_count
        )


@pytest.mark.django_db
class TestBatchRedirectToDetail:
    """T012: After batch creation, page redirects to payment detail."""

    def test_batch_redirects_on_success(
        self, logged_client, payment, equipment, class_slot
    ):
        start = payment.date
        next_monday = start + datetime.timedelta(days=(7 - start.weekday()) % 7 or 7)
        dates = [
            (next_monday + datetime.timedelta(weeks=i)).isoformat()
            for i in range(payment.class_slot_count)
        ]
        response = logged_client.post(
            f"/payments/{payment.pk}/batch-create/",
            json.dumps(
                {
                    "payment_id": payment.pk,
                    "equipment_id": equipment.id,
                    "class_slot_id": class_slot.id,
                    "dates": dates,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        # Client-side redirect happens in JS after receiving the response
        # Verify payment detail renders linked reservations
        detail = logged_client.get(f"/payments/{payment.pk}/")
        assert detail.status_code == 200
        detail_html = detail.content.decode()
        for r in PaymentReservation.objects.filter(payment=payment):
            from django.template.defaultfilters import date as date_filter

            formatted = date_filter(r.reservation.date, "SHORT_DATE_FORMAT")
            assert formatted in detail_html


@pytest.mark.django_db
class TestBatchZeroClassCount:
    """T013: Batch with zero class_slot_count does not show modal."""

    def test_zero_class_count_no_modal(self, logged_client, client):
        response = logged_client.post(
            "/payments/create/",
            {
                "client": client.id,
                "amount": 50,
                "payment_type": "CASH",
                "date": datetime.date.today(),
                "class_slot_count": 0,
                "payment_identifier": "",
            },
        )
        assert response.status_code == 200
        content = response.content.decode()
        assert "batchModal" not in content


@pytest.mark.django_db
class TestBatchPartialFailure:
    """T014: Partial failure on unique constraint conflicts."""

    def test_partial_failure_on_conflict(
        self, logged_client, payment, equipment, class_slot, staff_user, db
    ):
        from apps.reservations.models import Reservation

        # Use a different client so the pre-created reservation does not shift
        # the range.
        other_client = Client.objects.create(
            first_name="Other",
            last_name="Client",
            mobile="+9999999999",
        )
        start = payment.date
        next_monday = start + datetime.timedelta(days=(7 - start.weekday()) % 7 or 7)
        conflict_date = next_monday + datetime.timedelta(weeks=1)
        dates = [
            next_monday.isoformat(),
            conflict_date.isoformat(),
            (next_monday + datetime.timedelta(weeks=2)).isoformat(),
        ]
        # Same equipment, slot, and date blocks the unique constraint.
        Reservation.objects.create(
            client=other_client,
            equipment=equipment,
            class_slot=class_slot,
            date=conflict_date,
            created_by=staff_user,
            status="reserved",
        )
        response = logged_client.post(
            f"/payments/{payment.pk}/batch-create/",
            json.dumps(
                {
                    "payment_id": payment.pk,
                    "equipment_id": equipment.id,
                    "class_slot_id": class_slot.id,
                    "dates": dates,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "partial"
        assert data["created"] == 2
        assert len(data["failed"]) == 1


@pytest.mark.django_db
class TestBatchMax20:
    """T021: Exceeding 20 reservations shows warning."""

    def test_exceed_20_fails(
        self, logged_client, client, staff_user, equipment, class_slot
    ):
        payment = Payment.objects.create(
            client=client,
            amount=200,
            payment_type="CASH",
            date=datetime.date.today(),
            class_slot_count=25,
            reference="MAX-20",
            created_by=staff_user,
        )
        start = payment.date
        next_monday = start + datetime.timedelta(days=(7 - start.weekday()) % 7 or 7)
        dates = [
            (next_monday + datetime.timedelta(weeks=i)).isoformat() for i in range(25)
        ]
        response = logged_client.post(
            f"/payments/{payment.pk}/batch-create/",
            json.dumps(
                {
                    "payment_id": payment.pk,
                    "equipment_id": equipment.id,
                    "class_slot_id": class_slot.id,
                    "dates": dates,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 400
        data = response.json()
        assert data["status"] == "error"


@pytest.mark.django_db
class TestBatchDateRange:
    """T022: Selecting dates outside 4-week range is prevented."""

    def test_outside_range_fails(self, logged_client, payment, equipment, class_slot):
        # Override to 2 so we can send 2 dates (1 in range, 1 out)
        payment.class_slot_count = 2
        payment.save()
        start = payment.date
        next_monday = start + datetime.timedelta(days=(7 - start.weekday()) % 7 or 7)
        # One date within range, one outside (5 weeks out)
        dates = [
            next_monday.isoformat(),
            (next_monday + datetime.timedelta(weeks=5)).isoformat(),
        ]
        response = logged_client.post(
            f"/payments/{payment.pk}/batch-create/",
            json.dumps(
                {
                    "payment_id": payment.pk,
                    "equipment_id": equipment.id,
                    "class_slot_id": class_slot.id,
                    "dates": dates,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 400
        data = response.json()
        assert data["status"] == "error"


@pytest.mark.django_db
class TestBatchExactCount:
    """T023: Selecting fewer dates than block class count is prevented."""

    def test_fewer_dates_fails(self, logged_client, payment, equipment, class_slot):
        start = payment.date
        next_monday = start + datetime.timedelta(days=(7 - start.weekday()) % 7 or 7)
        # Only 1 date, but block class count is 3
        dates = [next_monday.isoformat()]
        response = logged_client.post(
            f"/payments/{payment.pk}/batch-create/",
            json.dumps(
                {
                    "payment_id": payment.pk,
                    "equipment_id": equipment.id,
                    "class_slot_id": class_slot.id,
                    "dates": dates,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 400
        data = response.json()
        assert data["status"] == "error"
        assert "dates" in data["errors"]


@pytest.mark.django_db
class TestBatchDOWMismatch:
    """T024: DOW mismatch prevents date selection."""

    def test_dow_mismatch_fails(self, logged_client, payment, equipment, class_slot):
        # class_slot has day_of_week=0 (Monday)
        # Pick a Tuesday date
        payment.class_slot_count = 1
        payment.save()
        start = payment.date
        next_monday = start + datetime.timedelta(days=(7 - start.weekday()) % 7 or 7)
        tuesday = next_monday + datetime.timedelta(days=1)
        dates = [tuesday.isoformat()]
        response = logged_client.post(
            f"/payments/{payment.pk}/batch-create/",
            json.dumps(
                {
                    "payment_id": payment.pk,
                    "equipment_id": equipment.id,
                    "class_slot_id": class_slot.id,
                    "dates": dates,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 400
        data = response.json()
        assert data["status"] == "error"
        assert "dates" in data["errors"]


@pytest.mark.django_db
class TestBatchConflictDisplay:
    """T025: Partial conflict display on payment detail page."""

    def test_partial_reservations_shown_on_detail(
        self, logged_client, payment, equipment, class_slot, staff_user, db
    ):
        from apps.reservations.models import Reservation

        # Use a different client so the pre-created reservation does not shift
        # the range.
        other_client = Client.objects.create(
            first_name="Other",
            last_name="Client",
            mobile="+8888888888",
        )
        payment.class_slot_count = 2
        payment.save()
        start = payment.date
        next_monday = start + datetime.timedelta(days=(7 - start.weekday()) % 7 or 7)
        conflict_date = next_monday
        success_date = next_monday + datetime.timedelta(weeks=1)
        dates = [success_date.isoformat(), conflict_date.isoformat()]
        # Pre-create conflict for OTHER client (same equipment+class_slot+date)
        Reservation.objects.create(
            client=other_client,
            equipment=equipment,
            class_slot=class_slot,
            date=conflict_date,
            created_by=staff_user,
            status="reserved",
        )
        response = logged_client.post(
            f"/payments/{payment.pk}/batch-create/",
            json.dumps(
                {
                    "payment_id": payment.pk,
                    "equipment_id": equipment.id,
                    "class_slot_id": class_slot.id,
                    "dates": dates,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "partial"
        assert data["created"] == 1
        assert len(data["failed"]) == 1
        # Verify payment detail shows the successfully created reservation
        detail = logged_client.get(f"/payments/{payment.pk}/")
        assert detail.status_code == 200
        detail_html = detail.content.decode()
        from django.template.defaultfilters import date as date_filter

        assert date_filter(success_date, "SHORT_DATE_FORMAT") in detail_html

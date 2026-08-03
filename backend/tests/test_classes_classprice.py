"""Tests for ClassPrice versioning, audit, atomic swap, and deletion prevention."""

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError, transaction
from django.test import Client as HttpClient

from apps.classes.models import ClassPrice, ClassSlot

User = get_user_model()


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture
def http_client():
    return HttpClient()


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username="admin",
        password="pass",
        email="admin@example.com",
    )


@pytest.fixture
def staff_user(db):
    return User.objects.create_user(
        username="staff",
        password="pass",
        is_staff=True,
    )


@pytest.fixture
def non_admin_user(db):
    return User.objects.create_user(
        username="regular",
        password="pass",
    )


@pytest.fixture
def admin_group(db):
    from django.contrib.auth.models import Group

    return Group.objects.create(name="Administrators")


@pytest.fixture
def admin_user_with_group(admin_group, db):
    return User.objects.create_user(
        username="admin2",
        password="pass",
    )


@pytest.fixture
def admin_with_group(admin_user_with_group, admin_group):
    admin_user_with_group.groups.add(admin_group)
    return admin_user_with_group


@pytest.fixture
def class_slot(db):
    slot = ClassSlot.objects.create(day_of_week=0, time="17:30")
    slot.refresh_from_db()
    return slot


@pytest.fixture
def logged_client(http_client, admin_user):
    http_client.force_login(admin_user)
    return http_client


# ── Phase 2: Model Invariants (T003) ─────────────────────────────────────────────


@pytest.mark.django_db
class TestClassPriceModel:
    """TDD tests for ClassPrice model fields and invariants."""

    def test_fields_and_defaults(self, class_slot, admin_user):
        price = ClassPrice.objects.create(
            class_slot=class_slot,
            price=100.00,
            created_by=admin_user,
        )
        assert price.current is True
        assert price.changed_at is None
        assert price.changed_by is None
        assert price.created_at is not None
        assert price.updated_at is not None

    def test_price_is_immutable_after_creation(self, class_slot, admin_user):
        price = ClassPrice.objects.create(
            class_slot=class_slot,
            price=100.00,
            created_by=admin_user,
        )
        price.refresh_from_db()
        original = price.price
        price.price = 200.00
        with pytest.raises((IntegrityError, Exception)):
            price.save()
        price.refresh_from_db()
        assert price.price == original

    def test_single_current_per_slot_enforced(self, class_slot, admin_user):
        ClassPrice.objects.create(
            class_slot=class_slot,
            price=100.00,
            created_by=admin_user,
        )
        with pytest.raises(IntegrityError):
            ClassPrice.objects.create(
                class_slot=class_slot,
                price=150.00,
                created_by=admin_user,
            )

    def test_can_create_inactive_price_after_current(self, class_slot, admin_user):
        ClassPrice.objects.create(
            class_slot=class_slot,
            price=100.00,
            created_by=admin_user,
        )
        # A historical (inactive) price can coexist with a current one
        inactive = ClassPrice.objects.create(
            class_slot=class_slot,
            price=50.00,
            current=False,
            created_by=admin_user,
        )
        inactive.refresh_from_db()
        assert inactive.current is False

    def test_str_representation(self, class_slot, admin_user):
        price = ClassPrice.objects.create(
            class_slot=class_slot,
            price=100.00,
            created_by=admin_user,
        )
        assert str(price) is not None
        assert "100" in str(price)

    def test_multiple_slots_can_each_have_current(self, admin_user):
        slot1 = ClassSlot.objects.create(day_of_week=0, time="17:30")
        slot2 = ClassSlot.objects.create(day_of_week=0, time="18:30")
        ClassPrice.objects.create(
            class_slot=slot1,
            price=100.00,
            created_by=admin_user,
        )
        ClassPrice.objects.create(
            class_slot=slot2,
            price=200.00,
            created_by=admin_user,
        )
        assert ClassPrice.objects.filter(current=True).count() == 2


# ── Phase 2: Deletion Prevention Model-Level (T022/T023) ─────────────────────────


@pytest.mark.django_db
class TestClassPriceDeletionPrevention:
    """TDD tests for hard delete prevention at model/queryset level."""

    def test_instance_delete_raises(self, class_slot, admin_user):
        price = ClassPrice.objects.create(
            class_slot=class_slot,
            price=100.00,
            created_by=admin_user,
        )
        with pytest.raises((PermissionDenied, RuntimeError, Exception)):
            price.delete()
        # Record still exists
        assert ClassPrice.objects.filter(pk=price.pk).exists()

    def test_queryset_delete_raises(self, class_slot, admin_user):
        ClassPrice.objects.create(
            class_slot=class_slot,
            price=100.00,
            created_by=admin_user,
        )
        with pytest.raises((PermissionDenied, RuntimeError, Exception)):
            ClassPrice.objects.all().delete()
        assert ClassPrice.objects.filter(class_slot=class_slot).count() == 1

    def test_filter_queryset_delete_raises(self, class_slot, admin_user):
        ClassPrice.objects.create(
            class_slot=class_slot,
            price=100.00,
            created_by=admin_user,
        )
        with pytest.raises((PermissionDenied, RuntimeError, Exception)):
            ClassPrice.objects.filter(current=True).delete()
        assert ClassPrice.objects.filter(class_slot=class_slot).count() == 1


# ── Phase 3: Atomic Price-Swap Service (T008/T009) ──────────────────────────────


@pytest.mark.django_db
class TestClassPriceAtomicSwap:
    """TDD tests for the atomic price-entry service."""

    def test_enter_first_price(self, class_slot, admin_user):
        new_price = ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=150.00,
            changed_by=admin_user,
        )
        new_price.refresh_from_db()
        assert new_price.current is True
        assert new_price.price == 150.00
        assert new_price.changed_at is None
        assert new_price.changed_by is None
        assert (
            ClassPrice.objects.filter(
                class_slot=class_slot,
                current=True,
            ).count()
            == 1
        )

    def test_update_archives_previous(self, class_slot, admin_user):
        original = ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=100.00,
            changed_by=admin_user,
        )
        new = ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=150.00,
            changed_by=admin_user,
        )
        original.refresh_from_db()
        new.refresh_from_db()
        assert original.current is False
        assert original.changed_at is not None
        assert original.changed_by == admin_user
        assert original.price == 100.00  # price immutable
        assert new.current is True
        assert new.changed_at is None
        assert (
            ClassPrice.objects.filter(
                class_slot=class_slot,
                current=True,
            ).count()
            == 1
        )

    def test_atomic_swap_rollback(self, class_slot, admin_user):
        original = ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=100.00,
            changed_by=admin_user,
        )
        # Force an error during the second enter_price by using an invalid value
        # The service should rollback, keeping the original current
        with pytest.raises(Exception):
            with transaction.atomic():
                # Simulate failure by creating an invalid second current price manually
                ClassPrice.objects.create(
                    class_slot=class_slot,
                    price=999.00,
                    created_by=admin_user,
                )
        original.refresh_from_db()
        assert original.current is True
        assert (
            ClassPrice.objects.filter(
                class_slot=class_slot,
                current=True,
            ).count()
            == 1
        )

    def test_multiple_updates_preserve_history(self, class_slot, admin_user):
        p1 = ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=100.00,
            changed_by=admin_user,
        )
        p2 = ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=120.00,
            changed_by=admin_user,
        )
        p3 = ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=150.00,
            changed_by=admin_user,
        )
        p1.refresh_from_db()
        p2.refresh_from_db()
        p3.refresh_from_db()
        assert p1.current is False
        assert p2.current is False
        assert p3.current is True
        assert ClassPrice.objects.filter(class_slot=class_slot).count() == 3

    def test_history_ordering_descending(self, class_slot, admin_user):
        p1 = ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=100.00,
            changed_by=admin_user,
        )
        p2 = ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=120.00,
            changed_by=admin_user,
        )
        p3 = ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=150.00,
            changed_by=admin_user,
        )
        history = list(
            ClassPrice.objects.filter(class_slot=class_slot)
            .order_by("-created_at")
            .values_list("pk", "price", "current")
        )
        ids = [h[0] for h in history]
        assert ids[0] == p3.pk
        assert ids[1] == p2.pk
        assert ids[2] == p1.pk


# ── Phase 4: Prices View (T015/T016) ────────────────────────────────────────────


@pytest.mark.django_db
class TestClassPricesView:
    """TDD tests for the class prices history view."""

    def test_prices_view_requires_login(self, http_client, class_slot):
        response = http_client.get(f"/classes/{class_slot.pk}/prices/")
        assert response.status_code in (302, 401, 403)

    def test_prices_view_shows_history(self, logged_client, class_slot, admin_user):
        ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=100.00,
            changed_by=admin_user,
        )
        ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=150.00,
            changed_by=admin_user,
        )
        response = logged_client.get(f"/classes/{class_slot.pk}/prices/")
        assert response.status_code == 200
        html = response.content.decode()
        assert "150" in html
        assert "100" in html

    def test_prices_view_empty_state(self, logged_client, class_slot):
        response = logged_client.get(f"/classes/{class_slot.pk}/prices/")
        assert response.status_code == 200
        html = response.content.decode()
        assert "no price history" in html.lower() or "historial" in html.lower()

    def test_prices_view_shows_current_badge(
        self,
        logged_client,
        class_slot,
        admin_user,
    ):
        ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=100.00,
            changed_by=admin_user,
        )
        ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=150.00,
            changed_by=admin_user,
        )
        response = logged_client.get(f"/classes/{class_slot.pk}/prices/")
        assert response.status_code == 200
        html = response.content.decode()
        assert "actual" in html.lower()

    def test_prices_view_shows_audit_attribution(
        self,
        logged_client,
        class_slot,
        admin_user,
    ):
        ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=100.00,
            changed_by=admin_user,
        )
        response = logged_client.get(f"/classes/{class_slot.pk}/prices/")
        assert response.status_code == 200
        html = response.content.decode()
        assert admin_user.username in html

    def test_prices_view_descending_order(
        self,
        logged_client,
        class_slot,
        admin_user,
    ):
        ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=100.00,
            changed_by=admin_user,
        )
        ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=150.00,
            changed_by=admin_user,
        )
        ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=200.00,
            changed_by=admin_user,
        )
        response = logged_client.get(f"/classes/{class_slot.pk}/prices/")
        assert response.status_code == 200
        html = response.content.decode()
        pos_200 = html.find("200")
        pos_150 = html.find("150")
        pos_100 = html.find("100")
        assert pos_200 < pos_150 < pos_100, "Prices should appear in descending"


# ── Phase 3: Create Price View — Admin Only (T011/T012) ───────────────────────────


@pytest.mark.django_db
class TestClassPriceCreateView:
    """TDD tests for the admin-only price add view."""

    def test_add_price_view_renders_for_admin(self, logged_client, class_slot):
        response = logged_client.get(f"/classes/{class_slot.pk}/prices/add/")
        assert response.status_code == 200

    def test_add_price_post_creates_price(self, logged_client, class_slot, admin_user):
        response = logged_client.post(
            f"/classes/{class_slot.pk}/prices/add/",
            {"price": "150.00"},
            follow=True,
        )
        assert response.status_code == 200
        assert (
            ClassPrice.objects.filter(
                class_slot=class_slot,
                current=True,
            ).count()
            == 1
        )
        price = ClassPrice.objects.get(class_slot=class_slot, current=True)
        assert price.price == 150.00
        assert price.created_by == admin_user

    def test_add_price_archives_previous(self, logged_client, class_slot, admin_user):
        ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=100.00,
            changed_by=admin_user,
        )
        logged_client.post(
            f"/classes/{class_slot.pk}/prices/add/",
            {"price": "200.00"},
            follow=True,
        )
        prices = ClassPrice.objects.filter(class_slot=class_slot).order_by("created_at")
        assert prices.count() == 2
        assert prices[0].current is False
        assert prices[0].price == 100.00
        assert prices[1].current is True
        assert prices[1].price == 200.00

    def test_non_admin_denied_add_view(self, http_client, non_admin_user, class_slot):
        http_client.force_login(non_admin_user)
        response = http_client.get(f"/classes/{class_slot.pk}/prices/add/")
        assert response.status_code in (302, 403)

    def test_non_admin_denied_add_post(self, http_client, non_admin_user, class_slot):
        http_client.force_login(non_admin_user)
        response = http_client.post(
            f"/classes/{class_slot.pk}/prices/add/",
            {"price": "150.00"},
        )
        assert response.status_code in (302, 403)
        assert not ClassPrice.objects.filter(class_slot=class_slot).exists()

    def test_add_price_invalid_negative_rejected(
        self,
        logged_client,
        class_slot,
        admin_user,
    ):
        response = logged_client.post(
            f"/classes/{class_slot.pk}/prices/add/",
            {"price": "-50.00"},
        )
        assert response.status_code == 200
        assert not ClassPrice.objects.filter(
            class_slot=class_slot,
            price=-50.00,
        ).exists()

    def test_add_price_invalid_zero_rejected(
        self,
        logged_client,
        class_slot,
        admin_user,
    ):
        response = logged_client.post(
            f"/classes/{class_slot.pk}/prices/add/",
            {"price": "0.00"},
        )
        assert response.status_code == 200
        assert not ClassPrice.objects.filter(class_slot=class_slot).exists()

    def test_anonymous_denied_add_view(self, http_client, class_slot):
        response = http_client.get(f"/classes/{class_slot.pk}/prices/add/")
        assert response.status_code in (302, 401, 403)


# ── Admin Delete Permission (T024) ───────────────────────────────────────────────


@pytest.mark.django_db
class TestClassPriceAdminDelete:
    """TDD tests that admin delete action is disabled."""

    def test_admin_has_delete_permission_false(self, admin_user):
        from apps.classes.admin import ClassPriceAdmin

        site_admin = ClassPriceAdmin(ClassPrice, None)
        assert site_admin.has_delete_permission(None, None) is False


# ── Quickstart Scenario Validations ──────────────────────────────────────────────


@pytest.mark.django_db
class TestQuickstartValidation:
    """End-to-end quickstart scenario validations."""

    def test_scenario_1_first_price(self, class_slot, admin_user):
        """SC-001: First price becomes the current price with attribution."""
        new = ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=100.00,
            changed_by=admin_user,
        )
        new.refresh_from_db()
        assert new.current is True
        assert new.created_by == admin_user
        assert (
            ClassPrice.objects.filter(
                class_slot=class_slot,
                current=True,
            ).count()
            == 1
        )

    def test_scenario_2_update_archives(self, class_slot, admin_user):
        """SC-001: Updating a price archives the previous one."""
        original = ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=100.00,
            changed_by=admin_user,
        )
        new = ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=150.00,
            changed_by=admin_user,
        )
        original.refresh_from_db()
        new.refresh_from_db()
        assert original.current is False
        assert original.changed_at is not None
        assert original.changed_by == admin_user
        assert new.current is True
        assert original.price == 100.00
        assert new.price == 150.00

    def test_scenario_3_single_current_enforced(self, class_slot, admin_user):
        """FR-009: Only one current price per class."""
        ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=100.00,
            changed_by=admin_user,
        )
        with pytest.raises(IntegrityError):
            ClassPrice.objects.create(
                class_slot=class_slot,
                price=200.00,
                created_by=admin_user,
            )

    def test_scenario_4_history_ordering(self, class_slot, admin_user):
        """FR-006: History in descending order with current flag."""
        p1 = ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=100.00,
            changed_by=admin_user,
        )
        p2 = ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=120.00,
            changed_by=admin_user,
        )
        p3 = ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=150.00,
            changed_by=admin_user,
        )
        history = list(
            ClassPrice.objects.filter(class_slot=class_slot)
            .order_by("-created_at")
            .values_list("pk", "price", "current")
        )
        assert history[0][0] == p3.pk
        assert history[1][0] == p2.pk
        assert history[2][0] == p1.pk
        assert history[0][2] is True  # p3 is current

    def test_scenario_5_deletion_prevented(self, class_slot, admin_user):
        """FR-008: No price record can be deleted."""
        price = ClassPrice.objects.enter_price(
            class_slot=class_slot,
            new_price=100.00,
            changed_by=admin_user,
        )
        count_before = ClassPrice.objects.count()
        with pytest.raises((PermissionDenied, RuntimeError, Exception)):
            price.delete()
        with pytest.raises((PermissionDenied, RuntimeError, Exception)):
            ClassPrice.objects.all().delete()
        assert ClassPrice.objects.count() == count_before

    def test_scenario_6_admin_only_changes(
        self,
        http_client,
        non_admin_user,
        class_slot,
    ):
        """FR-011: Only authorized administrators may enter prices."""
        http_client.force_login(non_admin_user)
        response = http_client.post(
            f"/classes/{class_slot.pk}/prices/add/",
            {"price": "150.00"},
        )
        assert response.status_code in (302, 403)
        assert not ClassPrice.objects.filter(class_slot=class_slot).exists()

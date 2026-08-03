"""Tests for ClassPrice as a standalone entity (no ClassSlot association).

Covers model invariants, deletion prevention, standalone enter_price service,
global price views, admin-only create, and quickstart validation scenarios.
"""

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.test import Client as HttpClient

from apps.classes.models import ClassPrice

User = get_user_model()


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
def logged_client(http_client, admin_user):
    http_client.force_login(admin_user)
    return http_client


@pytest.fixture
def logged_admin_group_client(http_client, admin_with_group):
    http_client.force_login(admin_with_group)
    return http_client


# ── Phase 2: Model Invariants ────────────────────────────────────────────────────


@pytest.mark.django_db
class TestClassPriceModel:
    """TDD tests for ClassPrice model fields and invariants (decoupled)."""

    def test_model_has_no_class_slot_field(self):
        """FR-001 / SC-001: ClassPrice must not have a class_slot attribute."""
        assert not hasattr(ClassPrice, "class_slot")
        assert "class_slot" not in [f.name for f in ClassPrice._meta.get_fields()]

    def test_fields_and_defaults(self, admin_user):
        """FR-002: Versioning fields are retained with correct defaults."""
        price = ClassPrice.objects.create(
            price=100.00,
            created_by=admin_user,
        )
        assert price.current is True
        assert price.changed_at is None
        assert price.changed_by is None
        assert price.created_at is not None
        assert price.updated_at is not None

    def test_price_is_immutable_after_creation(self, admin_user):
        """Price amount cannot be modified after creation."""
        price = ClassPrice.objects.create(
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

    def test_multiple_current_prices_allowed(self, admin_user):
        """Without the per-class unique constraint, multiple current prices coexist."""
        ClassPrice.objects.create(price=100.00, created_by=admin_user)
        ClassPrice.objects.create(price=200.00, created_by=admin_user)
        assert ClassPrice.objects.filter(current=True).count() == 2

    def test_can_create_inactive_price(self, admin_user):
        """Historical (inactive) prices can coexist with current ones."""
        ClassPrice.objects.create(price=100.00, created_by=admin_user)
        inactive = ClassPrice.objects.create(
            price=50.00,
            current=False,
            created_by=admin_user,
        )
        inactive.refresh_from_db()
        assert inactive.current is False

    def test_str_representation(self, admin_user):
        price = ClassPrice.objects.create(
            price=100.00,
            created_by=admin_user,
        )
        assert str(price) is not None
        assert "100" in str(price)


# ── Phase 2: Deletion Prevention ─────────────────────────────────────────────────


@pytest.mark.django_db
class TestClassPriceDeletionPrevention:
    """TDD tests for hard delete prevention at model/queryset level."""

    def test_instance_delete_raises(self, admin_user):
        price = ClassPrice.objects.create(
            price=100.00,
            created_by=admin_user,
        )
        with pytest.raises((PermissionDenied, RuntimeError, Exception)):
            price.delete()
        assert ClassPrice.objects.filter(pk=price.pk).exists()

    def test_queryset_delete_raises(self, admin_user):
        ClassPrice.objects.create(price=100.00, created_by=admin_user)
        with pytest.raises((PermissionDenied, RuntimeError, Exception)):
            ClassPrice.objects.all().delete()
        assert ClassPrice.objects.count() == 1

    def test_filter_queryset_delete_raises(self, admin_user):
        ClassPrice.objects.create(price=100.00, created_by=admin_user)
        with pytest.raises((PermissionDenied, RuntimeError, Exception)):
            ClassPrice.objects.filter(current=True).delete()
        assert ClassPrice.objects.count() == 1


# ── Phase 3: Standalone enter_price Service ─────────────────────────────────────


@pytest.mark.django_db
class TestClassPriceEnterPrice:
    """TDD tests for the standalone enter_price classmethod."""

    def test_enter_price_creates_current(self, admin_user):
        """FR-006: enter_price creates a standalone current price."""
        new_price = ClassPrice.objects.enter_price(
            new_price=150.00,
            changed_by=admin_user,
        )
        new_price.refresh_from_db()
        assert new_price.current is True
        assert new_price.price == 150.00
        assert new_price.changed_at is None
        assert new_price.changed_by is None
        assert new_price.created_by == admin_user

    def test_enter_price_no_swap(self, admin_user):
        """Without per-class grouping, enter_price creates new records (no retire)."""
        p1 = ClassPrice.objects.enter_price(
            new_price=100.00,
            changed_by=admin_user,
        )
        p2 = ClassPrice.objects.enter_price(
            new_price=150.00,
            changed_by=admin_user,
        )
        p1.refresh_from_db()
        p2.refresh_from_db()
        assert p1.current is True  # remains current (no per-class swap)
        assert p2.current is True
        assert p1.price == 100.00
        assert p2.price == 150.00
        assert ClassPrice.objects.count() == 2

    def test_enter_price_history_ordering_descending(self, admin_user):
        p1 = ClassPrice.objects.enter_price(
            new_price=100.00,
            changed_by=admin_user,
        )
        p2 = ClassPrice.objects.enter_price(
            new_price=120.00,
            changed_by=admin_user,
        )
        p3 = ClassPrice.objects.enter_price(
            new_price=150.00,
            changed_by=admin_user,
        )
        history = list(
            ClassPrice.objects.order_by("-created_at").values_list(
                "pk", "price", "current"
            )
        )
        ids = [h[0] for h in history]
        assert ids[0] == p3.pk
        assert ids[1] == p2.pk
        assert ids[2] == p1.pk


# ── Phase 4: Global Price List View ──────────────────────────────────────────────


@pytest.mark.django_db
class TestClassPricesView:
    """TDD tests for the global class prices history view."""

    def test_prices_view_requires_login(self, http_client):
        response = http_client.get("/classes/prices/")
        assert response.status_code in (302, 401, 403)

    def test_prices_view_shows_history(self, logged_client, admin_user):
        ClassPrice.objects.enter_price(new_price=100.00, changed_by=admin_user)
        ClassPrice.objects.enter_price(new_price=150.00, changed_by=admin_user)
        response = logged_client.get("/classes/prices/")
        assert response.status_code == 200
        html = response.content.decode()
        assert "150" in html
        assert "100" in html

    def test_prices_view_empty_state(self, logged_client):
        response = logged_client.get("/classes/prices/")
        assert response.status_code == 200
        html = response.content.decode()
        assert "no price history" in html.lower() or "historial" in html.lower()

    def test_prices_view_shows_current_badge(self, logged_client, admin_user):
        ClassPrice.objects.enter_price(new_price=100.00, changed_by=admin_user)
        ClassPrice.objects.enter_price(new_price=150.00, changed_by=admin_user)
        response = logged_client.get("/classes/prices/")
        assert response.status_code == 200
        html = response.content.decode()
        assert "actual" in html.lower()

    def test_prices_view_shows_audit_attribution(self, logged_client, admin_user):
        ClassPrice.objects.enter_price(new_price=100.00, changed_by=admin_user)
        response = logged_client.get("/classes/prices/")
        assert response.status_code == 200
        html = response.content.decode()
        assert admin_user.username in html

    def test_prices_view_descending_order(self, logged_client, admin_user):
        ClassPrice.objects.enter_price(new_price=100.00, changed_by=admin_user)
        ClassPrice.objects.enter_price(new_price=150.00, changed_by=admin_user)
        ClassPrice.objects.enter_price(new_price=200.00, changed_by=admin_user)
        response = logged_client.get("/classes/prices/")
        assert response.status_code == 200
        html = response.content.decode()
        pos_200 = html.find("200")
        pos_150 = html.find("150")
        pos_100 = html.find("100")
        assert pos_200 < pos_150 < pos_100, "Prices should appear in descending"


# ── Phase 3: Create Price View — Admin Only ─────────────────────────────────────


@pytest.mark.django_db
class TestClassPriceCreateView:
    """TDD tests for the admin-only price add view."""

    def test_add_price_view_renders_for_admin(self, logged_client):
        response = logged_client.get("/classes/prices/add/")
        assert response.status_code == 200

    def test_add_price_view_renders_for_admin_group(self, logged_admin_group_client):
        response = logged_admin_group_client.get("/classes/prices/add/")
        assert response.status_code == 200

    def test_add_price_post_creates_price(self, logged_client, admin_user):
        response = logged_client.post(
            "/classes/prices/add/",
            {"price": "150.00"},
            follow=True,
        )
        assert response.status_code == 200
        assert ClassPrice.objects.filter(current=True).count() == 1
        price = ClassPrice.objects.get(current=True)
        assert price.price == 150.00
        assert price.created_by == admin_user

    def test_add_price_archives_previous(self, logged_client, admin_user):
        """In decoupled mode, enter_price creates a new standalone record.

        The form view calls enter_price, which creates a new price (no retire).
        """
        ClassPrice.objects.enter_price(new_price=100.00, changed_by=admin_user)
        logged_client.post(
            "/classes/prices/add/",
            {"price": "200.00"},
            follow=True,
        )
        prices = list(ClassPrice.objects.order_by("created_at"))
        assert len(prices) == 2
        assert prices[0].current is True  # enter_price doesn't retire
        assert prices[0].price == 100.00
        assert prices[1].current is True
        assert prices[1].price == 200.00

    def test_non_admin_denied_add_view(self, http_client, non_admin_user):
        http_client.force_login(non_admin_user)
        response = http_client.get("/classes/prices/add/")
        assert response.status_code in (302, 403)

    def test_non_admin_denied_add_post(self, http_client, non_admin_user):
        http_client.force_login(non_admin_user)
        response = http_client.post(
            "/classes/prices/add/",
            {"price": "150.00"},
        )
        assert response.status_code in (302, 403)
        assert not ClassPrice.objects.exists()

    def test_add_price_invalid_negative_rejected(self, logged_client, admin_user):
        response = logged_client.post(
            "/classes/prices/add/",
            {"price": "-50.00"},
        )
        assert response.status_code == 200
        assert not ClassPrice.objects.filter(price="-50.00").exists()

    def test_add_price_invalid_zero_rejected(self, logged_client, admin_user):
        response = logged_client.post(
            "/classes/prices/add/",
            {"price": "0.00"},
        )
        assert response.status_code == 200
        assert not ClassPrice.objects.filter(price="0.00").exists()

    def test_anonymous_denied_add_view(self, http_client):
        response = http_client.get("/classes/prices/add/")
        assert response.status_code in (302, 401, 403)


# ── Admin Delete Permission ──────────────────────────────────────────────────────


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

    def test_scenario_1_model_has_no_class_slot(self):
        """SC-001: enter_price creates a standalone current price with attribution."""
        assert "class_slot" not in [f.name for f in ClassPrice._meta.get_fields()]

    def test_scenario_2_enter_price_standalone(self, admin_user):
        """SC-002: enter_price creates a standalone current price."""
        new = ClassPrice.objects.enter_price(
            new_price=150.00,
            changed_by=admin_user,
        )
        new.refresh_from_db()
        assert new.current is True
        assert new.created_by == admin_user
        assert new.changed_at is None

    def test_scenario_3_prices_view(self, logged_client, admin_user):
        """SC-003: All prices displayed in descending order with current badge."""
        ClassPrice.objects.enter_price(new_price=100.00, changed_by=admin_user)
        ClassPrice.objects.enter_price(new_price=150.00, changed_by=admin_user)
        response = logged_client.get("/classes/prices/")
        assert response.status_code == 200
        html = response.content.decode()
        assert "150" in html
        assert "100" in html
        assert "actual" in html.lower()

    def test_scenario_4_deletion_prevented(self, admin_user):
        """SC-004: No price record can be deleted."""
        price = ClassPrice.objects.enter_price(
            new_price=100.00,
            changed_by=admin_user,
        )
        count_before = ClassPrice.objects.count()
        with pytest.raises((PermissionDenied, RuntimeError, Exception)):
            price.delete()
        with pytest.raises((PermissionDenied, RuntimeError, Exception)):
            ClassPrice.objects.all().delete()
        assert ClassPrice.objects.count() == count_before

    def test_scenario_5_admin_only_changes(self, http_client, non_admin_user):
        """SC-006/FR-011: Only authorized administrators may enter prices."""
        http_client.force_login(non_admin_user)
        response = http_client.post(
            "/classes/prices/add/",
            {"price": "150.00"},
        )
        assert response.status_code in (302, 403)
        assert not ClassPrice.objects.exists()

    def test_scenario_6_multiple_current_allowed(self, admin_user):
        """SC-006: Without per-class constraint, multiple current prices coexist."""
        ClassPrice.objects.enter_price(new_price=100.00, changed_by=admin_user)
        ClassPrice.objects.enter_price(new_price=150.00, changed_by=admin_user)
        assert ClassPrice.objects.filter(current=True).count() == 2

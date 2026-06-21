import pytest
from django.contrib.auth.models import User
from django.test import Client as HttpClient

from apps.clients.models import Client


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
def sample_clients(db):
    Client.objects.create(
        first_name="John", last_name="Doe",
        email="john@test.com", mobile="+1 (555) 123-4567",
    )
    Client.objects.create(
        first_name="Jane", last_name="Smith",
        email="jane@example.com", mobile="+1 (555) 987-6543",
    )
    Client.objects.create(
        first_name="Mark", last_name="Johnson",
        email="mark@test.co", mobile="+54 11 5555-1212",
    )


@pytest.mark.django_db
class TestEmailHighlighting:

    def test_email_partial_match_highlighted(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=john")
        content = response.content.decode()
        assert "<mark>john</mark>" in content

    def test_email_case_insensitive_highlight(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=JOHN")
        content = response.content.decode()
        assert "<mark>john</mark>" in content or "<mark>JOHN</mark>" in content

    def test_email_highlight_with_partial_domain(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=test")
        content = response.content.decode()
        assert "<mark>test</mark>" in content

    def test_email_highlight_not_applied_for_name_below_3_chars(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=zz")
        content = response.content.decode()
        assert "<mark>" not in content


@pytest.mark.django_db
class TestMobileHighlighting:

    def test_mobile_digit_match_highlighted(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=555")
        content = response.content.decode()
        assert "<mark>555</mark>" in content

    def test_mobile_match_with_formatting(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=555")
        content = response.content.decode()
        assert "<mark>555</mark>" in content

    def test_mobile_match_across_formatting_chars(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=987")
        content = response.content.decode()
        assert "<mark>987</mark>" in content



    def test_mobile_highlight_not_applied_for_name_below_3_chars(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=zz")
        content = response.content.decode()
        assert "<mark>" not in content

    def test_mobile_highlight_partial_digits(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=1212")
        content = response.content.decode()
        assert "<mark>1212</mark>" in content


@pytest.mark.django_db
class TestHighlightConsistency:

    def test_same_mark_tag_used_across_fields(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=ar")
        content = response.content.decode()
        mark_count = content.count("<mark>")
        assert mark_count >= 3

    def test_name_highlighting_still_works(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=Joh")
        content = response.content.decode()
        assert "<mark>Joh</mark>" in content


@pytest.mark.django_db
class TestSearchRegression:

    def test_name_search_still_returns_results(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=Doe")
        content = response.content.decode()
        assert "John" in content
        assert "<mark>Doe</mark>" in content

    def test_email_search_returns_results(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=jane@example.com")
        content = response.content.decode()
        assert "Jane" in content

    def test_mobile_search_returns_results(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=+1 (555) 987-6543")
        content = response.content.decode()
        assert "Jane" in content

    def test_clear_search_removes_highlighting(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/")
        content = response.content.decode()
        assert "<mark>" not in content

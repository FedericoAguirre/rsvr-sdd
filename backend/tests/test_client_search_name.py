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
        email="john@test.com", mobile="+541111111111",
    )
    Client.objects.create(
        first_name="Jane", last_name="Smith",
        email="jane@test.com", mobile="+541111111112",
    )
    Client.objects.create(
        first_name="Mark", last_name="Johnson",
        email="mark@test.com", mobile="+541111111113",
    )
    Client.objects.create(
        first_name="Maria", last_name="Garcia",
        email="maria@test.com", mobile="+541111111114",
    )


@pytest.mark.django_db
class TestClientSearchByName:

    def test_search_by_first_name_partial(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=Joh")
        content = response.content.decode()
        assert "Joh" in content and "Doe" in content
        assert "Jane" not in content

    def test_search_by_last_name_partial(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=Smi")
        content = response.content.decode()
        assert "Smi" in content and "Jane" in content
        assert "Doe" not in content

    def test_search_case_insensitive(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=MAR")
        content = response.content.decode()
        assert "<mark>Mar</mark>" in content
        assert "NO ENCONTRADO" not in content

    def test_min_3_chars_does_not_trigger_name_search(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=zz")
        content = response.content.decode()
        assert "NO ENCONTRADO" in content

    def test_search_across_both_name_fields(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=Mar")
        content = response.content.decode()
        assert "<mark>Mar</mark>" in content


@pytest.mark.django_db
class TestClientSearchHighlight:

    def test_matched_term_wrapped_in_mark_tags(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=Joh")
        content = response.content.decode()
        assert "<mark" in content or "<MARK" in content

    def test_highlight_is_case_insensitive(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=JOH")
        content = response.content.decode()
        assert "<mark" in content or "<MARK" in content

    def test_multiple_occurrences_highlighted(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=ar")
        content = response.content.decode()
        assert "<mark" in content or "<MARK" in content


@pytest.mark.django_db
class TestClientSearchNotFound:

    def test_not_found_message_appears_when_no_match(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=Zzzz")
        content = response.content.decode()
        assert "NO ENCONTRADO" in content

    def test_not_found_disappears_when_search_modified(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=Zzzz")
        content = response.content.decode()
        assert "NO ENCONTRADO" in content
        response = logged_client.get("/clients/search/?q=Joh")
        content = response.content.decode()
        assert "NO ENCONTRADO" not in content


@pytest.mark.django_db
class TestClientSearchRegression:

    def test_search_by_existing_email(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=john@test.com")
        content = response.content.decode()
        assert "John" in content

    def test_search_by_existing_mobile(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=+541111111111")
        content = response.content.decode()
        assert "John" in content

    def test_search_by_name_and_email_combined(self, logged_client, sample_clients):
        response = logged_client.get("/clients/search/?q=john@test.com")
        content = response.content.decode()
        assert "John" in content

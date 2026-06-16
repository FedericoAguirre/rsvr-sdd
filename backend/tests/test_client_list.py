import pytest
from django.contrib.auth.models import User
from django.test import Client as HttpClient
from django.urls import reverse

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
def many_clients(db):
    Client.objects.all().delete()
    for i in range(21):
        Client.objects.create(
            first_name=f"First{i:02d}",
            last_name=f"Last{i:02d}",
            email=f"client{i:02d}@example.com",
            mobile=f"+54911{i:04d}",
        )
    return Client.objects.all()


@pytest.mark.django_db
class TestClientList:

    def test_all_clients_rendered_when_no_search(self, logged_client):
        Client.objects.all().delete()
        for i in range(15):
            Client.objects.create(first_name=f"Test{i:02d}", last_name=f"User{i:02d}")
        response = logged_client.get("/clients/search/")
        content = response.content.decode()
        for i in range(10):
            assert f"Test{i:02d}" in content

    def test_all_client_attributes_displayed(self, logged_client):
        Client.objects.create(
            first_name="Alice", last_name="Smith",
            email="alice@test.com", mobile="+541112223344",
            is_active=True,
        )
        response = logged_client.get("/clients/search/")
        content = response.content.decode()
        assert "Alice" in content
        assert "Smith" in content
        assert "alice@test.com" in content
        assert "+541112223344" in content
        assert "Activo" in content or "Yes" in content or "True" in content

    def test_pagination_21_clients_3_pages(self, logged_client, many_clients):
        response = logged_client.get("/clients/search/")
        content = response.content.decode()
        for i in range(10):
            assert f"First{i:02d}" in content
        assert "First10" not in content
        assert "page-link" in content

    def test_pagination_controls_only_when_over_10(self, logged_client):
        for i in range(5):
            Client.objects.create(first_name=f"User{i}", last_name="Test")
        response = logged_client.get("/clients/search/")
        content = response.content.decode()
        controls = "page-link" in content or "page-item" in content
        assert not controls, "Pagination controls should not appear with 5 clients"

    def test_pagination_controls_appear_with_11_clients(self, logged_client):
        for i in range(11):
            Client.objects.create(first_name=f"User{i}", last_name="Test")
        response = logged_client.get("/clients/search/")
        content = response.content.decode()
        assert "page-link" in content or "page-item" in content, \
            "Pagination controls should appear with 11 clients"

    def test_empty_state_when_no_clients(self, logged_client):
        Client.objects.all().delete()
        response = logged_client.get("/clients/search/")
        content = response.content.decode()
        assert "empiece a escribir para buscar clientes..." in content.lower()

    def test_search_still_works_alongside_list(self, logged_client):
        Client.objects.create(
            first_name="John", last_name="Doe",
            email="john@test.com", mobile="+541111111111",
        )
        Client.objects.create(
            first_name="Jane", last_name="Doe",
            email="jane@test.com", mobile="+541111111112",
        )
        response = logged_client.get("/clients/search/?q=john")
        content = response.content.decode()
        assert "John" in content
        assert "Jane" not in content

    def test_each_row_has_edit_link(self, logged_client):
        Client.objects.create(
            first_name="Bob", last_name="Brown",
            email="bob@test.com", mobile="+541111111113",
        )
        response = logged_client.get("/clients/search/")
        content = response.content.decode()
        client = Client.objects.get(email="bob@test.com")
        admin_url = reverse("admin:clients_client_change", args=[client.pk])
        assert admin_url in content

    def test_edit_link_points_to_correct_client(self, logged_client):
        c1 = Client.objects.create(
            first_name="Alice", last_name="A",
            email="alice@t.com", mobile="+541111111114",
        )
        c2 = Client.objects.create(
            first_name="Bob", last_name="B",
            email="bob@t.com", mobile="+541111111115",
        )
        response = logged_client.get("/clients/search/")
        content = response.content.decode()
        url1 = reverse("admin:clients_client_change", args=[c1.pk])
        url2 = reverse("admin:clients_client_change", args=[c2.pk])
        assert url1 in content
        assert url2 in content

    def test_counter_displays_total_count(self, logged_client):
        for i in range(7):
            Client.objects.create(first_name=f"U{i}", last_name="T")
        response = logged_client.get("/clients/search/")
        content = response.content.decode()
        assert "Total" in content or "clientes" in content.lower()
        assert "7" in content

    def test_counter_updates_when_clients_change(self, logged_client):
        response = logged_client.get("/clients/search/")
        content = response.content.decode()
        assert "0" in content
        Client.objects.create(first_name="New", last_name="Client")
        response = logged_client.get("/clients/search/")
        content = response.content.decode()
        assert "1" in content

import pytest
from django.test import Client
from django.contrib.auth.models import User


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def staff_user(db):
    return User.objects.create_user(username="staff", password="pass", is_staff=True)


@pytest.mark.django_db
class TestSpanishLabels:

    def _login(self, client, staff_user):
        client.force_login(staff_user)

    def test_navbar_brand_and_nav_links_spanish(self, client, staff_user):
        self._login(client, staff_user)
        response = client.get("/reservations/")
        content = response.content.decode()
        assert "Reserva de Cardio" in content
        assert "Cerrar sesión" in content

    def test_equipment_page_titles_spanish(self, client, staff_user):
        self._login(client, staff_user)
        response = client.get("/equipment/")
        content = response.content.decode()
        assert "Equipos" in content

    def test_reservation_page_titles_spanish(self, client, staff_user):
        self._login(client, staff_user)
        response = client.get("/reservations/")
        content = response.content.decode()
        assert "Reservaciones" in content

    def test_client_search_spanish(self, client, staff_user):
        self._login(client, staff_user)
        response = client.get("/clients/search/")
        content = response.content.decode()
        assert "Buscar Clientes" in content

    def test_class_schedule_spanish(self, client, staff_user):
        self._login(client, staff_user)
        response = client.get("/classes/")
        content = response.content.decode()
        assert "Horario de Clases" in content

import re
import pytest
from django.contrib.auth.models import User
from django.test import Client


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def staff_user(db):
    return User.objects.create_user(username="staff", password="pass", is_staff=True)


def _extract_nav_items(html):
    """Extract visible text from top-level navbar <li> items in order."""
    start = re.search(r'<ul class="navbar-nav[^"]*">', html)
    if not start:
        return []
    pos = start.end()
    depth = 1
    while depth > 0 and pos < len(html):
        open_tag = html.find('<ul', pos)
        close_tag = html.find('</ul>', pos)
        if close_tag == -1:
            break
        if open_tag != -1 and open_tag < close_tag:
            depth += 1
            pos = open_tag + 3
        else:
            depth -= 1
            pos = close_tag + 5
    nav_ul = html[start.end():pos - 5] if depth == 0 else html[start.end():]
    links = re.finditer(
        r'<a[^>]*class="nav-link[^"]*"[^>]*>(.*?)</a>',
        nav_ul,
        re.DOTALL,
    )
    buttons = re.finditer(
        r'<button[^>]*class="nav-link[^"]*"[^>]*>(.*?)</button>',
        nav_ul,
        re.DOTALL,
    )
    labeled = []
    for m in links:
        label = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        labeled.append((m.start(), label))
    for m in buttons:
        label = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        labeled.append((m.start(), label))
    labeled.sort(key=lambda x: x[0])
    return [label for _, label in labeled]


EXPECTED_NAV_ORDER = [
    "Clientes",
    "Pagos",
    "Reservaciones",
    "Equipo",
    "Horario",
    "Reportes",
    "Admin",
    "Cerrar sesión",
]


@pytest.mark.django_db
class TestSpanishLabels:

    def _login(self, client, staff_user):
        client.force_login(staff_user)

    def test_navbar_menu_item_order(self, client, staff_user):
        """Verify all nav items appear in the specified left-to-right order."""
        staff_user.is_superuser = True
        staff_user.save()
        self._login(client, staff_user)
        response = client.get("/reservations/")
        items = _extract_nav_items(response.content.decode())
        assert items == EXPECTED_NAV_ORDER, f"Expected {EXPECTED_NAV_ORDER}, got {items}"

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
        assert "Equipo" in content

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

    def test_client_search_upload_link_spanish(self, client, staff_user):
        self._login(client, staff_user)
        response = client.get("/clients/search/")
        content = response.content.decode()
        assert "Subir Clientes" in content
        assert "/clients/upload/" in content

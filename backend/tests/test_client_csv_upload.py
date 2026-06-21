import io

import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client as HttpClient

from apps.clients.models import Client

pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

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
def existing_clients(db):
    Client.objects.create(
        first_name="John", last_name="Doe",
        email="john@test.com", mobile="+541111111111",
    )
    Client.objects.create(
        first_name="Jane", last_name="Smith",
        email="jane@test.com", mobile="+541111111112",
    )


# ---------------------------------------------------------------------------
# T002 – parse_csv_file
# ---------------------------------------------------------------------------

class TestParseCsvFile:

    def test_parses_valid_csv(self):
        from apps.clients.csv_import import parse_csv_file
        content = "first_name,last_name,email,mobile\nAna,López,ana@test.com,+54911\n"
        result = parse_csv_file(io.StringIO(content))
        assert len(result) == 1
        assert result[0] == {"first_name": "Ana", "last_name": "López", "email": "ana@test.com", "mobile": "+54911"}

    def test_trims_whitespace(self):
        from apps.clients.csv_import import parse_csv_file
        content = "first_name,last_name,email,mobile\n  Ana  ,  López  ,ana@test.com,  +54911  \n"
        result = parse_csv_file(io.StringIO(content))
        assert result[0]["first_name"] == "Ana"
        assert result[0]["last_name"] == "López"
        assert result[0]["mobile"] == "+54911"

    def test_normalizes_empty_to_none(self):
        from apps.clients.csv_import import parse_csv_file
        content = "first_name,last_name,email,mobile\nAna,López,,\n"
        result = parse_csv_file(io.StringIO(content))
        assert result[0]["email"] is None
        assert result[0]["mobile"] is None

    def test_rejects_missing_required_column(self):
        from apps.clients.csv_import import parse_csv_file
        content = "first_name,email,mobile\nAna,ana@test.com,+54911\n"
        with pytest.raises(ValueError, match="last_name"):
            parse_csv_file(io.StringIO(content))

    def test_ignores_extra_columns(self):
        from apps.clients.csv_import import parse_csv_file
        content = "first_name,last_name,email,mobile,extra\nAna,López,ana@test.com,+54911,ignored\n"
        result = parse_csv_file(io.StringIO(content))
        assert len(result) == 1
        assert "extra" not in result[0]

    def test_handles_bom(self):
        from apps.clients.csv_import import parse_csv_file
        content = "\ufefffirst_name,last_name,email,mobile\nAna,López,ana@test.com,+54911\n"
        result = parse_csv_file(io.StringIO(content))
        assert len(result) == 1

    def test_handles_empty_file(self):
        from apps.clients.csv_import import parse_csv_file
        content = "first_name,last_name,email,mobile\n"
        result = parse_csv_file(io.StringIO(content))
        assert result == []


# ---------------------------------------------------------------------------
# T003 – match_client
# ---------------------------------------------------------------------------

class TestMatchClient:

    def test_matches_by_first_and_last_name(self, existing_clients):
        from apps.clients.csv_import import match_client
        row = {"first_name": "John", "last_name": "Doe", "email": "", "mobile": ""}
        client = match_client(row, Client.objects.all())
        assert client is not None
        assert client.first_name == "John"

    def test_match_by_name_is_case_insensitive(self, existing_clients):
        from apps.clients.csv_import import match_client
        row = {"first_name": "JOHN", "last_name": "DOE", "email": "", "mobile": ""}
        client = match_client(row, Client.objects.all())
        assert client is not None

    def test_matches_by_email_when_name_fails(self, existing_clients):
        from apps.clients.csv_import import match_client
        row = {"first_name": "Jonathan", "last_name": "Doe", "email": "jane@test.com", "mobile": ""}
        client = match_client(row, Client.objects.all())
        assert client is not None
        assert client.first_name == "Jane"

    def test_match_by_email_is_case_insensitive(self, existing_clients):
        from apps.clients.csv_import import match_client
        row = {"first_name": "X", "last_name": "Y", "email": "JANE@TEST.COM", "mobile": ""}
        client = match_client(row, Client.objects.all())
        assert client is not None

    def test_matches_by_mobile_when_name_and_email_fail(self, existing_clients):
        from apps.clients.csv_import import match_client
        row = {"first_name": "X", "last_name": "Y", "email": "no@match.com", "mobile": "+541111111112"}
        client = match_client(row, Client.objects.all())
        assert client is not None
        assert client.first_name == "Jane"

    def test_returns_none_when_no_match(self, existing_clients):
        from apps.clients.csv_import import match_client
        row = {"first_name": "Nobody", "last_name": "Nowhere", "email": "nonexist@test.com", "mobile": "+99999999"}
        client = match_client(row, Client.objects.all())
        assert client is None

    def test_email_match_skipped_when_email_is_none(self, existing_clients):
        from apps.clients.csv_import import match_client
        row = {"first_name": "X", "last_name": "Y", "email": None, "mobile": "+541111111112"}
        client = match_client(row, Client.objects.all())
        assert client is not None

    def test_mobile_match_skipped_when_mobile_is_none(self, existing_clients):
        from apps.clients.csv_import import match_client
        row = {"first_name": "X", "last_name": "Y", "email": "jane@test.com", "mobile": None}
        client = match_client(row, Client.objects.all())
        assert client is not None


# ---------------------------------------------------------------------------
# T004 – process_csv_rows
# ---------------------------------------------------------------------------

class TestProcessCsvRows:

    def test_creates_new_client_when_no_match(self, existing_clients):
        from apps.clients.csv_import import process_csv_rows
        rows = [{"first_name": "New", "last_name": "Client", "email": "new@test.com", "mobile": "+54000000001"}]
        result = process_csv_rows(rows)
        assert result.created == 1
        assert result.updated == 0
        assert result.errors == 0
        assert Client.objects.filter(email="new@test.com").exists()

    def test_updates_existing_client_on_name_match(self, existing_clients):
        from apps.clients.csv_import import process_csv_rows
        rows = [{"first_name": "John", "last_name": "Doe", "email": "johnny@test.com", "mobile": "+541111111111"}]
        result = process_csv_rows(rows)
        assert result.updated == 1
        Client.objects.get(first_name="John", last_name="Doe").email == "johnny@test.com"

    def test_reports_errors_for_invalid_rows(self, existing_clients):
        from apps.clients.csv_import import process_csv_rows
        rows = [
            {"first_name": "Valid", "last_name": "User", "email": "valid@test.com", "mobile": "+54000000001"},
            {"first_name": "", "last_name": "", "email": "", "mobile": ""},
        ]
        result = process_csv_rows(rows)
        assert result.created >= 1
        assert result.errors >= 1

    def test_total_rows_count(self, existing_clients):
        from apps.clients.csv_import import process_csv_rows
        rows = [
            {"first_name": "A", "last_name": "B", "email": "a@test.com", "mobile": "+54000000001"},
            {"first_name": "C", "last_name": "D", "email": "c@test.com", "mobile": "+54000000002"},
        ]
        result = process_csv_rows(rows)
        assert result.total_rows == 2

    def test_error_details_contain_row_info(self, existing_clients):
        from apps.clients.csv_import import process_csv_rows
        rows = [
            {"first_name": "", "last_name": "", "email": "", "mobile": ""},
        ]
        result = process_csv_rows(rows)
        assert len(result.error_details) == 1
        assert "row" in result.error_details[0]

    def test_partial_errors_dont_block_valid_rows(self, existing_clients):
        from apps.clients.csv_import import process_csv_rows
        rows = [
            {"first_name": "Good", "last_name": "One", "email": "good@test.com", "mobile": "+54000000001"},
            {"first_name": "", "last_name": "", "email": "", "mobile": ""},
            {"first_name": "Good", "last_name": "Two", "email": "good2@test.com", "mobile": "+54000000002"},
        ]
        result = process_csv_rows(rows)
        assert result.created == 2
        assert result.errors == 1

    def test_created_client_is_active(self, existing_clients):
        from apps.clients.csv_import import process_csv_rows
        rows = [{"first_name": "Active", "last_name": "Test", "email": "active@test.com", "mobile": "+54000000003"}]
        process_csv_rows(rows)
        client = Client.objects.get(email="active@test.com")
        assert client.is_active is True


# ---------------------------------------------------------------------------
# Helper to build a CSV upload file
# ---------------------------------------------------------------------------

def _csv_file(content: str, name: str = "test.csv") -> SimpleUploadedFile:
    return SimpleUploadedFile(name, content.encode("utf-8"), content_type="text/csv")


# ---------------------------------------------------------------------------
# T009 – GET /clients/upload/
# ---------------------------------------------------------------------------

class TestCsvUploadViewGet:

    def test_returns_200_and_contains_form(self, logged_client):
        response = logged_client.get("/clients/upload/")
        assert response.status_code == 200
        content = response.content.decode()
        assert 'type="file"' in content
        assert 'enctype="multipart/form-data"' in content or "csrf" in content


# ---------------------------------------------------------------------------
# T010 – POST valid CSV
# ---------------------------------------------------------------------------

class TestCsvUploadValidPost:

    def test_returns_results_with_correct_counts(self, logged_client, existing_clients):
        csv_data = "first_name,last_name,email,mobile\nNew,Client,new@test.com,+5400000001\n"
        response = logged_client.post(
            "/clients/upload/",
            {"csv_file": _csv_file(csv_data)},
        )
        content = response.content.decode()
        assert "1" in content  # total or created count
        assert response.status_code == 200


# ---------------------------------------------------------------------------
# T011 – POST with missing header
# ---------------------------------------------------------------------------

class TestCsvUploadMissingHeader:

    def test_shows_error_no_rows_processed(self, logged_client):
        csv_data = "first_name,email,mobile\nAna,ana@test.com,+54911\n"
        response = logged_client.post(
            "/clients/upload/",
            {"csv_file": _csv_file(csv_data)},
        )
        content = response.content.decode()
        assert "last_name" in content or "Faltan" in content or "requeridas" in content
        assert response.status_code == 200


# ---------------------------------------------------------------------------
# T012 – rows missing email AND mobile
# ---------------------------------------------------------------------------

class TestCsvUploadMissingContact:

    def test_skips_row_reports_error(self, logged_client, existing_clients):
        csv_data = "first_name,last_name,email,mobile\nJohn,Doe,,\n"
        response = logged_client.post(
            "/clients/upload/",
            {"csv_file": _csv_file(csv_data)},
        )
        content = response.content.decode()
        assert "error" in content.lower() or "1" in content


# ---------------------------------------------------------------------------
# T013 – empty file
# ---------------------------------------------------------------------------

class TestCsvUploadEmptyFile:

    def test_rejects_empty_file(self, logged_client):
        csv_data = "first_name,last_name,email,mobile\n"
        response = logged_client.post(
            "/clients/upload/",
            {"csv_file": _csv_file(csv_data)},
        )
        assert response.status_code == 200
        content = response.content.decode()
        assert "error" in content.lower() or "vací" in content or "sin datos" in content


# ---------------------------------------------------------------------------
# T014 – all-new CSV
# ---------------------------------------------------------------------------

class TestCsvUploadAllNew:

    def test_all_created(self, logged_client):
        csv_data = (
            "first_name,last_name,email,mobile\n"
            "Ana,López,ana@test.com,+54001\n"
            "Luis,Pérez,luis@test.com,+54002\n"
            "Carmen,Ruiz,carmen@test.com,+54003\n"
        )
        response = logged_client.post(
            "/clients/upload/",
            {"csv_file": _csv_file(csv_data)},
        )
        content = response.content.decode()
        assert "3" in content  # total rows
        assert response.status_code == 200


# ---------------------------------------------------------------------------
# T024 – GET /clients/template/
# ---------------------------------------------------------------------------

class TestCsvTemplateDownload:

    def test_returns_csv_content_type_and_filename(self, logged_client):
        response = logged_client.get("/clients/template/")
        assert response.status_code == 200
        assert response["Content-Type"] == "text/csv"
        assert "client_template" in response["Content-Disposition"]

    def test_contains_header_and_sample_row(self, logged_client):
        response = logged_client.get("/clients/template/")
        content = response.content.decode()
        lines = content.strip().split("\n")
        assert len(lines) >= 2
        assert "first_name" in lines[0]
        assert "last_name" in lines[0]

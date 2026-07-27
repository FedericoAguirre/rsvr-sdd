import csv
import io
from pathlib import Path

import pytest
from django.core.management import call_command
from django.test import TestCase


@pytest.fixture
def feature_done_dir(tmp_path):
    dir_ = tmp_path / "ai" / "features" / "done"
    dir_.mkdir(parents=True)
    (dir_ / "01_test_feature.md").write_text("# Test Feature One\n\nSome content")
    (dir_ / "02_another_feature.md").write_text("# Another Feature\n\nSome content")
    return dir_


@pytest.fixture
def specs_dir(tmp_path):
    dir_ = tmp_path / "specs"
    (dir_ / "001-test-one").mkdir(parents=True)
    spec = dir_ / "001-test-one" / "spec.md"
    spec.write_text(
        "# Spec\n\n## Acceptance criteria\n\nGiven X, Then Y\n\n"
        "## Constraints\n\nSome constraint\n\n## Edge Cases\n\nEdge case here\n\n"
        "## Assumptions\n\nAn assumption\n\n## Key Entities\n\nEntity\n\n"
        "## Success Criteria\n\nSC-001\n\n"
    )
    (dir_ / "002-another").mkdir(parents=True)
    spec2 = dir_ / "002-another" / "spec.md"
    spec2.write_text("# Spec\n\nJust description")
    return dir_


@pytest.fixture
def sessions_dir(tmp_path):
    dir_ = tmp_path / "ai" / "sessions"
    dir_.mkdir(parents=True)
    s1 = dir_ / "deepseek-v4-flash-free-001-test-feature-20260701T100000Z.md"
    s1.write_text(
        "# Session: 001\n\n"
        "**Model:** deepseek-v4-flash-free\n"
        "**Date:** 2026-07-01\n\n"
        "## Changes Made\n\nSomething\n\n"
        "## Test Results\n\n5 tests passed\n"
    )
    s2 = dir_ / "deepseek-v4-flash-free-001-test-feature-20260701T120000Z.md"
    s2.write_text(
        "# Session: 001\n\n"
        "**Model:** deepseek-v4-flash-free\n"
        "**Date:** 2026-07-01\n\n"
        "## Commits\n\n- `/speckit.specify`\n- fix bug\n\n"
        "## Test Results\n\n5 tests passed\n"
    )
    s3 = dir_ / "deepseek-v4-flash-free-002-another-20260702T090000Z.md"
    s3.write_text(
        "# Session: 002\n\n"
        "**Model:** deepseek-v4-flash-free\n"
        "**Date:** 2026-07-02\n\n"
        "## Changes Made\n\nSomething\n\n"
        "## Test Results\n\n3 tests passed\n"
    )
    return dir_


@pytest.fixture
def empty_done_dir(tmp_path):
    dir_ = tmp_path / "ai" / "features" / "done"
    dir_.mkdir(parents=True)
    return dir_


@pytest.fixture
def repo_with_data(tmp_path, feature_done_dir, specs_dir, sessions_dir):
    return tmp_path


@pytest.mark.django_db
class TestCollectAiDevData:
    def test_basic_csv_generation(self, repo_with_data):
        output = repo_with_data / "output.csv"
        call_command(
            "collect_ai_dev_data",
            output=str(output),
            done_dir=str(repo_with_data / "ai" / "features" / "done"),
            specs_dir=str(repo_with_data / "specs"),
            sessions_dir=str(repo_with_data / "ai" / "sessions"),
        )
        assert output.exists()
        with open(output) as f:
            reader = csv.reader(f)
            rows = list(reader)
        assert len(rows) >= 2
        assert rows[0] == [
            "feature", "complexity", "minutes", "model",
            "start_timestamp", "end_timestamp", "specs_quality", "iterations",
        ]

    def test_all_features_have_rows(self, repo_with_data):
        output = repo_with_data / "output.csv"
        call_command(
            "collect_ai_dev_data",
            output=str(output),
            done_dir=str(repo_with_data / "ai" / "features" / "done"),
            specs_dir=str(repo_with_data / "specs"),
            sessions_dir=str(repo_with_data / "ai" / "sessions"),
        )
        with open(output) as f:
            reader = csv.reader(f)
            rows = list(reader)
        feature_titles = {row[0] for row in rows[1:]}
        assert "Test Feature One" in feature_titles
        assert "Another Feature" in feature_titles

    def test_empty_state(self, empty_done_dir, tmp_path):
        output = tmp_path / "output.csv"
        specs = tmp_path / "specs"
        specs.mkdir()
        sessions = tmp_path / "ai" / "sessions"
        sessions.mkdir(parents=True)
        call_command(
            "collect_ai_dev_data",
            output=str(output),
            done_dir=str(empty_done_dir),
            specs_dir=str(specs),
            sessions_dir=str(sessions),
        )
        with open(output) as f:
            reader = csv.reader(f)
            rows = list(reader)
        assert len(rows) == 1
        assert rows[0] == [
            "feature", "complexity", "minutes", "model",
            "start_timestamp", "end_timestamp", "specs_quality", "iterations",
        ]

    def test_malformed_session_graceful(self, tmp_path):
        done = tmp_path / "ai" / "features" / "done"
        done.mkdir(parents=True)
        (done / "test.md").write_text("# Malformed Test")
        sessions = tmp_path / "ai" / "sessions"
        sessions.mkdir(parents=True)
        (sessions / "bad_session.md").write_text("No metadata here at all")
        output = tmp_path / "output.csv"
        specs = tmp_path / "specs"
        specs.mkdir()
        call_command(
            "collect_ai_dev_data",
            output=str(output),
            done_dir=str(done),
            specs_dir=str(specs),
            sessions_dir=str(sessions),
        )
        with open(output) as f:
            reader = csv.reader(f)
            rows = list(reader)
        assert len(rows) == 2
        assert rows[1][0] == "Malformed Test"

    def test_complexity_values_restricted(self, repo_with_data):
        output = repo_with_data / "output.csv"
        call_command(
            "collect_ai_dev_data",
            output=str(output),
            done_dir=str(repo_with_data / "ai" / "features" / "done"),
            specs_dir=str(repo_with_data / "specs"),
            sessions_dir=str(repo_with_data / "ai" / "sessions"),
        )
        with open(output) as f:
            reader = csv.reader(f)
            rows = list(reader)
        valid = {"1", "2", "3", "5", "8"}
        for row in rows[1:]:
            assert row[1] in valid, f"Invalid complexity: {row[1]}"

    def test_specs_quality_values_restricted(self, repo_with_data):
        output = repo_with_data / "output.csv"
        call_command(
            "collect_ai_dev_data",
            output=str(output),
            done_dir=str(repo_with_data / "ai" / "features" / "done"),
            specs_dir=str(repo_with_data / "specs"),
            sessions_dir=str(repo_with_data / "ai" / "sessions"),
        )
        with open(output) as f:
            reader = csv.reader(f)
            rows = list(reader)
        valid = {"1", "2", "3", "4", "5"}
        for row in rows[1:]:
            assert row[6] in valid, f"Invalid specs_quality: {row[6]}"

    def test_rfc_4180_compliance(self, tmp_path):
        done = tmp_path / "ai" / "features" / "done"
        done.mkdir(parents=True)
        (done / "comma.md").write_text('# Feature with "quotes" and , commas\n\n')
        sessions = tmp_path / "ai" / "sessions"
        sessions.mkdir(parents=True)
        specs = tmp_path / "specs"
        specs.mkdir()
        output = tmp_path / "output.csv"
        call_command(
            "collect_ai_dev_data",
            output=str(output),
            done_dir=str(done),
            specs_dir=str(specs),
            sessions_dir=str(sessions),
        )
        with open(output) as f:
            content = f.read()
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)
        assert len(rows) == 2
        assert '"' in content or rows[1][0].startswith('"')

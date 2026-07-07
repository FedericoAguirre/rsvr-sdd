"""Tests for docs/windows11_deployment.md PowerShell commands (static analysis only)."""

import ast
import re
from pathlib import Path

DOCS_PATH = Path(__file__).resolve().parents[2] / "docs" / "windows11_deployment.md"


def _extract_powershell_code_blocks(md_text: str) -> list[str]:
    blocks = re.findall(
        r"```powershell\n(.*?)```", md_text, re.DOTALL
    )
    return blocks


def _parse_env_loader_regex() -> str:
    return r"^[^#].*="


class TestDocContainsPowerShellEnvLoader:
    """Tests that docs contain the expected PowerShell commands."""

    def test_at_least_one_powershell_block_has_setenvironmentvariable(
        self,
    ):
        md = DOCS_PATH.read_text(encoding="utf-8")
        blocks = _extract_powershell_code_blocks(md)
        assert any(
            "SetEnvironmentVariable" in block for block in blocks
        ), (
            "No PowerShell code block in docs/windows11_deployment.md "
            "contains the .env loader (SetEnvironmentVariable). "
            "Expected after updating Option 1/2/3."
        )

    def test_at_least_one_powershell_block_has_uv_run_manage_py(
        self,
    ):
        md = DOCS_PATH.read_text(encoding="utf-8")
        blocks = _extract_powershell_code_blocks(md)
        assert any(
            "uv run" in block and "manage.py" in block for block in blocks
        ), (
            "No PowerShell code block in docs/windows11_deployment.md "
            "contains 'uv run .\\manage.py runserver'. "
            "Expected after updating Option 1/2/3."
        )


class TestEnvLoaderRegexLogic:
    """Tests for the .env parsing regex logic."""

    def test_regex_filters_comment_lines(self):
        lines = [
            "# DATABASE_URL=postgres://should:be@ignored/db",
            "SECRET_KEY=my-secret",
            "",
        ]
        pattern = _parse_env_loader_regex()
        matched = [line for line in lines if re.match(pattern, line)]
        assert len(matched) == 1
        assert matched[0].startswith("SECRET_KEY")

    def test_regex_includes_values_containing_equals(self):
        line = "DATABASE_URL=postgres://user:pass@host:5432/db?sslmode=require"
        assert re.match(_parse_env_loader_regex(), line)

    def test_regex_skips_blank_lines(self):
        assert not re.match(_parse_env_loader_regex(), "")
        assert not re.match(_parse_env_loader_regex(), "   ")


class TestDocValidationNoExecution:
    """Tests that verify no actual execution happens (static analysis only)."""

    def _imported_modules(self) -> set[str]:
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        mods: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    mods.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                mods.add(node.module.split(".")[0])
        return mods

    def _direct_calls(self) -> set[str]:
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        calls: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name):
                    calls.add(f"{node.func.value.id}.{node.func.attr}")
        return calls

    def test_no_subprocess_import(self):
        assert "subprocess" not in self._imported_modules()

    def test_no_os_dot_system_or_popen_call(self):
        calls = self._direct_calls()
        assert "os.system" not in calls
        assert "os.popen" not in calls

    def test_project_root_contains_manage_py(self):
        project_root = Path(__file__).resolve().parents[2]
        manage_py = project_root / "backend" / "manage.py"
        assert manage_py.exists(), (
            f"Expected {manage_py} to exist for path validation"
        )

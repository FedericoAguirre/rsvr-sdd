# Research: Update Restart Docs

## Phase 0 — Findings

### Decision: PowerShell Command Format

**Decision**: Inline `powershell.exe -Command` with the env loader and `uv run` chained via `;` in a single command string.

**Rationale**:
- Task Scheduler's "Start a program" action accepts `powershell.exe` as the program and `-Command "<script>"` as arguments
- The env loader must run in the same process scope as `uv run` so environment variables are available
- Chaining with `;` ensures sequential execution within the same PowerShell session
- No external `.ps1` file needed — keeps the Task Scheduler action self-contained

**Alternatives considered**:
- `.ps1` script file (rejected: adds file management overhead; the script would be short)
- `.bat` wrapper calling PowerShell (rejected: unnecessary indirection)
- Separate env loader script and server command in two Task Scheduler actions (rejected: cannot guarantee same process scope)

### Decision: Test Method Strategy

**Decision**: Static analysis of PowerShell command strings extracted from the documentation markdown file. No execution.

**Rationale**:
- CI does not run on Windows — cannot execute PowerShell commands
- The test validates the documentation stays correct: if someone edits the doc and introduces a syntax error in the PowerShell snippet, the test catches it
- The env loader regex pattern is predictable and parseable

**Alternatives considered**:
- Skipping tests entirely (rejected: FR-007 requires a test method)
- Running PowerShell in a Windows CI runner (rejected: infrastructure overhead for simple syntax checks)

### Decision: All Three Options Updated

**Decision**: All three startup options now use a consistent pattern: load .env via PowerShell, then `uv run .\manage.py runserver`.

**Rationale**:
- Consistency across all recovery scenarios reduces cognitive load
- The feature description originally targeted Option 3 only, but clarifications expanded scope
- Each option still differs in *when/how* it's triggered (manual command vs batch file vs Task Scheduler), but the core commands are identical

### Decision: Security Note

**Decision**: Add a one-paragraph security note about using `icacls` to restrict `.env` file permissions and a warning that Task Scheduler stores the command in plain text.

**Rationale**:
- The `.env` file contains database credentials and Django `SECRET_KEY` — sensitive data
- Task Scheduler tasks are readable by any user with access to the machine
- A simple permission hardening step is low effort and significantly reduces risk

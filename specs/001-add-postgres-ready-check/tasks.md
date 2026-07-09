# Tasks: Add PostgreSQL Readiness Check

## Setup

- [X] Load spec, plan, research, data-model, contracts, quickstart context
- [X] Verify no tasks.md exists — create one

## Core

- [X] **T1**: Modify `backend/start_app01.ps1` — add PostgreSQL readiness check function with TCP socket probe + `pg_isready` fallback, retry loop, exit codes, and status messages per the contract

## Polish

- [X] **T2**: Update `AGENTS.md` session summary if needed
- [X] **T3**: Final review — verify script matches spec, contract, and research decisions

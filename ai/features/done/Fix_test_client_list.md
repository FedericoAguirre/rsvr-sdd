# Spec: Fix Pre-existing Test Failures in test_client_list.py

**Feature Branch**: (none — fix existing tests)

**Created**: 2026-06-13

**Status**: Draft

**Root Cause**: The `0002_seed_test_clients.py` data migration inserts 5 permanent clients (Ana Fernández, Carlos López, Lucía García, María Rodríguez, Pedro Martínez) during test database setup. This shifts pagination offsets and fills the empty state, causing 3 tests in `test_client_list.py` to fail.

## Failed Tests

### 1. `test_all_clients_rendered_when_no_search` (line 39)

**Problem**: Creates 15 "Test" clients (`Test00`–`Test14`), expects first 10 (`Test00`–`Test09`) on page 1. But seed data adds 5 clients that sort before them alphabetically (Ana, Carlos, Lucía, María, Pedro), consuming 5 of the 10 slots per page. Only `Test00`–`Test04` appear on page 1; `Test05`–`Test09` are on page 2.

**Fix options**:
- (A) Create clients with names that sort *before* the seed data (e.g., `"Aaaa"`) to ensure all 15 test clients appear on page 1.
- (B) Delete seed data in test setup or use `reverse` migration.
- (C) Increase page size in test OR test for presence across all pages.

### 2. `test_pagination_21_clients_3_pages` (line 61)

**Problem**: Creates 21 "First" clients (`First00`–`First20`), expects `First00`–`First09` on page 1. Seed data (Ana, Carlos) sort before `First00`, pushing `First08` and `First09` to page 2.

**Fix options**: Same as #1 — adjust names or account for seed data.

### 3. `test_empty_state_when_no_clients` (line 85)

**Problem**: Creates no clients and asserts `"no se encontraron clientes"` appears. But the 5 seed clients are present, so the page renders clients instead of the empty state.

**Fix options**:
- (A) Delete seed clients in test setup (e.g., `Client.objects.all().delete()`).
- (B) Change assertion to verify the empty state message is *not* a required condition for the page — not ideal since the test's purpose is to verify the empty state.
- (C) Accept that an "empty" state cannot occur with seed data and remove/modify the test.

## Recommended Fixes

| Test | Fix | Rationale |
|---|---|---|
| `test_empty_state_when_no_clients` | Delete all clients (`Client.objects.all().delete()`) before assertion | Preserves test intent — verifies empty state rendering |
| `test_all_clients_rendered_when_no_search` | Change names to sort before seed data (e.g., `"Aaaa"` prefix) or loop over all pages | Minimal change preserves pagination coverage |
| `test_pagination_21_clients_3_pages` | Same approach as above | Keep pagination assertions correct with seed data offset |

## Acceptance Criteria

1. All 11 tests in `test_client_list.py` pass when run in isolation with seed migration present.
2. The empty state test still verifies the "no se encontraron clientes" message is rendered when no clients exist.
3. The pagination tests correctly verify 10 items per page accounting for seed data presence.

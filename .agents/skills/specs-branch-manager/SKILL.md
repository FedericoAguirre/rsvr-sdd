---
name: specs-branch-manager
description: Automate the specs branch workflow. Use when the user says "switch to specs branch", "create spec", "update spec", "ready to merge", "done specifying", "ready to implement", or similar phrases about managing the specs branch workflow. Triggers automated git operations: branch switching with main merge, auto-commit/push of spec changes, and squash-merge PR preparation.
---

This skill automates the specs branch development workflow. It handles three distinct phases:

1. **Branch switch** — switch to specs branch with automatic main sync and docker restart
2. **Spec file management** — auto-commit and push spec changes to origin/specs
3. **Merge preparation** — squash commits, prepare PR, and merge to origin/main

## Workflow

### Phase 1: Switch to specs branch

**Trigger**: User says "switch to specs branch", "go to specs", "start working on specs", or similar.

**Steps**:

1. **Stash working changes** — if on a different branch with uncommitted changes, stash them first. Inform the user.
2. **Switch to specs branch** — `git checkout specs`. If it doesn't exist locally, create it from `origin/specs`: `git checkout -b specs origin/specs`.
3. **Sync with main**:
   - `git fetch origin main`
   - `git pull origin main --ff-only` — fast-forward merge from main into specs
4. **Restart Docker**: Run `make restart` (or `docker compose restart`). Wait for the command to complete.
5. **Notify**: Tell the user the specs branch is ready and Docker is up. Example:

   ```
   Switched to specs branch. Main merged (fast-forward). Docker env is up.
   You can check the app at http://localhost:8000 (or your configured port).
   ```

**Edge cases**:
- If `specs` branch doesn't exist locally or on remote: Tell the user and abort.
- If `git pull --ff-only` fails due to conflicts: Inform the user there are merge conflicts that need manual resolution and abort the auto-workflow.
- If Docker is not running: try `make up` instead of restart. If that also fails, warn the user.

### Phase 2: Spec file management

**Trigger**: User creates or updates a spec file (e.g., "create spec for X", "update spec Y", "I finished the spec file", "adding spec for feature Z") OR the user explicitly says "commit specs" or "push specs".

**Steps**:

1. **Detect changes**: Run `git status --short` to find new or modified files. Identify files under `ai/features/todos/` directory.
2. **Classify changes**:
   - New file → `Adds`
   - Modified file → `Updates`
3. **Build commit message**: Format: `[specs] - [Adds|Updates] - [spec_file] with [short_change_description]`
   - `spec_file` is the relative path from repo root (e.g., `ai/features/todos/NNN_new_feature.md`)
   - `short_change_description` is a concise summary of what was added/updated
4. **Stage and commit**: `git add <files> && git commit -m "<formatted message>"`
5. **Push**: `git push origin specs`
6. **Notify**: Tell the user the files were committed and pushed. Example:

   ```
   [specs] - Adds - ai/features/todos/NNN_new_feature.md with export payments feature spec
   Pushed to origin/specs.
   ```

**Multiple files**: If multiple spec files were changed, commit them together with a combined description. Example:

```
[specs] - Adds - ai/features/todos/NN1_new_feature.md, ai/features/todos/NN2_new_feature.md, and ai/features/todos/NN3_new_feature.md with export payments spec and tasks
```

**Edge cases**:
- If no changes detected: Tell the user "No spec changes detected. Nothing to commit."
- If the commit message would be too long (>72 chars for the first line), abbreviate the description.

### Phase 3: Merge preparation

**Trigger**: User says "I'm done with specifying", "ready to merge", "ready to implement", "specs are done", "merge specs", "prepare PR", or similar phrases.

**Steps**:

1. **Ensure on specs branch**: If not on specs, switch to it (with stashing if needed).
2. **Sync with main**: `git fetch origin main && git pull origin main --ff-only`
3. **Squash commits**: Count all commits on specs since the merge-base with main:
   - `merge_base=$(git merge-base specs origin/main)`
   - `git reset --soft $merge_base`
   - `git commit -m "Specs - [summary of all specs changes]"`
4. **Push squashed commit**: `git push origin specs --force`
5. **Prepare PR**: Run `gh pr create` or prepare the PR description:
   - Title: `Specs - [feature name or "Various specs"]`
   - Body: List all spec files included and a brief summary of each
   - Base branch: `main`
6. **Merge to main**: 
   - If using GitHub CLI: `gh pr merge --squash --delete-branch`
   - If merges are done manually: Tell the user the PR is ready at the URL
7. **Switch back to main**: `git checkout main && git pull origin main`
8. **Notify**: Provide PR URL and confirmation.

**Edge cases**:
- If GitHub CLI (`gh`) is not installed: Skip PR creation, guide the user to create it manually at the GitHub URL.
- If there are merge conflicts with main: Inform the user and stop. Do not force-push.

## Quick Reference

| Phase | Trigger Phrase | Key Action |
|-------|----------------|------------|
| 1 | "switch to specs branch", "go to specs" | Checkout specs, pull main, restart docker |
| 2 | "create spec", "update spec", "commit specs" | Auto-commit + push to origin/specs |
| 3 | "ready to merge", "done specifying" | Squash, PR, merge to main |

## Commit Message Format (Phase 2)

```
[specs] - [Adds|Updates] - [spec_file_path] with [short_change_description]
```

## Merge Commit Format (Phase 3)

```
Specs - [summary of all specs changes]
```

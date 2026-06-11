# Security Mitigation Plan — rsvr-sdd

Analysis of Docker and configuration security issues performed on 2026-06-10.

---

## Issues Found

### 🔴 Critical

1. **Hardcoded credentials in `docker-compose.yml:6-18`**
   `POSTGRES_PASSWORD: rsvr` — weak, plaintext default. The same credential appears in `DATABASE_URL`.

2. **`DEBUG: "True"` in `docker-compose.yml:16` (and defaults to `True` in `settings.py:9`)**
   In production, Django debug pages leak stack traces, settings, and internal state.

### 🟠 High

3. **`ALLOWED_HOSTS` defaults to `"*"` in `settings.py:10`**
   Accepts any HTTP Host header, enabling host-header injection attacks.

4. **`SECRET_KEY` fallback is `"dev-secret-key-change-in-production"` in `settings.py:8`**
   If someone deploys without setting the env var, Django's cryptographic signing (sessions, CSRF, password reset tokens) is trivially forgeable.

5. **Container runs as root** — Dockerfile has no `USER` directive. If the app is compromised, the attacker has root inside the container.

### 🟡 Medium

6. **PostgreSQL port exposed to host** (`ports: "5432:5432"`) — database is reachable from outside the Docker network, not just the `web` service.

7. **Source code bind-mounted into container** (`./backend:/app` in `docker-compose.yml:21`) — fine for dev, dangerous for production (live code injection, secrets on host).

8. **Gunicorn exposed directly on `0.0.0.0:8000` without a reverse proxy** — no request buffering, rate limiting, or SSL termination. Gunicorn's docs explicitly recommend putting it behind nginx.

### 🟢 Low

9. **`psycopg2-binary` in `pyproject.toml`** — pre-compiled wheels are not recommended for production; use `psycopg2` instead.

10. **No restart policy or healthcheck on `web` service** — no automatic recovery on crash.

---

## Mitigation Actions

| # | Action | Priority | File(s) |
|---|--------|----------|---------|
| 1 | Replace hardcoded secrets with `${POSTGRES_PASSWORD}` and `${DATABASE_URL}` variables; add `.env.example` with placeholder values | Critical | `docker-compose.yml` |
| 2 | Remove `DEBUG` from compose (default to `False` in settings), or set `DEBUG: "False"` explicitly | Critical | `docker-compose.yml`, `settings.py` |
| 3 | Remove wildcard default — require `ALLOWED_HOSTS` to be explicitly set | High | `settings.py` |
| 4 | Remove insecure default — raise `ImproperlyConfigured` if `SECRET_KEY` is unset | High | `settings.py` |
| 5 | Add `RUN addgroup --system app && adduser --system --ingroup app app` and `USER app` | High | `backend/Dockerfile` |
| 6 | Remove host port mapping for `db` (only expose internally to Docker network) | Medium | `docker-compose.yml` |
| 7 | Remove the bind mount in production profile; separate dev/prod compose files | Medium | `docker-compose.yml` |
| 8 | Add nginx reverse proxy service, switch gunicorn to a unix socket | Medium | `docker-compose.yml`, `backend/Dockerfile` |
| 9 | Replace `psycopg2-binary` with `psycopg2` | Low | `pyproject.toml` |
| 10 | Add `restart: unless-stopped` and `healthcheck` to `web` service | Low | `docker-compose.yml` |

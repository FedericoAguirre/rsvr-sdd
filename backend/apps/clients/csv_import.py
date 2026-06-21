import csv
import io
from dataclasses import dataclass, field

from django.db import IntegrityError

from .models import Client

REQUIRED_COLUMNS = {"first_name", "last_name"}
OPTIONAL_COLUMNS = {"email", "mobile"}
ALL_COLUMNS = REQUIRED_COLUMNS | OPTIONAL_COLUMNS


@dataclass
class ImportResult:
    total_rows: int = 0
    created: int = 0
    updated: int = 0
    errors: int = 0
    error_details: list = field(default_factory=list)


def _cleanse_row(row: dict) -> dict:
    cleaned = {}
    for key in ALL_COLUMNS:
        val = row.get(key, "")
        if isinstance(val, str):
            val = val.strip()
        cleaned[key] = val if val else None
    return cleaned


def parse_csv_file(file: io.TextIOBase) -> list[dict]:
    content = file.read()
    if content.startswith("\ufeff"):
        content = content[1:]
    reader = csv.DictReader(io.StringIO(content))
    if reader.fieldnames is None:
        raise ValueError("El archivo CSV no tiene un encabezado válido.")

    header_lower = {h.strip().lower(): h.strip() for h in reader.fieldnames if h}
    missing = REQUIRED_COLUMNS - set(header_lower.keys())
    if missing:
        raise ValueError(
            "Faltan las columnas requeridas: %s." % ", ".join(sorted(missing))
        )

    rows = []
    for row in reader:
        raw = {}
        for col in ALL_COLUMNS:
            original_key = header_lower.get(col)
            raw[col] = row.get(original_key, "") if original_key else ""
        rows.append(_cleanse_row(raw))
    return rows


def match_client(row: dict, qs) -> Client | None:
    name_match = qs.filter(
        first_name__iexact=row["first_name"],
        last_name__iexact=row["last_name"],
    ).first()
    if name_match:
        return name_match

    if row.get("email"):
        email_match = qs.filter(email__iexact=row["email"]).first()
        if email_match:
            return email_match

    if row.get("mobile"):
        mobile_match = qs.filter(mobile=row["mobile"]).first()
        if mobile_match:
            return mobile_match

    return None


def process_csv_rows(rows: list[dict]) -> ImportResult:
    result = ImportResult(total_rows=len(rows))

    for row in rows:
        if not row.get("first_name") or not row.get("last_name"):
            result.errors += 1
            result.error_details.append(
                {"row": result.total_rows,
                 "message": "first_name y last_name son requeridos."}
            )
            continue

        if not row.get("email") and not row.get("mobile"):
            result.errors += 1
            result.error_details.append(
                {"row": result.total_rows, "message": "Debe proporcionar al menos un email o un móvil."}
            )
            continue

        existing = match_client(row, Client.objects.all())
        if existing:
            existing.first_name = row["first_name"]
            existing.last_name = row["last_name"]
            if row.get("email") is not None:
                existing.email = row["email"]
            if row.get("mobile") is not None:
                existing.mobile = row["mobile"]
            try:
                existing.save()
                result.updated += 1
            except IntegrityError as e:
                result.errors += 1
                result.error_details.append({"row": result.total_rows, "message": str(e)})
        else:
            try:
                Client.objects.create(
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    email=row.get("email"),
                    mobile=row.get("mobile"),
                    is_active=True,
                )
                result.created += 1
            except IntegrityError as e:
                result.errors += 1
                result.error_details.append({"row": result.total_rows, "message": str(e)})

    return result

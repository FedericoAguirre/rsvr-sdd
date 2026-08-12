"""Shared date-window rules for payment batch reservations."""

from dataclasses import dataclass
from datetime import date, time, timedelta
from zoneinfo import ZoneInfo

from django.conf import settings
from django.db.models import Max
from django.utils import timezone

from apps.classes.models import ClassSlot
from apps.reservations.models import Reservation


@dataclass(frozen=True)
class BatchReservationWindow:
    """The first eligible date, end date, and payment-day cutoff."""

    start: date
    end: date
    same_day_cutoff: time | None


def get_batch_reservation_window(payment):
    """Return the eligible date window for a payment's batch reservations."""
    latest = Reservation.objects.filter(client=payment.client).aggregate(
        Max("date")
    )
    candidate = payment.date
    latest_date = latest["date__max"]
    if latest_date is not None:
        candidate = max(candidate, latest_date + timedelta(days=1))

    cutoff = _same_day_cutoff(payment)
    active_weekdays = set(
        ClassSlot.objects.filter(is_active=True).values_list("day_of_week", flat=True)
    )
    if not active_weekdays:
        return BatchReservationWindow(candidate, candidate + timedelta(days=20), cutoff)

    start = candidate
    while True:
        day_cutoff = cutoff if start == payment.date else None
        if start.weekday() in active_weekdays and _has_eligible_slot(start, day_cutoff):
            break
        start += timedelta(days=1)

    return BatchReservationWindow(start, start + timedelta(days=20), cutoff)


def _same_day_cutoff(payment):
    local_created_at = timezone.localtime(
        payment.created_at,
        ZoneInfo(settings.TIME_ZONE),
    )
    if local_created_at.date() == payment.date:
        return local_created_at.time()
    return None


def _has_eligible_slot(day, cutoff):
    slots = ClassSlot.objects.filter(day_of_week=day.weekday(), is_active=True)
    if cutoff is not None:
        slots = slots.filter(time__gt=cutoff)
    return slots.exists()

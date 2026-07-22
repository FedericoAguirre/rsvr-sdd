import datetime
import re
import unicodedata

from django.utils.translation import gettext as _


def snake_case_name(first_name, last_name):
    full = f"{first_name} {last_name}"
    normalized = unicodedata.normalize("NFKD", full)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    lowered = ascii_only.lower().strip()
    return re.sub(r"[^a-z0-9\s]", "", lowered).replace(" ", "_")


def generate_ics(reservations, prodid="-//rsvr-sdd//Class Reservations//ES", extra_fields_fn=None):
    from icalendar import Calendar, Event, Timezone, TimezoneDaylight, TimezoneStandard

    cal = Calendar()
    cal.add("version", "2.0")
    cal.add("prodid", prodid)

    tz = Timezone()
    tz.add("tzid", "America/Denver")
    tz.add("x-lic-location", "America/Denver")

    std = TimezoneStandard()
    std.add("dtstart", datetime.datetime(1970, 11, 1, 2, 0, 0, tzinfo=datetime.timezone.utc))
    std.add("tzoffsetfrom", datetime.timedelta(hours=-6))
    std.add("tzoffsetto", datetime.timedelta(hours=-7))
    std.add("tzname", "MST")
    tz.add_component(std)

    dst = TimezoneDaylight()
    dst.add("dtstart", datetime.datetime(1970, 3, 8, 2, 0, 0, tzinfo=datetime.timezone.utc))
    dst.add("tzoffsetfrom", datetime.timedelta(hours=-7))
    dst.add("tzoffsetto", datetime.timedelta(hours=-6))
    dst.add("tzname", "MDT")
    tz.add_component(dst)

    cal.add_component(tz)

    tzinfo = datetime.timezone(datetime.timedelta(hours=-6))
    for r in reservations:
        event = Event()
        start = datetime.datetime.combine(r.date, r.class_slot.time, tzinfo=tzinfo)
        end = start + datetime.timedelta(hours=1)
        event.add("dtstart", start)
        event.add("dtend", end)
        event.add("summary", str(r.class_slot))
        description = _("Client: %(name)s\nClass: %(slot)s\nDate: %(date)s\nEquipment: %(equipment)s") % {
            "name": str(r.client),
            "slot": str(r.class_slot),
            "date": r.date.isoformat(),
            "equipment": str(r.equipment),
        }
        if extra_fields_fn:
            extra = extra_fields_fn(r)
            if extra:
                for key, value in extra.items():
                    description += f"\n{key}: {value}"
        event.add("description", description)
        cal.add_component(event)

    return cal.to_ical()

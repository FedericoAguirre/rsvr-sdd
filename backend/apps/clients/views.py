import csv
import datetime
import io
import re
import unicodedata

import django.db.models as models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from . import csv_import
from .forms import ClientCsvUploadForm, ClientForm, ClientSearchForm
from .models import Client


@login_required
def client_search(request):
    form = ClientSearchForm(request.GET or None)
    q = ""
    if form.is_valid():
        q = form.cleaned_data.get("q", "")
    filters = models.Q(email__icontains=q) | models.Q(mobile__icontains=q)
    if q and len(q) >= 3:
        filters |= models.Q(first_name__icontains=q) | models.Q(last_name__icontains=q)
    if q:
        clients = Client.objects.filter(filters).order_by("last_name", "first_name")
    else:
        clients = Client.objects.all().order_by("last_name", "first_name")
    paginator = Paginator(clients, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    client_count = Client.objects.count()
    not_found = bool(q) and not page_obj.object_list
    context = {
        "form": form,
        "page_obj": page_obj,
        "results": page_obj.object_list,
        "q": q,
        "client_count": client_count,
        "not_found": not_found,
    }
    if request.headers.get("HX-Request"):
        return render(request, "clients/_search_results.html", context)
    return render(request, "clients/search.html", context)


@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    reservations = client.reservations.select_related("equipment", "class_slot").all()
    return render(request, "clients/client_detail.html", {"client": client, "reservations": reservations})


def _snake_case_name(client):
    full = f"{client.first_name} {client.last_name}"
    normalized = unicodedata.normalize("NFKD", full)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    lowered = ascii_only.lower().strip()
    return re.sub(r"[^a-z0-9\s]", "", lowered).replace(" ", "_")


def _generate_ics(client, reservations, start_date, end_date):
    from icalendar import Calendar, Event, Timezone, TimezoneDaylight, TimezoneStandard

    cal = Calendar()
    cal.add("version", "2.0")
    cal.add("prodid", "-//rsvr-sdd//Class Reservations//ES")

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
        event.add("description", _("Client: %(name)s\nClass: %(slot)s\nDate: %(date)s\nEquipment: %(equipment)s") % {
            "name": str(r.client),
            "slot": str(r.class_slot),
            "date": r.date.isoformat(),
            "equipment": str(r.equipment),
        })
        cal.add_component(event)

    return cal.to_ical()


@login_required
def client_calendar(request, pk):
    client = get_object_or_404(Client, pk=pk)
    start_date_str = request.GET.get("start_date", "")
    end_date_str = request.GET.get("end_date", "")

    if not start_date_str or not end_date_str:
        messages.error(request, _("Please provide both a start date and an end date."))
        return redirect("clients:client-detail", pk=client.pk)

    try:
        start_date = datetime.date.fromisoformat(start_date_str)
        end_date = datetime.date.fromisoformat(end_date_str)
    except ValueError:
        messages.error(request, _("Invalid date format. Use YYYY-MM-DD."))
        return redirect("clients:client-detail", pk=client.pk)

    if start_date > end_date:
        messages.error(request, _("The start date must be before the end date."))
        return redirect("clients:client-detail", pk=client.pk)

    reservations = client.reservations.select_related("equipment", "class_slot").filter(
        date__gte=start_date, date__lte=end_date
    )

    if not reservations.exists():
        messages.info(request, _("No reservations found for the selected date range."))
        return redirect("clients:client-detail", pk=client.pk)

    ics_content = _generate_ics(client, reservations, start_date, end_date)
    snake_name = _snake_case_name(client)
    filename = f"cal_{snake_name}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.ics"

    response = HttpResponse(ics_content, content_type="text/calendar; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


@login_required
def client_create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, _("Client %s created.") % client)
            return redirect("clients:client-detail", pk=client.pk)
    else:
        form = ClientForm()
    return render(request, "clients/client_form.html", {"form": form})


@login_required
def client_csv_upload(request):
    result = None
    if request.method == "POST":
        form = ClientCsvUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["csv_file"]
            if csv_file.size == 0:
                form.add_error("csv_file", _("The file is empty."))
            else:
                try:
                    decoded = csv_file.read().decode("utf-8")
                    rows = csv_import.parse_csv_file(io.StringIO(decoded))
                    if not rows:
                        form.add_error("csv_file", _("The CSV file contains no data rows."))
                    else:
                        result = csv_import.process_csv_rows(rows)
                        messages.success(
                            request,
                            _("Processed %(total)s rows: %(created)s created, %(updated)s updated, %(errors)s errors.")
                            % {"total": result.total_rows, "created": result.created, "updated": result.updated, "errors": result.errors},
                        )
                except UnicodeDecodeError:
                    form.add_error("csv_file", _("Could not decode the file. Please use UTF-8 encoding."))
                except ValueError as e:
                    form.add_error("csv_file", str(e))
    else:
        form = ClientCsvUploadForm()
    return render(request, "clients/client_csv_upload.html", {"form": form, "result": result})


@login_required
def client_csv_template(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="client_template.csv"'
    writer = csv.writer(response)
    writer.writerow(["first_name", "last_name", "email", "mobile"])
    writer.writerow(["Nombre", "Apellido", "ejemplo@correo.com", "+5491123456789"])
    return response

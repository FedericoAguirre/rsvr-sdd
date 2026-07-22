import csv
import datetime
import io

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

from apps.payments.models import PaymentReservation
from utils.ical import generate_ics, snake_case_name


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
    return snake_case_name(client.first_name, client.last_name)


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

    prs = PaymentReservation.objects.filter(
        reservation__in=reservations,
    ).select_related("payment")
    payment_map = {pr.reservation_id: pr.payment.payment_identifier for pr in prs}

    def extra_fields(r):
        payment_id = payment_map.get(r.pk)
        return {"Pago": payment_id or _("Reservación sin asociar")}

    ics_content = generate_ics(reservations, extra_fields_fn=extra_fields)
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

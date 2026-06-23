import json
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext as _

from apps.classes.models import ClassSlot

from .forms import ReservationForm
from .models import Reservation

logger = logging.getLogger(__name__)


def _get_slot_reservations(class_slot_pk, date_str):
    reservations = Reservation.objects.none()
    class_slot = None
    if class_slot_pk and date_str:
        reservations = Reservation.objects.filter(
            class_slot_id=class_slot_pk,
            date=date_str,
        ).select_related("client", "equipment", "class_slot").order_by("equipment__name")
        class_slot = get_object_or_404(ClassSlot, pk=class_slot_pk)
    return reservations, class_slot


@login_required
def reservation_list_pdf(request):
    class_slot_pk = request.GET.get("class_slot")
    date_str = request.GET.get("date", "")
    reservations, class_slot = _get_slot_reservations(class_slot_pk, date_str)
    date_display = date_str.replace("-", "/") if date_str else ""
    try:
        from weasyprint import HTML
        html_string = render_to_string("reservations/reservation_list_pdf.html", {
            "reservations": reservations,
            "class_slot": class_slot,
            "date_str": date_str,
            "date_display": date_display,
        })
        pdf = HTML(string=html_string).write_pdf()
        response = HttpResponse(pdf, content_type="application/pdf")
        safe_name = (
            str(class_slot).replace(" ", "_").translate(
                str.maketrans("", "", "/" + chr(0) + '<>:"|?*')
            ) if class_slot else "unknown"
        )
        date_compact = date_str.replace("-", "") if date_str else "no_date"
        filename = f"reservations_{safe_name}_{date_compact}.pdf"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response
    except Exception as exc:
        logger.exception("PDF generation failed: %s", exc)
        messages.error(request, _("Could not generate the PDF. Please try again."))
        return redirect(request.META.get("HTTP_REFERER", "reservations:reservation-list"))


@login_required
def reservation_list(request):
    date_str = request.GET.get("date", "")
    class_slot_pk = request.GET.get("class_slot", "")
    status_filter = request.GET.get("status", "")
    if class_slot_pk and date_str:
        reservations, class_slot = _get_slot_reservations(class_slot_pk, date_str)
    else:
        reservations = Reservation.objects.select_related("client", "equipment", "class_slot").all()
        if date_str:
            reservations = reservations.filter(date=date_str)
        class_slot = None
    if status_filter:
        reservations = reservations.filter(status=status_filter)
    class_slots = ClassSlot.objects.all()
    today = timezone.localdate()
    date_display = date_str.replace("-", "/") if date_str else ""
    return render(request, "reservations/reservation_list.html", {
        "reservations": reservations,
        "today": today,
        "class_slots": class_slots,
        "class_slot": class_slot,
        "date_str": date_str,
        "date_display": date_display,
        "status_filter": status_filter,
    })


@login_required
def reservation_detail(request, pk):
    reservation = get_object_or_404(
        Reservation.objects.select_related("client", "equipment", "class_slot", "created_by"),
        pk=pk,
    )
    return render(request, "reservations/reservation_detail.html", {"reservation": reservation})


@login_required
def reservation_change_status(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    new_status = request.POST.get("status")
    if new_status is None and request.headers.get("Content-Type") == "application/json":
        try:
            new_status = json.loads(request.body).get("status")
        except (json.JSONDecodeError, AttributeError):
            new_status = None
    valid_statuses = dict(Reservation.STATUS_CHOICES)
    if new_status not in valid_statuses:
        if request.headers.get("HX-Request"):
            return HttpResponse(_("Invalid status."), status=400)
        messages.error(request, _("Invalid status."))
        return redirect("reservations:reservation-detail", pk=reservation.pk)
    reservation.status = new_status
    reservation.save()
    if request.headers.get("HX-Request"):
        response = render(request, "reservations/partials/reservation_row.html", {
            "reservation": reservation,
        })
        response["HX-Trigger"] = "statusChanged"
        return response
    messages.success(request, _("Reservation status updated."))
    return redirect("reservations:reservation-detail", pk=reservation.pk)


@login_required
def reservation_create(request):
    initial = {}
    client_pk = request.GET.get("client")
    if client_pk:
        initial["client"] = client_pk
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.created_by = request.user
            reservation.save()
            messages.success(request, _("Reservation created."))
            return redirect("reservations:reservation-detail", pk=reservation.pk)
    else:
        form = ReservationForm(initial=initial)
    return render(request, "reservations/reservation_form.html", {"form": form})

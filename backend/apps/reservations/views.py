from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext as _
from apps.classes.models import ClassSlot
from .models import Reservation
from .forms import ReservationForm


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
def reservation_list_by_slot(request):
    class_slot_pk = request.GET.get("class_slot")
    date_str = request.GET.get("date", "")
    reservations, class_slot = _get_slot_reservations(class_slot_pk, date_str)
    return render(request, "reservations/reservation_list_by_slot.html", {
        "reservations": reservations,
        "class_slot": class_slot,
        "date_str": date_str,
    })


@login_required
def reservation_list_pdf(request):
    class_slot_pk = request.GET.get("class_slot")
    date_str = request.GET.get("date", "")
    reservations, class_slot = _get_slot_reservations(class_slot_pk, date_str)
    try:
        from weasyprint import HTML
        html_string = render_to_string("reservations/reservation_list_pdf.html", {
            "reservations": reservations,
            "class_slot": class_slot,
            "date_str": date_str,
        })
        pdf = HTML(string=html_string).write_pdf()
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="reservations-{date_str}.pdf"'
        return response
    except Exception:
        messages.error(request, _("Could not generate the PDF. Please try again."))
        return redirect("reservations:reservation-list-by-slot")


@login_required
def reservation_list(request):
    date_str = request.GET.get("date", "")
    client_pk = request.GET.get("client", "")
    reservations = Reservation.objects.select_related("client", "equipment", "class_slot").all()
    if date_str:
        reservations = reservations.filter(date=date_str)
    if client_pk:
        reservations = reservations.filter(client_id=client_pk)
    today = timezone.localdate()
    return render(request, "reservations/reservation_list.html", {
        "reservations": reservations,
        "today": today,
    })


@login_required
def reservation_detail(request, pk):
    reservation = get_object_or_404(
        Reservation.objects.select_related("client", "equipment", "class_slot", "created_by"),
        pk=pk,
    )
    return render(request, "reservations/reservation_detail.html", {"reservation": reservation})


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

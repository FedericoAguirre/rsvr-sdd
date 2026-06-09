from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Reservation
from .forms import ReservationForm


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
            messages.success(request, "Reservation created.")
            return redirect("reservation-detail", pk=reservation.pk)
    else:
        form = ReservationForm(initial=initial)
    return render(request, "reservations/reservation_form.html", {"form": form})

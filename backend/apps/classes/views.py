from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import ClassSlot


@login_required
def class_schedule(request):
    slots = ClassSlot.objects.all().order_by("day_of_week", "time")
    return render(request, "classes/schedule.html", {"slots": slots})


@login_required
def class_toggle(request, pk):
    slot = get_object_or_404(ClassSlot, pk=pk)
    slot.is_active = not slot.is_active
    slot.save()
    status = "activated" if slot.is_active else "deactivated"
    messages.success(request, f"Class slot {slot} {status}.")
    return redirect("class-schedule")

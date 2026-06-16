from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

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
    if slot.is_active:
        messages.success(request, _("Class slot %s activated.") % slot)
    else:
        messages.success(request, _("Class slot %s deactivated.") % slot)
    return redirect("classes:class-schedule")

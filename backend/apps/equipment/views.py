from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Equipment
from .forms import EquipmentForm


@login_required
def equipment_list(request):
    equipments = Equipment.objects.all().order_by("name")
    return render(request, "equipment/equipment_list.html", {"equipments": equipments})


@login_required
def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    return render(request, "equipment/equipment_detail.html", {"equipment": equipment})


@login_required
def equipment_create(request):
    if request.method == "POST":
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Equipment added.")
            return redirect("equipment:equipment-list")
    else:
        form = EquipmentForm()
    return render(request, "equipment/equipment_form.html", {"form": form, "title": "Add Equipment"})


@login_required
def equipment_edit(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == "POST":
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, "Equipment updated.")
            return redirect("equipment:equipment-list")
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, "equipment/equipment_form.html", {"form": form, "title": "Edit Equipment"})

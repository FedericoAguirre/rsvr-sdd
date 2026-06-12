from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Client
from .forms import ClientSearchForm, ClientForm


@login_required
def client_search(request):
    form = ClientSearchForm(request.GET or None)
    results = Client.objects.none()
    q = ""
    if form.is_valid():
        q = form.cleaned_data.get("q", "")
        if q:
            results = Client.objects.filter(
                models.Q(email__icontains=q) | models.Q(mobile__icontains=q)
            )
    return render(request, "clients/search.html", {"form": form, "results": results, "q": q})


@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    reservations = client.reservations.select_related("equipment", "class_slot").all()
    return render(request, "clients/client_detail.html", {"client": client, "reservations": reservations})


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


import django.db.models as models

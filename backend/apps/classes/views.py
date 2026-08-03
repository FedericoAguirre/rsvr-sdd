from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import CreateView, TemplateView

from .forms import ClassPriceForm
from .models import ClassPrice


def is_admin(user):
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name="Administrators").exists()
    )


@login_required
def class_schedule(request):
    from .models import ClassSlot

    slots = ClassSlot.objects.all().order_by("day_of_week", "time")
    return render(request, "classes/schedule.html", {"slots": slots})


@login_required
def class_toggle(request, pk):
    from .models import ClassSlot

    slot = get_object_or_404(ClassSlot, pk=pk)
    slot.is_active = not slot.is_active
    slot.save()
    if slot.is_active:
        messages.success(request, _("Class slot %s activated.") % slot)
    else:
        messages.success(request, _("Class slot %s deactivated.") % slot)
    return redirect("classes:class-schedule")


class ClassPriceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ClassPrice
    form_class = ClassPriceForm
    template_name = "classes/class_price_form.html"

    def test_func(self):
        return is_admin(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_prices"] = ClassPrice.objects.filter(
            current=True,
        ).order_by("-created_at")
        return context

    def form_valid(self, form):
        ClassPrice.objects.enter_price(
            new_price=form.cleaned_data["price"],
            changed_by=self.request.user,
        )
        messages.success(self.request, _("Price updated successfully."))
        return redirect(reverse("classes:price-list"))


class ClassPricesView(LoginRequiredMixin, TemplateView):
    template_name = "classes/class_prices.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        price_history = ClassPrice.objects.all().select_related(
            "created_by",
            "changed_by",
        )
        current_prices = price_history.filter(current=True)
        context["current_prices"] = current_prices
        context["price_history"] = price_history
        context["user_can_add"] = is_admin(self.request.user)
        return context

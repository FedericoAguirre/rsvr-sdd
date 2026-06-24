import json

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from .forms import PaymentForm
from .models import Payment, PaymentReservation


class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = "payments/payment_list.html"
    context_object_name = "payments"
    paginate_by = 5

    def get_queryset(self):
        qs = Payment.objects.filter(is_deleted=False).select_related(
            "client", "created_by",
        )
        client_id = self.request.GET.get("client")
        if client_id:
            qs = qs.filter(client_id=client_id)
        return qs.order_by("-date", "-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client_filter"] = self.request.GET.get("client", "")
        return context


class ClientPaymentHistoryView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = "payments/payment_list.html"
    context_object_name = "payments"
    paginate_by = 5

    def get_queryset(self):
        return Payment.objects.filter(
            client_id=self.kwargs["client_id"], is_deleted=False,
        ).select_related("client", "created_by").order_by("-date", "-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client_filter"] = str(self.kwargs["client_id"])
        return context


class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = "payments/payment_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mode"] = "create"
        context["from_reservation"] = "from_reservation" in self.request.GET
        context["client_id"] = self.request.GET.get("client", "")
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("payments:detail", kwargs={"pk": self.object.pk})


class PaymentDetailView(LoginRequiredMixin, DetailView):
    model = Payment
    template_name = "payments/payment_detail.html"
    context_object_name = "payment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reservations"] = self.object.payment_reservations.select_related(
            "reservation__client", "reservation__equipment", "reservation__class_slot",
        ).all()
        context["remaining_slots"] = (
            self.object.class_slot_count - self.object.payment_reservations.count()
        )
        return context


class PaymentUpdateView(LoginRequiredMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = "payments/payment_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mode"] = "edit"
        return context

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("payments:detail", kwargs={"pk": self.object.pk})


class PaymentDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        payment = get_object_or_404(Payment, pk=kwargs["pk"])
        payment.is_deleted = True
        payment.updated_by = request.user
        payment.save()
        return redirect("payments:list")


class PaymentAssociateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        payment = get_object_or_404(Payment, pk=kwargs["pk"])
        reservation_ids = request.POST.getlist("reservations")
        max_new = payment.class_slot_count - payment.payment_reservations.count()
        if max_new <= 0:
            return redirect("payments:detail", pk=payment.pk)
        with transaction.atomic():
            from apps.reservations.models import Reservation
            for rid in reservation_ids[:max_new]:
                reservation = get_object_or_404(
                    Reservation, pk=rid, client=payment.client,
                )
                PaymentReservation.objects.get_or_create(
                    payment=payment,
                    reservation=reservation,
                )
        return redirect("payments:detail", pk=payment.pk)


class PaymentReportView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "payments/payment_reports.html"

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(
            name="Administrators",
        ).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grouping = self.request.GET.get("grouping", "month")
        start = self.request.GET.get("start", "")
        end = self.request.GET.get("end", "")
        qs = Payment.objects.filter(is_deleted=False)
        if start and end:
            qs = qs.filter(date__gte=start, date__lte=end)
        context["grouping"] = grouping
        context["start_date"] = start
        context["end_date"] = end

        if grouping == "day":
            rows = qs.values("date", "payment_type").annotate(
                total=Sum("amount"), count=Count("id"),
            ).order_by("date", "payment_type")
        elif grouping == "week":
            rows = qs.extra(
                select={"week": "date_trunc('week', date)::date"},
            ).values("week", "payment_type").annotate(
                total=Sum("amount"), count=Count("id"),
            ).order_by("week", "payment_type")
        elif grouping == "range":
            rows = qs.values("date", "payment_type").annotate(
                total=Sum("amount"), count=Count("id"),
            ).order_by("date", "payment_type")
        else:
            rows = qs.values("date__year", "date__month", "payment_type").annotate(
                total=Sum("amount"), count=Count("id"),
            ).order_by("date__year", "date__month", "payment_type")

        context["report_data"] = json.dumps(list(rows), default=str)
        return context

import calendar
import logging
from datetime import date, timedelta

import openpyxl
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.db.models import Count, Q, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from apps.clients.models import Client

from .forms import PaymentForm
from .models import Payment, PaymentReservation

logger = logging.getLogger(__name__)


class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = "payments/payment_list.html"
    context_object_name = "payments"
    paginate_by = 5

    def get_queryset(self):
        qs = Payment.objects.filter(is_deleted=False).select_related(
            "client", "created_by",
        )
        q = self.request.GET.get("q", "").strip()
        if q and len(q) >= 3:
            matching_client_ids = Client.objects.filter(
                is_active=True,
            ).filter(
                Q(first_name__icontains=q)
                | Q(last_name__icontains=q)
                | Q(email__icontains=q)
                | Q(mobile__icontains=q),
            ).values_list("id", flat=True)
            qs = qs.filter(client_id__in=matching_client_ids)
        return qs.order_by("-date", "-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get("q", "")
        context["q"] = q
        page_obj = context.get("page_obj")
        if page_obj is not None:
            context["not_found"] = (
                bool(q) and len(q) >= 3 and page_obj.paginator.count == 0
            )
        else:
            context["not_found"] = False
        context["client_filter"] = q
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("HX-Request"):
            return render(
                self.request,
                "payments/partials/_payment_search_results.html",
                context,
            )
        return super().render_to_response(context, **response_kwargs)


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

    def get_initial(self):
        initial = super().get_initial()
        client_id = self.request.GET.get("client")
        if client_id:
            initial["client"] = client_id
        return initial

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
    def get(self, request, *args, **kwargs):
        payment = get_object_or_404(Payment, pk=kwargs["pk"])
        from apps.reservations.models import Reservation
        associated_ids = payment.payment_reservations.values_list(
            "reservation_id", flat=True,
        )
        available_reservations = Reservation.objects.filter(
            client=payment.client,
        ).exclude(pk__in=associated_ids).select_related(
            "equipment", "class_slot",
        ).order_by("-date", "class_slot__time")
        remaining_slots = (
            payment.class_slot_count - payment.payment_reservations.count()
        )
        return render(
            request,
            "payments/payment_associate.html",
            {
                "payment": payment,
                "available_reservations": available_reservations,
                "remaining_slots": remaining_slots,
            },
        )

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


class PaymentExportView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(
            name="Administrators",
        ).exists()

    def get(self, request, *args, **kwargs):
        try:
            start = request.GET.get("fecha_inicio", "")
            end = request.GET.get("fecha_fin", "")
            if not start or not end:
                return JsonResponse(
                    {"error": str(_("Start date must be before end date."))},
                    status=400,
                )
            try:
                start_dt = date.fromisoformat(start)
                end_dt = date.fromisoformat(end)
            except (ValueError, TypeError):
                return JsonResponse(
                    {"error": str(_("Start date must be before end date."))},
                    status=400,
                )
            if start_dt > end_dt:
                return JsonResponse(
                    {"error": str(_("Start date must be before end date."))},
                    status=400,
                )
            qs = Payment.objects.filter(
                is_deleted=False, date__gte=start_dt, date__lte=end_dt,
            ).select_related("client").order_by("date")
            if not qs.exists():
                return JsonResponse(
                    {"error": str(_("No payments found for the selected date range."))},
                    status=404,
                )
            wb = openpyxl.Workbook(write_only=True)
            ws = wb.create_sheet()
            ws.append(["Identificador", "Cliente", "Monto", "Tipo", "Fecha", "Clases"])
            for p in qs:
                ws.append([
                    p.payment_identifier,
                    str(p.client),
                    float(p.amount),
                    p.payment_type,
                    p.date.isoformat(),
                    p.class_slot_count,
                ])
            start_str = start_dt.strftime("%Y%m%d")
            end_str = end_dt.strftime("%Y%m%d")
            filename = f"pagos_{start_str}_{end_str}.xlsx"
            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            wb.save(response)
            logger.info(
                "Export: user=%s start=%s end=%s count=%d",
                request.user, start, end, qs.count(),
            )
            return response
        except Exception:
            logger.exception("Export failed for user=%s", request.user)
            return JsonResponse(
                {"error": str(_("Could not generate the file. Please try again."))},
                status=500,
            )


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
        if grouping == "week" and start and end:
            try:
                start_dt = date.fromisoformat(start)
                end_dt = date.fromisoformat(end)
                start_dt -= timedelta(days=start_dt.weekday())
                end_dt += timedelta(days=6 - end_dt.weekday())
                start = start_dt.isoformat()
                end = end_dt.isoformat()
            except (ValueError, TypeError):
                pass
        elif grouping == "month" and start and end:
            try:
                start_dt = date.fromisoformat(start)
                end_dt = date.fromisoformat(end)
                start_dt = start_dt.replace(day=1)
                _, last_day = calendar.monthrange(end_dt.year, end_dt.month)
                end_dt = end_dt.replace(day=last_day)
                start = start_dt.isoformat()
                end = end_dt.isoformat()
            except (ValueError, TypeError):
                pass
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
        else:
            rows = qs.values("date__year", "date__month", "payment_type").annotate(
                total=Sum("amount"), count=Count("id"),
            ).order_by("date__year", "date__month", "payment_type")

        context["report_data"] = list(rows)
        return context

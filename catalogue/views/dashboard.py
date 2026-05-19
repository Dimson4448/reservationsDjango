import csv

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import DecimalField, ExpressionWrapper, F, Sum
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from catalogue.models import Representation, RepresentationReservation, Reservation, Review, Show


@staff_member_required
def index(request):
    revenue_expression = ExpressionWrapper(
        F("price") * F("quantity"),
        output_field=DecimalField(max_digits=10, decimal_places=2),
    )
    revenue = RepresentationReservation.objects.aggregate(total=Sum(revenue_expression))["total"] or 0
    now = timezone.now()

    context = {
        "stats": [
            {"label": "Spectacles", "value": Show.objects.count()},
            {"label": "Reservables", "value": Show.objects.filter(bookable=True).count()},
            {"label": "Representations a venir", "value": Representation.objects.filter(schedule__gte=now).count()},
            {
                "label": "Reservations confirmees",
                "value": Reservation.objects.filter(status=Reservation.Status.CONFIRMED).count(),
            },
            {
                "label": "Reservations annulees",
                "value": Reservation.objects.filter(status=Reservation.Status.CANCELED).count(),
            },
            {"label": "Avis en attente", "value": Review.objects.filter(validated=False).count()},
            {"label": "Utilisateurs", "value": User.objects.count()},
            {"label": "Chiffre d'affaires", "value": f"{revenue:.2f} EUR"},
        ],
        "upcoming_representations": (
            Representation.objects.select_related("show", "location")
            .filter(schedule__gte=now)
            .order_by("schedule")[:5]
        ),
        "recent_reservations": (
            Reservation.objects.select_related("user")
            .prefetch_related("representation_reservations__representation__show")
            .order_by("-booking_date")[:5]
        ),
    }
    return render(request, "dashboard/index.html", context)


@staff_member_required
def pending_reviews(request):
    reviews = (
        Review.objects.select_related("user", "show")
        .filter(validated=False)
        .order_by("-created_at", "-id")
    )
    paginator = Paginator(reviews, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "dashboard/reviews.html", {
        "reviews": page_obj,
        "page_obj": page_obj,
        "pagination_query": "",
    })


@staff_member_required
def reservations(request):
    status_filter = request.GET.get("status", "").strip()
    reservations_query = (
        Reservation.objects.select_related("user")
        .prefetch_related("representation_reservations__representation__show")
        .order_by("-booking_date", "-id")
    )
    if status_filter in Reservation.Status.values:
        reservations_query = reservations_query.filter(status=status_filter)

    paginator = Paginator(reservations_query, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "dashboard/reservations.html", {
        "reservations": page_obj,
        "page_obj": page_obj,
        "status_filter": status_filter,
        "statuses": Reservation.Status,
        "pagination_query": f"status={status_filter}",
    })


@staff_member_required
@require_POST
def update_reservation_status(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    status = request.POST.get("status", "")

    if status not in Reservation.Status.values:
        messages.error(request, "Statut invalide.")
        return redirect("catalogue:dashboard-reservations")

    reservation.status = status
    reservation.save(update_fields=["status"])
    messages.success(request, "Statut de la reservation mis a jour.")
    return redirect("catalogue:dashboard-reservations")


@staff_member_required
@require_POST
def validate_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, validated=False)
    review.validated = True
    review.updated_at = timezone.now()
    review.save(update_fields=["validated", "updated_at"])
    messages.success(request, "Avis valide.")
    return redirect("catalogue:dashboard-reviews")


@staff_member_required
def export_reservations(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="reservations.csv"'

    writer = csv.writer(response)
    writer.writerow(["reference", "client", "email", "statut", "date", "spectacle", "quantite", "prix", "total"])

    reservation_items = (
        RepresentationReservation.objects.select_related(
            "reservation__user",
            "representation__show",
        )
        .order_by("-reservation__booking_date", "reservation_id")
    )
    for item in reservation_items:
        reservation = item.reservation
        writer.writerow(
            [
                reservation.id,
                reservation.user.username,
                reservation.user.email,
                reservation.get_status_display(),
                timezone.localtime(reservation.booking_date).strftime("%d/%m/%Y %H:%M"),
                item.representation.show.title,
                item.quantity,
                f"{item.price:.2f}",
                f"{item.line_total:.2f}",
            ]
        )

    return response

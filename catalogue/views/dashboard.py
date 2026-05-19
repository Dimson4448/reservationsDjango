import csv

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import DecimalField, ExpressionWrapper, F, Sum
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

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

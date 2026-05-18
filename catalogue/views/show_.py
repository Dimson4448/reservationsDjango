from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalogue.forms import ReservationForm
from catalogue.models import Representation, RepresentationReservation, Reservation, Show


def index(request):
    shows = Show.objects.select_related("location").prefetch_related("representations").all()
    return render(request, "show/index.html", {
        "shows": shows,
        "title": "Liste des spectacles",
    })


def show(request, show_id):
    show = get_object_or_404(
        Show.objects.select_related("location").prefetch_related(
            "representations",
            "prices",
            "reviews",
        ),
        id=show_id,
    )
    return render(request, "show/show.html", {
        "show": show,
        "title": "Fiche d'un spectacle",
    })


@login_required
def reserve(request, representation_id):
    representation = get_object_or_404(
        Representation.objects.select_related("show", "location"),
        id=representation_id,
        show__bookable=True,
    )
    form = ReservationForm(request.POST or None, representation=representation)

    if request.method == "POST" and form.is_valid():
        price_show = form.cleaned_data["price_show"]
        quantity = form.cleaned_data["quantity"]

        with transaction.atomic():
            reservation = Reservation.objects.create(
                user=request.user,
                status=Reservation.Status.CONFIRMED,
            )
            RepresentationReservation.objects.create(
                representation=representation,
                reservation=reservation,
                price=price_show.price.price,
                quantity=quantity,
            )

        messages.success(request, "Reservation confirmee.")
        return redirect("accounts:user-profile")

    return render(request, "reservation/create.html", {
        "form": form,
        "representation": representation,
    })


@login_required
@require_POST
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        user=request.user,
    )

    if reservation.status == Reservation.Status.CANCELED:
        messages.info(request, "Cette reservation est deja annulee.")
        return redirect("accounts:user-profile")

    reservation.status = Reservation.Status.CANCELED
    reservation.save(update_fields=["status"])
    messages.success(request, "Reservation annulee.")
    return redirect("accounts:user-profile")

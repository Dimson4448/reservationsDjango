from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Min, Prefetch, Q
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from catalogue.forms import ReservationForm, ReviewForm
from catalogue.models import Representation, RepresentationReservation, Reservation, Show


def index(request):
    query = request.GET.get("q", "").strip()
    availability = request.GET.get("availability", "").strip()
    shows = Show.objects.select_related("location").prefetch_related("representations").all()

    if query:
        shows = shows.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(location__designation__icontains=query)
        )

    if availability == "bookable":
        shows = shows.filter(bookable=True)
    elif availability == "unavailable":
        shows = shows.filter(bookable=False)

    return render(request, "show/index.html", {
        "shows": shows,
        "title": "Liste des spectacles",
        "query": query,
        "availability": availability,
    })


def show(request, show_id):
    show = get_object_or_404(
        Show.objects.select_related("location").prefetch_related(
            Prefetch(
                "representations",
                queryset=Representation.objects.select_related("location").order_by("schedule"),
            ),
            "prices",
            "reviews",
        ).annotate(min_price=Min("price_links__price__price")),
        id=show_id,
    )
    return render(request, "show/show.html", {
        "show": show,
        "title": "Fiche d'un spectacle",
        "review_form": ReviewForm(),
        "validated_reviews": show.reviews.filter(validated=True).select_related("user"),
    })


@login_required
@require_POST
def add_review(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    form = ReviewForm(request.POST)

    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.show = show
        review.validated = False
        review.save()
        messages.success(request, "Votre avis a ete envoye et attend validation.")
        return redirect("catalogue:show-show", show_id=show.id)

    messages.error(request, "Votre avis n'a pas pu etre enregistre.")
    validated_reviews = show.reviews.filter(validated=True).select_related("user")
    return render(request, "show/show.html", {
        "show": show,
        "title": "Fiche d'un spectacle",
        "review_form": form,
        "validated_reviews": validated_reviews,
    })


@login_required
def reserve(request, representation_id):
    representation = get_object_or_404(
        Representation.objects.select_related("show", "location"),
        id=representation_id,
        show__bookable=True,
        schedule__gte=timezone.now(),
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

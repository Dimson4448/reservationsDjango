from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import transaction
from django.db.models import Min, Prefetch, Q
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from catalogue.forms import ReservationForm, ReviewForm
from catalogue.models import Representation, RepresentationReservation, Reservation, Show


def _session_value(session, key, default=None):
    if isinstance(session, dict):
        return session.get(key, default)
    return getattr(session, key, default)


def configured_payment_methods():
    labels = {
        "card": "Carte bancaire",
        "bancontact": "Bancontact",
        "klarna": "Klarna",
    }
    return [
        {"value": method, "label": labels.get(method, method.title())}
        for method in settings.STRIPE_PAYMENT_METHOD_TYPES
    ]


def index(request):
    query = request.GET.get("q", "").strip()
    availability = request.GET.get("availability", "").strip()
    shows = (
        Show.objects
        .select_related("location")
        .prefetch_related("representations")
        .order_by("title", "id")
    )

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

    paginator = Paginator(shows, 6)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "show/index.html", {
        "shows": page_obj,
        "page_obj": page_obj,
        "title": "Liste des spectacles",
        "query": query,
        "availability": availability,
        "pagination_query": f"q={query}&availability={availability}",
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
                status=Reservation.Status.PENDING,
                payment_status=Reservation.PaymentStatus.UNPAID,
            )
            RepresentationReservation.objects.create(
                representation=representation,
                reservation=reservation,
                price=price_show.price.price,
                quantity=quantity,
            )

        messages.success(request, "Reservation ajoutee au panier. Le billet sera disponible apres paiement.")
        return redirect("catalogue:reservation-cart", reservation_id=reservation.id)

    return render(request, "reservation/create.html", {
        "form": form,
        "representation": representation,
    })


@login_required
def reservation_cart(request, reservation_id):
    reservation = get_object_or_404(
        Reservation.objects.prefetch_related(
            "representation_reservations__representation__show",
            "representation_reservations__representation__location",
        ),
        id=reservation_id,
        user=request.user,
    )
    if reservation.is_paid:
        return redirect("catalogue:reservation-confirmation", reservation_id=reservation.id)

    return render(request, "reservation/cart.html", {
        "reservation": reservation,
        "stripe_configured": bool(settings.STRIPE_SECRET_KEY),
        "payment_methods": configured_payment_methods(),
    })


@login_required
@require_POST
def start_payment(request, reservation_id):
    reservation = get_object_or_404(
        Reservation.objects.prefetch_related("representation_reservations__representation__show"),
        id=reservation_id,
        user=request.user,
        status=Reservation.Status.PENDING,
        payment_status=Reservation.PaymentStatus.UNPAID,
    )
    if not settings.STRIPE_SECRET_KEY:
        messages.error(request, "Le paiement en ligne n'est pas encore configure.")
        return redirect("catalogue:reservation-cart", reservation_id=reservation.id)

    try:
        import stripe
    except ImportError:
        messages.error(request, "Le module Stripe n'est pas installe.")
        return redirect("catalogue:reservation-cart", reservation_id=reservation.id)

    selected_method = request.POST.get("payment_method", "").strip()
    payment_methods = (
        [selected_method]
        if selected_method in settings.STRIPE_PAYMENT_METHOD_TYPES
        else settings.STRIPE_PAYMENT_METHOD_TYPES
    )
    stripe.api_key = settings.STRIPE_SECRET_KEY

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=payment_methods,
        customer_email=request.user.email or None,
        line_items=[
            {
                "price_data": {
                    "currency": settings.STRIPE_CURRENCY,
                    "product_data": {
                        "name": f"Reservation Ultimate SPT #{reservation.id}",
                    },
                    "unit_amount": int(reservation.total_amount * 100),
                },
                "quantity": 1,
            }
        ],
        metadata={"reservation_id": reservation.id},
        success_url=request.build_absolute_uri(
            reverse("catalogue:reservation-payment-success", args=[reservation.id])
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(
            reverse("catalogue:reservation-cart", args=[reservation.id])
        ),
    )
    reservation.payment_reference = session.id
    reservation.payment_method = ",".join(payment_methods)
    reservation.save(update_fields=["payment_reference", "payment_method"])
    return redirect(session.url)


@login_required
def payment_success(request, reservation_id):
    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        user=request.user,
        status=Reservation.Status.PENDING,
    )
    session_id = request.GET.get("session_id", "")
    if not settings.STRIPE_SECRET_KEY or not session_id:
        messages.error(request, "Paiement impossible a verifier.")
        return redirect("catalogue:reservation-cart", reservation_id=reservation.id)

    try:
        import stripe
    except ImportError:
        messages.error(request, "Le module Stripe n'est pas installe.")
        return redirect("catalogue:reservation-cart", reservation_id=reservation.id)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    if session.payment_status != "paid":
        messages.error(request, "Le paiement n'est pas encore confirme.")
        return redirect("catalogue:reservation-cart", reservation_id=reservation.id)

    reservation.mark_paid(
        payment_reference=session.id,
        payment_method=getattr(session, "payment_method_types", ["stripe"])[0],
    )
    messages.success(request, "Paiement confirme. Votre billet est disponible.")
    return redirect("catalogue:reservation-confirmation", reservation_id=reservation.id)


@csrf_exempt
@require_POST
def stripe_webhook(request):
    if not settings.STRIPE_WEBHOOK_SECRET:
        return HttpResponse("Stripe webhook non configure.", status=503)

    try:
        import stripe
    except ImportError:
        return HttpResponse("Stripe non installe.", status=503)

    payload = request.body
    signature = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    try:
        event = stripe.Webhook.construct_event(
            payload,
            signature,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event.get("type") == "checkout.session.completed":
        session = event["data"]["object"]
        metadata = _session_value(session, "metadata", {}) or {}
        reservation_id = metadata.get("reservation_id")
        payment_status = _session_value(session, "payment_status")
        if reservation_id and payment_status == "paid":
            reservation = Reservation.objects.filter(
                id=reservation_id,
                status=Reservation.Status.PENDING,
            ).first()
            if reservation:
                payment_methods = _session_value(session, "payment_method_types", ["stripe"])
                reservation.mark_paid(
                    payment_reference=_session_value(session, "id", ""),
                    payment_method=payment_methods[0] if payment_methods else "stripe",
                )

    return JsonResponse({"received": True})


@login_required
def reservation_confirmation(request, reservation_id):
    reservation = get_object_or_404(
        Reservation.objects.prefetch_related(
            "representation_reservations__representation__show",
            "representation_reservations__representation__location",
        ),
        id=reservation_id,
        user=request.user,
    )
    if not reservation.is_paid:
        messages.info(request, "Le paiement est requis avant la confirmation finale.")
        return redirect("catalogue:reservation-cart", reservation_id=reservation.id)

    return render(request, "reservation/confirmation.html", {
        "reservation": reservation,
    })


@login_required
def reservation_ticket(request, reservation_id):
    reservation = get_object_or_404(
        Reservation.objects.prefetch_related(
            "representation_reservations__representation__show",
            "representation_reservations__representation__location",
        ),
        id=reservation_id,
        user=request.user,
        status=Reservation.Status.CONFIRMED,
        payment_status=Reservation.PaymentStatus.PAID,
    )
    return render(request, "reservation/ticket.html", {
        "reservation": reservation,
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
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({
                "status": reservation.status,
                "status_label": reservation.get_status_display(),
                "message": "Cette reservation est deja annulee.",
            })
        messages.info(request, "Cette reservation est deja annulee.")
        return redirect("accounts:user-profile")

    reservation.status = Reservation.Status.CANCELED
    reservation.save(update_fields=["status"])

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "status": reservation.status,
            "status_label": reservation.get_status_display(),
            "message": "Reservation annulee.",
        })

    messages.success(request, "Reservation annulee.")
    return redirect("accounts:user-profile")

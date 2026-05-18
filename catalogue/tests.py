from datetime import timedelta
from decimal import Decimal

from django.contrib import admin
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.test import SimpleTestCase, TestCase
from django.utils import timezone
from django.urls import reverse, resolve

from catalogue.models import (
    Artist,
    Locality,
    Location,
    Price,
    PriceShow,
    Representation,
    RepresentationReservation,
    Reservation,
    Review,
    Show,
)
from catalogue.admin import ReservationAdmin, ReviewAdmin, ShowAdmin
from catalogue.views import artist, show_


class CatalogueRoutingTests(SimpleTestCase):
    def test_show_routes_are_registered(self):
        self.assertEqual(resolve(reverse("catalogue:show-index")).func, show_.index)
        self.assertEqual(resolve(reverse("catalogue:show-show", args=[1])).func, show_.show)

    def test_reservation_route_is_registered(self):
        url = reverse("catalogue:reservation-create", args=[1])
        self.assertEqual(resolve(url).func, show_.reserve)

    def test_reservation_cancel_route_is_registered(self):
        url = reverse("catalogue:reservation-cancel", args=[1])
        self.assertEqual(resolve(url).func, show_.cancel_reservation)

    def test_review_create_route_is_registered(self):
        url = reverse("catalogue:show-review-create", args=[1])
        self.assertEqual(resolve(url).func, show_.add_review)

    def test_artist_routes_are_registered(self):
        self.assertEqual(resolve(reverse("catalogue:artist-index")).func, artist.index)
        self.assertEqual(resolve(reverse("catalogue:artist-show", args=[1])).func, artist.show)


class CatalogueTemplateTests(SimpleTestCase):
    def test_main_templates_compile(self):
        templates = [
            "home.html",
            "layouts/base.html",
            "artist/index.html",
            "artist/show.html",
            "show/index.html",
            "show/show.html",
            "reservation/create.html",
        ]
        for template_name in templates:
            with self.subTest(template=template_name):
                self.assertIsNotNone(get_template(template_name))


class CatalogueAdminTests(SimpleTestCase):
    def test_key_models_use_custom_admin_classes(self):
        self.assertIsInstance(admin.site._registry[Show], ShowAdmin)
        self.assertIsInstance(admin.site._registry[Reservation], ReservationAdmin)
        self.assertIsInstance(admin.site._registry[Review], ReviewAdmin)


class ReservationFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="client",
            email="client@example.com",
            password="pass12345",
        )
        self.locality = Locality.objects.create(postal_code="1000", locality="Bruxelles")
        self.location = Location.objects.create(
            slug="theatre-test",
            designation="Theatre Test",
            address="Rue Test 1",
            locality=self.locality,
            website="https://example.com",
        )
        self.show = Show.objects.create(
            slug="spectacle-test",
            title="Spectacle Test",
            description="Description test",
            duration=90,
            created_in=2026,
            location=self.location,
            bookable=True,
        )
        self.price = Price.objects.create(
            type="Standard",
            price=Decimal("25.00"),
            description="Tarif standard",
            end_date=timezone.localdate() + timedelta(days=30),
        )
        self.price_show = PriceShow.objects.create(show=self.show, price=self.price)
        self.representation = Representation.objects.create(
            show=self.show,
            location=self.location,
            schedule=timezone.now() + timedelta(days=5),
        )

    def test_authenticated_user_can_create_reservation(self):
        self.client.login(username="client", password="pass12345")

        response = self.client.post(
            reverse("catalogue:reservation-create", args=[self.representation.id]),
            {
                "representation": self.representation.id,
                "price_show": self.price_show.id,
                "quantity": 2,
            },
        )

        self.assertRedirects(response, reverse("accounts:user-profile"))
        reservation = Reservation.objects.get(user=self.user)
        self.assertEqual(reservation.status, Reservation.Status.CONFIRMED)
        item = reservation.representation_reservations.get()
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.line_total, self.price.price * 2)

    def test_user_can_cancel_own_reservation(self):
        reservation = Reservation.objects.create(user=self.user)
        RepresentationReservation.objects.create(
            reservation=reservation,
            representation=self.representation,
            price=self.price.price,
            quantity=1,
        )
        self.client.login(username="client", password="pass12345")

        response = self.client.post(reverse("catalogue:reservation-cancel", args=[reservation.id]))

        self.assertRedirects(response, reverse("accounts:user-profile"))
        reservation.refresh_from_db()
        self.assertEqual(reservation.status, Reservation.Status.CANCELED)

    def test_user_can_cancel_own_reservation_with_ajax(self):
        reservation = Reservation.objects.create(user=self.user)
        RepresentationReservation.objects.create(
            reservation=reservation,
            representation=self.representation,
            price=self.price.price,
            quantity=1,
        )
        self.client.login(username="client", password="pass12345")

        response = self.client.post(
            reverse("catalogue:reservation-cancel", args=[reservation.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], Reservation.Status.CANCELED)
        reservation.refresh_from_db()
        self.assertEqual(reservation.status, Reservation.Status.CANCELED)


class ShowCatalogueTests(TestCase):
    def setUp(self):
        self.locality = Locality.objects.create(postal_code="1000", locality="Bruxelles")
        self.location = Location.objects.create(
            slug="catalogue-theatre",
            designation="Theatre Catalogue",
            address="Rue Catalogue 1",
            locality=self.locality,
            website="https://catalogue.example.com",
        )
        self.bookable_show = Show.objects.create(
            slug="bruxelles-comedie",
            title="Bruxelles Comedie",
            description="Spectacle comique belge",
            duration=80,
            created_in=2026,
            location=self.location,
            bookable=True,
        )
        self.unavailable_show = Show.objects.create(
            slug="archive-drama",
            title="Archive Drama",
            description="Ancien spectacle",
            duration=60,
            created_in=2025,
            location=self.location,
            bookable=False,
        )
        self.price = Price.objects.create(
            type="Catalogue Standard",
            price=Decimal("19.50"),
            description="Tarif catalogue",
            end_date=timezone.localdate() + timedelta(days=30),
        )
        PriceShow.objects.create(show=self.bookable_show, price=self.price)
        self.representation = Representation.objects.create(
            show=self.bookable_show,
            location=self.location,
            schedule=timezone.now() + timedelta(days=10),
        )

    def test_show_index_can_search_by_title(self):
        response = self.client.get(reverse("catalogue:show-index"), {"q": "comedie"})

        self.assertContains(response, self.bookable_show.title)
        self.assertNotContains(response, self.unavailable_show.title)

    def test_show_index_can_filter_bookable_shows(self):
        response = self.client.get(reverse("catalogue:show-index"), {"availability": "bookable"})

        self.assertContains(response, self.bookable_show.title)
        self.assertNotContains(response, self.unavailable_show.title)

    def test_show_detail_displays_booking_summary(self):
        response = self.client.get(reverse("catalogue:show-show", args=[self.bookable_show.id]))

        self.assertContains(response, "A partir de")
        self.assertContains(response, "19.50")
        self.assertContains(response, "Reservable")
        self.assertContains(response, self.location.designation)

    def test_past_representation_is_not_bookable(self):
        past_representation = Representation.objects.create(
            show=self.bookable_show,
            location=self.location,
            schedule=timezone.now() - timedelta(days=1),
        )

        self.assertFalse(past_representation.is_bookable)

    def test_past_representation_reservation_page_returns_404(self):
        past_representation = Representation.objects.create(
            show=self.bookable_show,
            location=self.location,
            schedule=timezone.now() - timedelta(days=1),
        )
        user = User.objects.create_user(username="past-client", password="pass12345")
        self.client.login(username="past-client", password="pass12345")

        response = self.client.get(reverse("catalogue:reservation-create", args=[past_representation.id]))

        self.assertEqual(response.status_code, 404)

    def test_show_detail_displays_only_validated_reviews(self):
        user = User.objects.create_user(username="viewer", password="pass12345")
        Review.objects.create(
            user=user,
            show=self.bookable_show,
            review="Tres bon spectacle",
            stars=5,
            validated=True,
        )
        Review.objects.create(
            user=user,
            show=self.bookable_show,
            review="Avis en attente",
            stars=3,
            validated=False,
        )

        response = self.client.get(reverse("catalogue:show-show", args=[self.bookable_show.id]))

        self.assertContains(response, "Tres bon spectacle")
        self.assertNotContains(response, "Avis en attente")

    def test_authenticated_user_can_submit_review(self):
        user = User.objects.create_user(username="reviewer", password="pass12345")
        self.client.login(username="reviewer", password="pass12345")

        response = self.client.post(
            reverse("catalogue:show-review-create", args=[self.bookable_show.id]),
            {
                "stars": 4,
                "review": "Bonne experience",
            },
        )

        self.assertRedirects(response, reverse("catalogue:show-show", args=[self.bookable_show.id]))
        review = Review.objects.get(user=user, show=self.bookable_show)
        self.assertEqual(review.stars, 4)
        self.assertFalse(review.validated)


class ArtistCatalogueTests(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(firstname="Claude", lastname="Semal")
        self.other_artist = Artist.objects.create(firstname="Daniel", lastname="Marcelin")

    def test_artist_index_can_search_by_firstname(self):
        response = self.client.get(reverse("catalogue:artist-index"), {"q": "claude"})

        self.assertContains(response, self.artist.lastname)
        self.assertNotContains(response, self.other_artist.lastname)

    def test_artist_index_can_search_by_lastname(self):
        response = self.client.get(reverse("catalogue:artist-index"), {"q": "marcelin"})

        self.assertContains(response, self.other_artist.lastname)
        self.assertNotContains(response, self.artist.lastname)

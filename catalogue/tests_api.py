from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from catalogue.models import (
    Artist,
    Locality,
    Location,
    Price,
    PriceShow,
    Representation,
    Reservation,
    Review,
    Show,
)


class ArtistAPITests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="bob", password="illusion4468")
        self.client.force_authenticate(user=self.user)

    def test_create_artist(self):
        data = {"firstname": "John", "lastname": "Doe"}
        response = self.client.post("/catalogue/api/artists/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_artist_list(self):
        Artist.objects.create(firstname="Jane", lastname="Smith")
        response = self.client.get("/catalogue/api/artists/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CatalogueAPITests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="client-api", password="pass12345")
        self.locality = Locality.objects.create(postal_code="1000", locality="Bruxelles")
        self.location = Location.objects.create(
            slug="api-theatre",
            designation="API Theatre",
            address="Rue API 1",
            locality=self.locality,
            website="https://api.example.com",
        )
        self.show = Show.objects.create(
            slug="api-show",
            title="API Show",
            description="Spectacle expose par API",
            duration=75,
            created_in=2026,
            location=self.location,
            bookable=True,
        )
        self.price = Price.objects.create(
            type="API Standard",
            price=Decimal("18.00"),
            description="Tarif API",
            end_date=timezone.localdate() + timedelta(days=30),
        )
        self.price_show = PriceShow.objects.create(show=self.show, price=self.price)
        self.representation = Representation.objects.create(
            show=self.show,
            location=self.location,
            schedule=timezone.now() + timedelta(days=7),
        )

    def test_show_list_is_public(self):
        Review.objects.create(
            user=self.user,
            show=self.show,
            stars=5,
            review="Avis public",
            validated=True,
        )
        Review.objects.create(
            user=self.user,
            show=self.show,
            stars=2,
            review="Avis cache",
            validated=False,
        )

        response = self.client.get("/catalogue/api/shows/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "API Show")
        self.assertEqual(response.data[0]["prices"][0]["type"], "API Standard")
        self.assertEqual(response.data[0]["reviews"][0]["review"], "Avis public")
        self.assertEqual(len(response.data[0]["reviews"]), 1)

    def test_representation_list_is_public(self):
        response = self.client.get("/catalogue/api/representations/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["show_title"], "API Show")
        self.assertTrue(response.data[0]["is_bookable"])

    def test_authenticated_user_can_create_api_reservation(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            "/catalogue/api/reservations/",
            {
                "representation_id": self.representation.id,
                "price_show_id": self.price_show.id,
                "quantity": 3,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], Reservation.Status.PENDING)
        self.assertEqual(response.data["payment_status"], Reservation.PaymentStatus.UNPAID)
        self.assertEqual(response.data["items"][0]["quantity"], 3)
        self.assertIn("/catalogue/reservation/", response.data["cart_url"])
        self.assertTrue(response.data["cart_url"].endswith("/cart"))
        self.assertIn("/catalogue/reservation/", response.data["confirmation_url"])
        self.assertTrue(response.data["confirmation_url"].endswith("/confirmation"))

    def test_authenticated_user_can_cancel_api_reservation(self):
        self.client.force_authenticate(user=self.user)
        create_response = self.client.post(
            "/catalogue/api/reservations/",
            {
                "representation_id": self.representation.id,
                "price_show_id": self.price_show.id,
                "quantity": 1,
            },
            format="json",
        )
        reservation_id = create_response.data["id"]

        response = self.client.post(f"/catalogue/api/reservations/{reservation_id}/cancel/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], Reservation.Status.CANCELED)

    def test_authenticated_user_can_submit_api_review(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            f"/catalogue/api/shows/{self.show.id}/reviews/",
            {
                "stars": 4,
                "review": "Avis API",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["review"], "Avis API")
        review = Review.objects.get(review="Avis API")
        self.assertFalse(review.validated)

    def test_api_cannot_reserve_past_representation(self):
        past_representation = Representation.objects.create(
            show=self.show,
            location=self.location,
            schedule=timezone.now() - timedelta(days=1),
        )
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            "/catalogue/api/reservations/",
            {
                "representation_id": past_representation.id,
                "price_show_id": self.price_show.id,
                "quantity": 1,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

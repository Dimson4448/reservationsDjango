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
        response = self.client.get("/catalogue/api/shows/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "API Show")
        self.assertEqual(response.data[0]["prices"][0]["type"], "API Standard")

    def test_representation_list_is_public(self):
        response = self.client.get("/catalogue/api/representations/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["show_title"], "API Show")

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
        self.assertEqual(response.data["status"], Reservation.Status.CONFIRMED)
        self.assertEqual(response.data["items"][0]["quantity"], 3)

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

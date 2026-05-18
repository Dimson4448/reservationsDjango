from django.contrib.auth.models import User
from django.template.loader import get_template
from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve

from accounts import views
from catalogue.models import Reservation


class AccountRoutingTests(SimpleTestCase):
    def test_profile_routes_are_registered(self):
        self.assertEqual(resolve(reverse("accounts:user-profile")).func, views.profile)
        self.assertEqual(resolve(reverse("accounts:user-delete", args=[1])).func, views.delete)


class AccountTemplateTests(SimpleTestCase):
    def test_profile_template_compiles(self):
        self.assertIsNotNone(get_template("user/profile.html"))


class ProfileReservationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="client", password="pass12345")
        self.confirmed = Reservation.objects.create(
            user=self.user,
            status=Reservation.Status.CONFIRMED,
        )
        self.canceled = Reservation.objects.create(
            user=self.user,
            status=Reservation.Status.CANCELED,
        )

    def test_profile_displays_reservation_summary(self):
        self.client.login(username="client", password="pass12345")

        response = self.client.get(reverse("accounts:user-profile"))

        self.assertContains(response, "Total")
        self.assertContains(response, "Confirmees")
        self.assertContains(response, "Annulees")
        self.assertContains(response, f"#{self.confirmed.id}")
        self.assertContains(response, f"#{self.canceled.id}")

    def test_profile_can_filter_canceled_reservations(self):
        self.client.login(username="client", password="pass12345")

        response = self.client.get(reverse("accounts:user-profile"), {"status": "canceled"})

        self.assertContains(response, f"#{self.canceled.id}")
        self.assertNotContains(response, f"#{self.confirmed.id}")

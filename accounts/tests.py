from django.template.loader import get_template
from django.test import SimpleTestCase
from django.urls import reverse, resolve

from accounts import views


class AccountRoutingTests(SimpleTestCase):
    def test_profile_routes_are_registered(self):
        self.assertEqual(resolve(reverse("accounts:user-profile")).func, views.profile)
        self.assertEqual(resolve(reverse("accounts:user-delete", args=[1])).func, views.delete)


class AccountTemplateTests(SimpleTestCase):
    def test_profile_template_compiles(self):
        self.assertIsNotNone(get_template("user/profile.html"))

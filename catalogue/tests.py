from django.template.loader import get_template
from django.test import SimpleTestCase
from django.urls import reverse, resolve

from catalogue.views import artist, show_


class CatalogueRoutingTests(SimpleTestCase):
    def test_show_routes_are_registered(self):
        self.assertEqual(resolve(reverse("catalogue:show-index")).func, show_.index)
        self.assertEqual(resolve(reverse("catalogue:show-show", args=[1])).func, show_.show)

    def test_reservation_route_is_registered(self):
        url = reverse("catalogue:reservation-create", args=[1])
        self.assertEqual(resolve(url).func, show_.reserve)

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

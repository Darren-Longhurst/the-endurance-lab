from django.test import SimpleTestCase
from django.urls import resolve, reverse

from checkout import views


class CheckoutUrlsTests(SimpleTestCase):
    def test_checkout_url_resolves(self):
        url = reverse("checkout")
        self.assertEqual(resolve(url).func, views.checkout)

    def test_cache_checkout_data_url_resolves(self):
        url = reverse("cache_checkout_data")
        self.assertEqual(resolve(url).func, views.cache_checkout_data)

    def test_checkout_success_url_resolves(self):
        url = reverse("checkout_success", args=["ORDER123"])
        self.assertEqual(resolve(url).func, views.checkout_success)

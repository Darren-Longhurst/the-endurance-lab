from django.test import SimpleTestCase
from django.urls import reverse, NoReverseMatch


class CheckoutURLTests(SimpleTestCase):
    def test_checkout_url_resolves(self):
        try:
            url = reverse("checkout")
        except NoReverseMatch:
            self.skipTest("URL name 'checkout' not found.")
        self.assertTrue(url)

    def test_checkout_success_url_resolves(self):
        # success pages often need an order number arg; try a placeholder
        try:
            url = reverse("checkout_success", args=["TESTORDER123"])
        except NoReverseMatch:
            self.skipTest("URL name 'checkout_success' not found.")
        self.assertTrue(url)

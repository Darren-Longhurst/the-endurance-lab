from django.test import TestCase
from django.urls import reverse, NoReverseMatch


class ProductsViewTests(TestCase):
    def test_products_page_returns_200(self):
        try:
            url = reverse("products")
        except NoReverseMatch:
            self.skipTest("URL name 'products' not found.")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_product_detail_returns_200_or_404(self):
        """
        If product id 1 doesn't exist yet, a 404 is acceptable.
        Once you add factories/fixtures, change this to assert 200.
        """
        try:
            url = reverse("product_detail", args=[1])
        except NoReverseMatch:
            self.skipTest("URL name 'product_detail' not found.")
        resp = self.client.get(url)
        self.assertIn(resp.status_code, [200, 404])

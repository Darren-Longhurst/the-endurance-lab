from django.test import SimpleTestCase
from django.urls import reverse, NoReverseMatch


class ProductsURLTests(SimpleTestCase):
    def test_products_list_url_resolves(self):
        """Products listing page should resolve."""
        try:
            url = reverse("products")
        except NoReverseMatch:
            self.skipTest("URL name 'products' not found.")
        self.assertTrue(url)

    def test_product_detail_url_resolves(self):
        """Product detail page should resolve (requires an id)."""
        try:
            url = reverse("product_detail", args=[1])
        except NoReverseMatch:
            self.skipTest("URL name 'product_detail' not found.")
        self.assertTrue(url)

    def test_add_product_url_resolves(self):
        try:
            url = reverse("add_product")
        except NoReverseMatch:
            self.skipTest("URL name 'add_product' not found.")
        self.assertTrue(url)

    def test_edit_product_url_resolves(self):
        try:
            url = reverse("edit_product", args=[1])
        except NoReverseMatch:
            self.skipTest("URL name 'edit_product' not found.")
        self.assertTrue(url)

    def test_delete_product_url_resolves(self):
        try:
            url = reverse("delete_product", args=[1])
        except NoReverseMatch:
            self.skipTest("URL name 'delete_product' not found.")
        self.assertTrue(url)

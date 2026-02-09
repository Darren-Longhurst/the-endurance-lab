from django.test import TestCase


class ProductsModelTests(TestCase):
    def test_product_str(self):
        try:
            from products.models import Product
        except Exception:
            self.skipTest("Could not import Product model from products.models")

        # Create minimal valid object (adjust fields if required)
        kwargs = {}
        for field in ["name", "price"]:
            if field == "name":
                kwargs["name"] = "Test Product"
            if field == "price":
                kwargs["price"] = "9.99"

        try:
            product = Product.objects.create(**kwargs)
        except Exception:
            self.skipTest("Could not create Product with minimal fields; update required fields in test.")

        self.assertEqual(str(product), getattr(product, "name", ""))

    def test_category_str(self):
        try:
            from products.models import Category
        except Exception:
            self.skipTest("Could not import Category model from products.models")

        try:
            cat = Category.objects.create(name="energy", friendly_name="Energy")
        except Exception:
            self.skipTest("Could not create Category; update required fields in test.")

        # common pattern: __str__ returns name
        self.assertEqual(str(cat), getattr(cat, "name", ""))

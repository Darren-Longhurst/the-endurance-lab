from types import SimpleNamespace
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse


class CartViewTests(TestCase):
    def setUp(self):
        # ensure session exists
        session = self.client.session
        session["cart"] = {}
        session.save()

    def test_view_cart_renders_template(self):
        resp = self.client.get(reverse("view_cart"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "cart/cart.html")

    @patch("cart.views.get_object_or_404")
    def test_add_to_cart_adds_new_item_no_variant(self, mock_get_object_or_404):
        # first get_object_or_404 call returns Product
        mock_get_object_or_404.return_value = SimpleNamespace(name="Test Product")

        resp = self.client.post(
            reverse("add_to_cart", args=[1]),
            {
                "quantity": "2",
                "redirect_url": reverse("view_cart"),
                # no product_variant => non-variant item_key "1"
            },
        )

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse("view_cart"))

        session = self.client.session
        self.assertEqual(session["cart"]["1"], 2)

        # only product lookup, no variant lookup
        self.assertEqual(mock_get_object_or_404.call_count, 1)

    @patch("cart.views.get_object_or_404")
    def test_add_to_cart_increments_existing_item(self, mock_get_object_or_404):
        mock_get_object_or_404.return_value = SimpleNamespace(name="Test Product")

        # seed cart with existing item
        session = self.client.session
        session["cart"] = {"1": 1}
        session.save()

        resp = self.client.post(
            reverse("add_to_cart", args=[1]),
            {"quantity": "3", "redirect_url": reverse("view_cart")},
        )

        self.assertEqual(resp.status_code, 302)

        session = self.client.session
        self.assertEqual(session["cart"]["1"], 4)

    @patch("cart.views.get_object_or_404")
    def test_add_to_cart_adds_variant_item_key_and_uses_variant_name(self, mock_get_object_or_404):
        # first call -> Product, second call -> ProductVariant
        product = SimpleNamespace(name="Gel")
        variant = SimpleNamespace(variant_value="Strawberry")
        mock_get_object_or_404.side_effect = [product, variant]

        resp = self.client.post(
            reverse("add_to_cart", args=[10]),
            {
                "quantity": "1",
                "redirect_url": reverse("view_cart"),
                "product_variant": "5",
            },
        )

        self.assertEqual(resp.status_code, 302)

        session = self.client.session
        # variant key should be "10_5"
        self.assertEqual(session["cart"]["10_5"], 1)
        self.assertEqual(mock_get_object_or_404.call_count, 2)

    def test_adjust_cart_sets_quantity_when_positive(self):
        # seed cart with an item_key (could be variant-style or normal)
        session = self.client.session
        session["cart"] = {"10_5": 1}
        session.save()

        resp = self.client.post(
            reverse("adjust_cart", args=["10_5"]),
            {"quantity": "4"},
        )

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse("view_cart"))

        session = self.client.session
        self.assertEqual(session["cart"]["10_5"], 4)

    def test_adjust_cart_removes_item_when_zero(self):
        session = self.client.session
        session["cart"] = {"1": 2}
        session.save()

        resp = self.client.post(
            reverse("adjust_cart", args=["1"]),
            {"quantity": "0"},
        )

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse("view_cart"))

        session = self.client.session
        self.assertNotIn("1", session["cart"])

    def test_remove_from_cart_returns_200_on_success(self):
        session = self.client.session
        session["cart"] = {"1": 2}
        session.save()

        resp = self.client.get(reverse("remove_from_cart", args=["1"]))
        self.assertEqual(resp.status_code, 200)

        session = self.client.session
        self.assertNotIn("1", session["cart"])

    def test_remove_from_cart_returns_500_if_key_missing(self):
        # empty cart => pop() raises KeyError => hits exception branch => 500
        session = self.client.session
        session["cart"] = {}
        session.save()

        resp = self.client.get(reverse("remove_from_cart", args=["does-not-exist"]))
        self.assertEqual(resp.status_code, 500)

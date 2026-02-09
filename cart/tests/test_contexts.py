from decimal import Decimal

from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import Http404

from cart.contexts import cart_contents
from products.models import Product, Category


class CartContextsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(name="test", friendly_name="Test")

        self.product = Product.objects.create(
            name="Test Product",
            description="desc",
            price=Decimal("10.00"),
            category=self.category,
        )

    def _request_with_session(self, cart_dict):
        request = self.factory.get("/")
        middleware = SessionMiddleware(lambda r: None)
        middleware.process_request(request)
        request.session.save()
        request.session["cart"] = cart_dict
        request.session.save()
        return request

    def test_cart_context_empty_cart_has_expected_keys(self):
        request = self._request_with_session({})
        ctx = cart_contents(request)

        # keys your context processor actually returns (based on your output)
        self.assertIn("cart_items", ctx)
        self.assertIn("subtotal", ctx)
        self.assertIn("product_count", ctx)
        self.assertIn("delivery", ctx)
        self.assertIn("free_delivery_delta", ctx)
        self.assertIn("free_delivery_threshold", ctx)
        self.assertIn("grand_total", ctx)

        self.assertEqual(ctx["product_count"], 0)
        self.assertEqual(ctx["subtotal"], 0)

    def test_cart_context_with_valid_product_calculates_totals(self):
        request = self._request_with_session({str(self.product.id): 2})
        ctx = cart_contents(request)

        self.assertEqual(ctx["product_count"], 2)
        self.assertEqual(ctx["subtotal"], Decimal("20.00"))
        self.assertGreaterEqual(ctx["grand_total"], ctx["subtotal"])

        # should include at least one cart item
        self.assertTrue(len(ctx["cart_items"]) >= 1)

    def test_cart_context_missing_product_raises_404(self):
        """
        Your cart_contents uses get_object_or_404(Product, pk=item_key),
        so missing product IDs should raise Http404 (NOT be silently ignored).
        """
        request = self._request_with_session({"999999": 1})
        with self.assertRaises(Http404):
            cart_contents(request)

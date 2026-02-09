from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock
from decimal import Decimal

from products.models import Product
from checkout.models import Order
from profiles.models import UserProfile


class CheckoutViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name="Test Product",
            price=Decimal("10.00"),
            description="Test",
            sku="TEST1"
        )
        self.checkout_url = reverse("checkout")

    # ---------------------------
    # cache_checkout_data
    # ---------------------------

    @patch("checkout.views.stripe.PaymentIntent.modify")
    def test_cache_checkout_data_success(self, mock_modify):
        response = self.client.post(
            reverse("cache_checkout_data"),
            {
                "client_secret": "pi_123_secret_456",
                "save_info": "true"
            }
        )
        self.assertEqual(response.status_code, 200)
        mock_modify.assert_called_once()

    @patch("checkout.views.stripe.PaymentIntent.modify", side_effect=Exception("Stripe error"))
    def test_cache_checkout_data_failure(self, mock_modify):
        response = self.client.post(
            reverse("cache_checkout_data"),
            {
                "client_secret": "pi_123_secret_456",
                "save_info": "true"
            }
        )
        self.assertEqual(response.status_code, 400)

    # ---------------------------
    # checkout GET
    # ---------------------------

    def test_checkout_get_empty_cart_redirects(self):
        response = self.client.get(self.checkout_url)
        self.assertRedirects(response, reverse("products"))

    @patch("checkout.views.stripe.PaymentIntent.create")
    def test_checkout_get_with_cart(self, mock_create):
        mock_create.return_value = MagicMock(client_secret="secret123")

        session = self.client.session
        session["cart"] = {str(self.product.id): 2}
        session.save()

        response = self.client.get(self.checkout_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "secret123")

    # ---------------------------
    # checkout POST
    # ---------------------------

    @patch("checkout.views.stripe.PaymentIntent.create")
    def test_checkout_post_valid_order(self, mock_create):
        mock_create.return_value = MagicMock(client_secret="secret123")

        session = self.client.session
        session["cart"] = {str(self.product.id): 1}
        session.save()

        response = self.client.post(self.checkout_url, {
            "full_name": "Test User",
            "email": "test@test.com",
            "phone_number": "123456789",
            "country": "GB",
            "postcode": "ABC123",
            "town_or_city": "Town",
            "street_address1": "Street 1",
            "street_address2": "",
            "county": "County",
            "client_secret": "pi_123_secret_456",
        })

        order = Order.objects.first()
        self.assertRedirects(
            response,
            reverse("checkout_success", args=[order.order_number])
        )

    def test_checkout_post_invalid_form(self):
        session = self.client.session
        session["cart"] = {str(self.product.id): 1}
        session.save()

        response = self.client.post(self.checkout_url, {})
        self.assertEqual(response.status_code, 200)

    def test_checkout_post_product_missing(self):
        session = self.client.session
        session["cart"] = {"999": 1}
        session.save()

        response = self.client.post(self.checkout_url, {
            "full_name": "Test User",
            "email": "test@test.com",
            "phone_number": "123456789",
            "country": "GB",
            "postcode": "ABC123",
            "town_or_city": "Town",
            "street_address1": "Street 1",
            "street_address2": "",
            "county": "County",
            "client_secret": "pi_123_secret_456",
        })

        self.assertRedirects(response, reverse("view_cart"))

    # ---------------------------
    # checkout_success
    # ---------------------------

    def test_checkout_success_anonymous(self):
        order = Order.objects.create(
            full_name="Test",
            email="test@test.com",
            phone_number="123",
            country="GB",
            postcode="ABC",
            town_or_city="Town",
            street_address1="Street",
            stripe_pid="pid123",
            original_cart="{}",
        )

        response = self.client.get(
            reverse("checkout_success", args=[order.order_number])
        )

        self.assertEqual(response.status_code, 200)

    def test_checkout_success_authenticated_user(self):
        user = User.objects.create_user("testuser", "test@test.com", "pass")
        profile = UserProfile.objects.create(user=user)

        self.client.login(username="testuser", password="pass")

        order = Order.objects.create(
            full_name="Test",
            email="test@test.com",
            phone_number="123",
            country="GB",
            postcode="ABC",
            town_or_city="Town",
            street_address1="Street",
            stripe_pid="pid123",
            original_cart="{}",
        )

        session = self.client.session
        session["save_info"] = True
        session.save()

        response = self.client.get(
            reverse("checkout_success", args=[order.order_number])
        )

        order.refresh_from_db()
        self.assertEqual(order.user_profile, profile)
        self.assertEqual(response.status_code, 200)

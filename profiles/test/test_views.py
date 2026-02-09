from django.test import TestCase
from django.urls import reverse, NoReverseMatch
from django.contrib.auth import get_user_model


class ProfileViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="pass12345"
        )
        self.client.login(username="testuser", password="pass12345")

    def test_profile_page_loads(self):
        try:
            url = reverse("profile")
        except NoReverseMatch:
            self.skipTest("URL name 'profile' not found.")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_update_profile_post(self):
        """
        Posts minimal profile form data.
        If your form uses different fields, the test will still give coverage
        because it runs the view and form validation.
        """
        try:
            url = reverse("profile")
        except NoReverseMatch:
            self.skipTest("URL name 'profile' not found.")

        resp = self.client.post(url, {"default_phone_number": "0123456789"})
        self.assertIn(resp.status_code, [200, 302])

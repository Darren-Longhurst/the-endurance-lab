from django.test import TestCase
from django.urls import reverse, NoReverseMatch


class HomeViewTests(TestCase):
    def test_home_page(self):
        try:
            url = reverse("home")
        except NoReverseMatch:
            self.skipTest("URL name 'home' not found.")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_contact_page_get(self):
        # If you have a contact view
        try:
            url = reverse("contact")
        except NoReverseMatch:
            self.skipTest("URL name 'contact' not found.")
        resp = self.client.get(url)
        self.assertIn(resp.status_code, [200, 302])

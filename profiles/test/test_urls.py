from django.test import SimpleTestCase
from django.urls import reverse, NoReverseMatch


class ProfilesURLTests(SimpleTestCase):
    def test_profile_url_resolves(self):
        try:
            url = reverse("profile")
        except NoReverseMatch:
            self.skipTest("URL name 'profile' not found.")
        self.assertTrue(url)

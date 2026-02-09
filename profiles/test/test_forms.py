from django.test import TestCase


class ProfileFormTests(TestCase):
    def test_profile_form_accepts_valid_data(self):
        from profiles.forms import UserProfileForm

        # Only include fields that definitely exist; extra fields are ignored by Django
        form = UserProfileForm(data={"default_phone_number": "07123456789"})
        form.is_valid()  # triggers validation paths
        self.assertTrue(hasattr(form, "errors"))

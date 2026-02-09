from django.test import TestCase


class CheckoutFormTests(TestCase):
    def test_order_form_validation_runs(self):
        from checkout.forms import OrderForm

        form = OrderForm(data={})
        form.is_valid()
        self.assertTrue(hasattr(form, "errors"))

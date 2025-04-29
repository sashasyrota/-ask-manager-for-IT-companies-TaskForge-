from django.test import TestCase

from taskmanager.forms import WorkerCreationForm
from taskmanager.models import Position


class TestForms(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="test_position")

    def test_worker_form_with_custom_fields(self):
        form_data = {
            "username": "new_user",
            "password1": "<PASSWORD12>",
            "password2": "<PASSWORD12>",
            "first_name": "Test_first_name",
            "last_name": "Test_last_name",
            "position": self.position,
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

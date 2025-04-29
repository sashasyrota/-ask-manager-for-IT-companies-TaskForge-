from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from taskmanager.models import Position


class TestAdmin(TestCase):
    def setUp(self):
        self.client = Client()
        self.position = Position.objects.create(name="test_position")
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="<PASSWORD>", position=self.position
        )
        self.client.force_login(self.admin_user)

        self.worker = get_user_model().objects.create_user(
            username="test_username",
            password="<TESTPASSWORD>",
            position=self.position,
        )

    def test_worker_position_listed(self):
        url = reverse("admin:taskmanager_worker_changelist")
        res = self.client.get(url)
        self.assertContains(res, "test_position")

    def test_worker_detail_position_listed(self):
        url = reverse("admin:taskmanager_worker_change", args=[self.worker.pk])
        res = self.client.get(url)
        self.assertContains(res, "test_position")

    def test_worker_add_position_listed(self):
        url = reverse("admin:taskmanager_worker_add")
        res = self.client.get(url)
        self.assertContains(res, "test_position")

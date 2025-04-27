from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taskmanager.models import Position, Task, Worker, TaskType


class TestPositionViews(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="TestName1"
        )
        self.position = Position.objects.create(
            name="TestName2"
        )
        self.position = Position.objects.create(
            name="TestName3"
        )
        self.user = get_user_model().objects.create_user(
            username="TestUser",
            password="<PASSWORD>",
            position=self.position,
        )
        self.urls = {
            "list": reverse("taskmanager:position-list"),
            "create": reverse("taskmanager:position-create"),
            "update": reverse(
                "taskmanager:position-update", kwargs={"pk": self.position.pk}
            ),
            "delete": reverse(
                "taskmanager:position-delete", kwargs={"pk": self.position.pk}
            ),
        }

    def test_login_required_position(self):
        for url in self.urls:
            response = self.client.get(self.urls[url])
            self.assertNotEqual(response.status_code, 200)

    def test_retrieve_position_list(self):
        self.client.force_login(self.user)
        response = self.client.get(self.urls["list"])
        self.assertEqual(response.status_code, 200)
        positions = Position.objects.all()
        print(response.context)
        self.assertEqual(
            list(positions),
            list(response.context["positions"]),
        )
        self.assertTemplateUsed(response, "taskmanager/position-list.html")

    def test_position_search(self):
        self.client.force_login(self.user)
        response = self.client.get(self.urls["list"], {"name": "Name2"})
        position = response.context["positions"]
        self.assertEqual(position[0].name, "TestName2")


class TestWorkerLoginRequiredViews(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="TestName1"
        )

        self.worker1 = Worker.objects.create_user(
            first_name="Test Worker1",
            username="TestUsername1",
            password="<PASSWORD>1",
            position=self.position,
        )
        self.worker2 = Worker.objects.create_user(
            first_name="Test Worker2",
            username="TestUsername2",
            password="<PASSWORD>2",
            position=self.position,
        )

        self.urls = {
            "list": reverse("taskmanager:worker-list"),
            "create": reverse("taskmanager:worker-create"),
            "update":
                reverse("taskmanager:worker-update", kwargs={"pk": self.worker1.pk}),
            "delete":
                reverse("taskmanager:worker-delete", kwargs={"pk": self.worker1.pk}),
            "detail":
                reverse("taskmanager:worker-detail", kwargs={"pk": self.worker1.pk}),
            "assign":
                reverse(
                    "taskmanager:toggle-task-assign", kwargs={"pk": self.worker1.pk}
            ),
        }

    def test_login_required_worker(self):
        for url in self.urls:
            response = self.client.get(self.urls[url])
            self.assertNotEqual(response.status_code, 200)

    def test_retrieve_worker_list(self):
        self.client.force_login(self.worker1)
        response = self.client.get(self.urls["list"])
        self.assertEqual(response.status_code, 200)
        workers = Worker.objects.all()
        self.assertEqual(
            list(workers),
            list(response.context["workers"]),
        )
        self.assertTemplateUsed(response, "taskmanager/worker-list.html")

    def test_worker_search(self):
        self.client.force_login(self.worker1)
        response = self.client.get(self.urls["list"], {"search": "name2"})
        workers = response.context["workers"]
        self.assertEqual(workers[0].username, "TestUsername2")


class TestTaskLoginRequiredViews(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="TestName1"
        )

        self.tasktype = TaskType.objects.create(name="TestTaskType")

        self.user = get_user_model().objects.create_user(
            username="TestUser",
            password="<PASSWORD>",
            position=self.position,
        )

        self.task1 = Task.objects.create(
            name="TestName1",
            description="TestDescription1",
            is_complete=True,
            task_type=self.tasktype,
        )

        self.task2 = Task.objects.create(
            name="TestName2",
            description="TestDescription2",
            is_complete=True,
            task_type=self.tasktype,
        )

        self.urls = {
            "list": reverse("taskmanager:task-list"),
            "create": reverse("taskmanager:task-create"),
            "update": reverse(
                "taskmanager:task-update", kwargs={"pk": self.task1.pk}
            ),
            "delete": reverse(
                "taskmanager:task-delete", kwargs={"pk": self.task1.pk}
            ),
        }

    def test_login_required_task(self):
        for url in self.urls:
            response = self.client.get(self.urls[url])
            self.assertNotEqual(response.status_code, 200)

    def test_retrieve_task_list(self):
        self.client.force_login(self.user)
        response = self.client.get(self.urls["list"])
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.all()
        self.assertEqual(
            list(tasks),
            list(response.context["tasks"]),
        )
        self.assertTemplateUsed(response, "taskmanager/task-list.html")

    def test_task_search(self):
        self.client.force_login(self.user)
        response = self.client.get(self.urls["list"], {"search": "ame2"})
        tasks = response.context["tasks"]
        self.assertEqual(tasks[0].name, "TestName2")


class TestTaskTypeLoginRequiredViews(TestCase):
    def setUp(self):
        self.tasktype1 = TaskType.objects.create(name="TestTaskType1")

        self.tasktype2 = TaskType.objects.create(name="TestTaskType2")

        self.position = Position.objects.create(
            name="TestName1"
        )

        self.user = get_user_model().objects.create_user(
            username="TestUser",
            password="<PASSWORD>",
            position=self.position,
        )

        self.urls = {
            "list": reverse("taskmanager:tasktype-list"),
            "create": reverse("taskmanager:tasktype-create"),
            "update": reverse(
                "taskmanager:tasktype-update", kwargs={"pk": self.tasktype1.pk}
            ),
            "delete": reverse(
                "taskmanager:tasktype-delete", kwargs={"pk": self.tasktype1.pk}
            ),
        }

    def test_login_required_tasktype(self):
        for url in self.urls:
            response = self.client.get(self.urls[url])
            self.assertNotEqual(response.status_code, 200)

    def test_retrieve_tasktype_list(self):
        self.client.force_login(self.user)
        response = self.client.get(self.urls["list"])
        self.assertEqual(response.status_code, 200)
        tasktypes = TaskType.objects.all()
        self.assertEqual(
            list(tasktypes),
            list(response.context["task_types"]),
        )
        self.assertTemplateUsed(response, "taskmanager/tasktype-list.html")

    def test_tasktype_search(self):
        self.client.force_login(self.user)
        response = self.client.get(self.urls["list"], {"search": "ype2"})
        task_types = response.context["task_types"]
        self.assertEqual(task_types[0].name, "TestTaskType2")

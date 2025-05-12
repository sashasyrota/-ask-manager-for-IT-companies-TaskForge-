from django.test import TestCase

from taskmanager.models import Position, Worker, Task, TaskType


class TestModel(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="TestName",
        )
        self.worker = Worker.objects.create_user(
            id=1,
            first_name="TestFirstName",
            last_name="TestLastName",
            username="TestUsername",
            password="<PASSWORD>",
            position=self.position,
        )
        self.tasktype = TaskType.objects.create(name="TestTaskType")
        self.task = Task.objects.create(
            name="TestName",
            description="TestDescription",
            is_complete=True,
            task_type=self.tasktype,
        )

    def test_position_str(self):
        self.assertEqual(str(self.position), "TestName")

    def test_worker_str(self):
        self.assertEqual(str(self.worker), "TestUsername (1)")

    def test_task_str(self):
        self.assertEqual(str(self.task), "TestName")

    def test_worker_with_position(self):
        self.assertEqual(self.worker.position, self.position)
        self.assertEqual(self.worker.first_name, "TestFirstName")
        self.assertEqual(self.worker.last_name, "TestLastName")
        self.assertTrue(self.worker.check_password("<PASSWORD>"))
        self.assertEqual(self.worker.username, "TestUsername")

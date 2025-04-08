from django.contrib.auth.models import User, AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=100)


class Priority(models.TextChoices):
    URGENT = 'urgent', 'URGENT'
    HIGH = 'high', 'HIGH'
    NORMAL = 'normal', 'NORMAL'
    LOW = 'low', 'LOW'


class Position(models.Model):
    name = models.CharField(max_length=100)


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='workers')


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_complete = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.NORMAL,
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name='tasks')
    assignees = models.ManyToManyField(Worker, related_name='tasks')

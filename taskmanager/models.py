from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.urls import reverse


class TaskType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Priority(models.TextChoices):
    URGENT = 'urgent', 'URGENT'
    HIGH = 'high', 'HIGH'
    NORMAL = 'normal', 'NORMAL'
    LOW = 'low', 'LOW'


class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='workers', null=True)

    def get_absolute_url(self):
        return reverse("taskmanager:worker-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.username} ({self.pk})"


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.NORMAL,
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name='tasks')
    assignees = models.ManyToManyField(Worker, related_name='tasks')

    class Meta:
        ordering = ['deadline']

    def __str__(self):
        return self.name
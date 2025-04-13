from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from taskmanager.models import Task, Worker, TaskType, Position


def index(request) -> HttpResponse:
    context = {
        'tasks': Task.objects.count(),
        'workers': Worker.objects.count(),
    }
    return render(request, "taskmanager/index.html", context=context)


class TaskListView(generic.ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'taskmanager/task-list.html'


class TaskDetailView(generic.DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'taskmanager/task-detail.html'


class TaskCreateView(generic.CreateView):
    model = Task
    fields = "__all__"
    template_name = "taskmanager/task-form.html"
    success_url = reverse_lazy("taskmanager:task-list")

class WorkerListView(generic.ListView):
    model = Worker
    context_object_name = 'workers'
    template_name = 'taskmanager/worker-list.html'


class WorkerDetailView(generic.DetailView):
    model = Worker
    template_name = 'taskmanager/worker-detail.html'


class TaskTypeListView(generic.ListView):
    model = TaskType
    context_object_name = 'task_types'
    template_name = 'taskmanager/tasktype-list.html'


class TaskTypeDetailView(generic.DetailView):
    model = TaskType
    context_object_name = 'task_type'
    template_name = 'taskmanager/tasktype-detail.html'


class PositionListView(generic.ListView):
    model = Position
    context_object_name = 'positions'
    template_name = 'taskmanager/position-list.html'


class PositionDetailView(generic.DetailView):
    model = Position
    template_name = 'taskmanager/position-detail.html'

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.views import LogoutView

from taskmanager.forms import TaskNameSearchForm, WorkerUsernameSearchForm, TaskTypeNameSearchForm, \
    PositionNameSearchForm
from taskmanager.models import Task, Worker, TaskType, Position


def index(request) -> HttpResponse:
    context = {
        'tasks': Task.objects,
        'workers': Worker.objects,
        'nearest_deadline': Task.objects.order_by('deadline')[0],
    }
    return render(request, "taskmanager/index.html", context=context)


class TaskListView(generic.ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'taskmanager/task-list.html'
    paginate_by = 5

    def get_context_data(
        self, *, object_list = None, **kwargs
    ):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get('name')
        context['search_form'] = TaskNameSearchForm(initial={'name': name})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset



class TaskDetailView(generic.DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'taskmanager/task-detail.html'


class TaskCreateView(generic.CreateView):
    model = Task
    fields = "__all__"
    template_name = "taskmanager/task-form.html"
    success_url = reverse_lazy("taskmanager:task-list")


class TaskUpdateView(generic.UpdateView):
    model = Task
    fields = "__all__"
    template_name = "taskmanager/task-form.html"
    success_url = reverse_lazy("taskmanager:task-detail")


class TaskDeleteView(generic.DeleteView):
    model = Task
    template_name = "taskmanager/task-confirm-form.html"
    success_url = reverse_lazy("taskmanager:task-list")


class ToggleTaskAssignView(View):
    def get(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        worker = get_object_or_404(Worker, pk=request.user.id)
        if worker.tasks.filter(id=pk).exists():
            task.assignees.remove(worker)
        else:
            task.assignees.add(worker)
        return redirect("taskmanager:task-detail", pk=pk)


class WorkerListView(generic.ListView):
    model = Worker
    context_object_name = 'workers'
    template_name = 'taskmanager/worker-list.html'
    paginate_by = 5

    def get_context_data(
        self, *, object_list = None, **kwargs
    ):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get('username')
        context['search_form'] = WorkerUsernameSearchForm(initial={'username': username})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.GET.get('username')
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset


class WorkerDetailView(generic.DetailView):
    model = Worker
    template_name = 'taskmanager/worker-detail.html'


class WorkerCreateView(generic.CreateView):
    model = Worker
    fields = "__all__"
    template_name = "taskmanager/worker-form.html"
    success_url = reverse_lazy("taskmanager:worker-list")


class WorkerUpdateView(generic.UpdateView):
    model = Worker
    fields = "__all__"
    template_name = "taskmanager/worker-form.html"
    success_url = reverse_lazy("taskmanager:worker-detail")


class WorkerDeleteView(generic.DeleteView):
    model = Worker
    template_name = "taskmanager/worker-confirm-form.html"
    success_url = reverse_lazy("taskmanager:worker-list")


class TaskTypeListView(generic.ListView):
    model = TaskType
    context_object_name = 'task_types'
    template_name = 'taskmanager/tasktype-list.html'
    paginate_by = 5

    def get_context_data(
        self, *, object_list = None, **kwargs
    ):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get('name')
        context['search_form'] = TaskTypeNameSearchForm(initial={'name': name})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class TaskTypeDetailView(generic.DetailView):
    model = TaskType
    context_object_name = 'task_type'
    template_name = 'taskmanager/tasktype-detail.html'


class TaskTypeCreateView(generic.CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "taskmanager/tasktype-form.html"
    success_url = reverse_lazy("taskmanager:tasktype-list")


class TaskTypeUpdateView(generic.UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "taskmanager/tasktype-form.html"
    success_url = reverse_lazy("taskmanager:tasktype-detail")


class TaskTypeDeleteView(generic.DeleteView):
    model = TaskType
    template_name = "taskmanager/tasktype-confirm-form.html"
    success_url = reverse_lazy("taskmanager:tasktype-list")

class PositionListView(generic.ListView):
    model = Position
    context_object_name = 'positions'
    template_name = 'taskmanager/position-list.html'

    def get_context_data(
        self, *, object_list = None, **kwargs
    ):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get('name')
        context['search_form'] = PositionNameSearchForm(initial={'name': name})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class PositionDetailView(generic.DetailView):
    model = Position
    template_name = 'taskmanager/position-detail.html'


class PositionCreateView(generic.CreateView):
    model = Position
    fields = "__all__"
    template_name = "taskmanager/position-form.html"
    success_url = reverse_lazy("taskmanager:position-list")


class PositionUpdateView(generic.UpdateView):
    model = Position
    fields = "__all__"
    template_name = "taskmanager/position-form.html"
    success_url = reverse_lazy("taskmanager:position-detail")


class PositionDeleteView(generic.DeleteView):
    model = Position
    template_name = "taskmanager/position-confirm-form.html"
    success_url = reverse_lazy("taskmanager:position-list")

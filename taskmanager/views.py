from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.views import LoginView, PasswordChangeView

from taskmanager.forms import (
    TaskNameSearchForm,
    WorkerUsernameSearchForm,
    TaskTypeNameSearchForm,
    PositionNameSearchForm,
    WorkerSortForm,
    TaskSortForm,
    PositionSortForm,
    TaskTypeSortForm,
    LoginForm,
    UserPasswordChangeForm,
    WorkerCreationForm,
    WorkerChangeForm,
    TaskChangeForm,
)

from taskmanager.models import Task, Worker, TaskType, Position


@login_required
def index(request) -> HttpResponse:
    context = {
        "tasks": Task.objects,
        "tasktypes": TaskType.objects,
        "workers": Worker.objects,
        "positions": Position.objects,
        "nearest_deadline": Task.objects.filter(is_complete=False).order_by("deadline")[
            0
        ],
    }
    return render(request, "taskmanager/index.html", context=context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "taskmanager/task-list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        search = self.request.GET.get("search")
        context["search_form"] = TaskNameSearchForm(initial={"search": search})
        context["sort_form"] = TaskSortForm(
            initial={"sort_by": self.request.GET.get("sort_by", "")}
        )
        context["tasks_count"] = Task.objects.count()
        return context

    def get_queryset(self):
        queryset = super().get_queryset().select_related("task_type")
        name = self.request.GET.get("search")
        if name:
            queryset = queryset.filter(name__icontains=name)
        sort_by = self.request.GET.get("sort_by")
        if sort_by in [
            "id",
            "name",
            "deadline",
            "is_complete",
            "priority",
            "task_type",
        ]:
            queryset = queryset.order_by(sort_by)
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    context_object_name = "task"
    template_name = "taskmanager/task-detail.html"


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskChangeForm
    template_name = "taskmanager/task-form.html"
    success_url = reverse_lazy("taskmanager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskChangeForm
    template_name = "taskmanager/task-form.html"

    def get_success_url(self):
        task_id = self.object.id
        return reverse_lazy("taskmanager:task-detail", args=[task_id])


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "taskmanager/task-confirm-form.html"
    success_url = reverse_lazy("taskmanager:task-list")


class ToggleTaskAssignView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        worker = get_object_or_404(Worker, pk=request.user.id)
        if worker.tasks.filter(id=pk).exists():
            task.assignees.remove(worker)
        else:
            task.assignees.add(worker)
        return redirect("taskmanager:task-detail", pk=pk)


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    context_object_name = "workers"
    template_name = "taskmanager/worker-list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("search")
        context["search_form"] = WorkerUsernameSearchForm(initial={"search": username})
        context["sort_form"] = WorkerSortForm(
            initial={"sort_by": self.request.GET.get("sort_by", "")}
        )
        context["workers_count"] = Worker.objects.count()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.GET.get("search")
        if username:
            queryset = queryset.filter(username__icontains=username)
        sort_by = self.request.GET.get("sort_by")
        if sort_by in ["id", "position", "username", "first_name", "last_name"]:
            queryset = queryset.order_by(sort_by)
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    template_name = "taskmanager/worker-detail.html"


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    template_name = "taskmanager/worker-form.html"
    success_url = reverse_lazy("taskmanager:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerChangeForm
    template_name = "taskmanager/worker-form.html"

    def get_success_url(self):
        worker_id = self.object.id
        return reverse_lazy("taskmanager:worker-detail", args=[worker_id])


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    template_name = "taskmanager/worker-confirm-form.html"
    success_url = reverse_lazy("taskmanager:worker-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    context_object_name = "task_types"
    template_name = "taskmanager/tasktype-list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        search = self.request.GET.get("search")
        context["search_form"] = TaskTypeNameSearchForm(initial={"search": search})
        context["sort_form"] = TaskTypeSortForm(
            initial={"sort_by": self.request.GET.get("sort_by", "")}
        )
        context["task_types_count"] = TaskType.objects.count()
        return context

    def get_queryset(self):
        queryset = TaskType.objects.annotate(task_count=Count("tasks"))
        name = self.request.GET.get("search")
        if name:
            queryset = queryset.filter(name__icontains=name)
        sort_by = self.request.GET.get("sort_by")
        if sort_by in ["id", "name", "task_count"]:
            queryset = queryset.order_by(sort_by)
        return queryset


class TaskTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = TaskType
    context_object_name = "task_type"
    template_name = "taskmanager/tasktype-detail.html"


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "taskmanager/tasktype-form.html"
    success_url = reverse_lazy("taskmanager:tasktype-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "taskmanager/tasktype-form.html"

    def get_success_url(self):
        task_type_id = self.object.id
        return reverse_lazy("taskmanager:tasktype-detail", kwargs={"pk": task_type_id})


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "taskmanager/tasktype-confirm-form.html"
    success_url = reverse_lazy("taskmanager:tasktype-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    context_object_name = "positions"
    template_name = "taskmanager/position-list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("search")
        context["search_form"] = PositionNameSearchForm(initial={"search": name})
        context["sort_form"] = PositionSortForm(
            initial={"sort_by": self.request.GET.get("sort_by", "")}
        )
        context["position_count"] = Position.objects.count()
        return context

    def get_queryset(self):
        queryset = Position.objects.annotate(worker_count=Count("workers"))
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        sort_by = self.request.GET.get("sort_by")
        if sort_by in ["id", "name", "worker_count"]:
            queryset = queryset.order_by(sort_by)
        return queryset


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position
    template_name = "taskmanager/position-detail.html"


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    template_name = "taskmanager/position-form.html"
    success_url = reverse_lazy("taskmanager:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    template_name = "taskmanager/position-form.html"

    def get_success_url(self):
        position_id = self.object.id
        return reverse_lazy("taskmanager:position-detail", kwargs={"pk": position_id})


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    template_name = "taskmanager/position-confirm-form.html"
    success_url = reverse_lazy("taskmanager:position-list")


class UserLoginView(LoginView):
    template_name = "registration/login.html"
    form_class = LoginForm


@login_required
def logout_view(request):
    logout(request)
    return redirect("/accounts/login/")


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "registration/password_change.html"
    form_class = UserPasswordChangeForm

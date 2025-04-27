from asyncio import tasks

from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path

from taskmanager.views import (
    index,
    TaskDetailView,
    WorkerListView,
    WorkerDetailView,
    TaskTypeListView,
    PositionListView,
    PositionDetailView,
    TaskTypeDetailView,
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    ToggleTaskAssignView, WorkerCreateView, WorkerUpdateView, WorkerDeleteView, TaskTypeCreateView, TaskTypeUpdateView,
    TaskTypeDeleteView, PositionCreateView, PositionUpdateView, PositionDeleteView, UserLoginView, logout_view,
    UserPasswordChangeView
)

urlpatterns = [
    path("", index, name="index"),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/password-change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change-done/', PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'
    ), name="password_change_done"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/assign/", ToggleTaskAssignView.as_view(), name="toggle-task-assign"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("workers/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"),
    path("tasktypes/", TaskTypeListView.as_view(), name="tasktype-list"),
    path("tasktypes/<int:pk>/", TaskTypeDetailView.as_view(), name="tasktype-detail"),
    path("tasktypes/create/", TaskTypeCreateView.as_view(), name="tasktype-create"),
    path("tasktypes/<int:pk>/update/", TaskTypeUpdateView.as_view(), name="tasktype-update"),
    path("tasktypes/<int:pk>/delete/", TaskTypeDeleteView.as_view(), name="tasktype-delete"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/<int:pk>/", PositionDetailView.as_view(), name="position-detail"),
    path("positions/create/", PositionCreateView.as_view(), name="position-create"),
    path("positions/<int:pk>/update/", PositionUpdateView.as_view(), name="position-update"),
    path("positions/<int:pk>/delete/", PositionDeleteView.as_view(), name="position-delete"),
]


app_name = "taskmanager"
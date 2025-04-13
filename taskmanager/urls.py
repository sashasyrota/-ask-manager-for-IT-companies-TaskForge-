from asyncio import tasks

from django.urls import path

from taskmanager.views import index, TaskDetailView, WorkerListView, WorkerDetailView, TaskTypeListView, \
    PositionListView, PositionDetailView, TaskTypeDetailView, TaskListView, TaskCreateView

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("tasktypes/", TaskTypeListView.as_view(), name="tasktype-list"),
    path("tasktypes/<int:pk>/", TaskTypeDetailView.as_view(), name="tasktype-detail"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/<int:pk>/", PositionDetailView.as_view(), name="position-detail"),
]


app_name = "taskmanager"
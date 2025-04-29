from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from taskmanager.models import Task, Position, TaskType, Worker


class TaskAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "deadline", "is_complete", "priority", "task_type"]
    list_filter = ["is_complete", "priority", "task_type"]
    actions = ["mark_task"]
    search_fields = ["name", "id"]

    @admin.action(description="Mark task as complete")
    def mark_task(self, request, queryset):
        queryset.update(is_complete=True)


class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["id", "name"]


class PositionAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name", "id"]


class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (("Additional info", {"fields": ("position",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("position",)}),
    )


admin.site.register(Task, TaskAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(TaskType, TaskTypeAdmin)
admin.site.register(Worker, WorkerAdmin)

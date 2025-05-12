from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UsernameField,
    PasswordChangeForm,
    UserCreationForm,
    UserChangeForm,
)
from django.utils.translation import gettext_lazy as _

from taskmanager.models import Worker, Task


class TaskChangeForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}), required=False
    )
    assignees = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Task
        fields = "__all__"


class TaskNameSearchForm(forms.Form):
    search = forms.CharField(
        max_length=255,
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class ": "form-control",
                "placeholder": "Name",
            }
        ),
    )


TASK_SORT_CHOICES = [
    ("id", "ID"),
    ("name", "Name"),
    ("deadline", "Deadline"),
    ("is_complete", "Is complete"),
    ("priority", "Priority"),
    ("task_type", "Task type"),
]


class TaskSortForm(forms.Form):
    sort_by = forms.ChoiceField(
        choices=TASK_SORT_CHOICES,
        label="",
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class WorkerUsernameSearchForm(forms.Form):
    search = forms.CharField(
        max_length=255,
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={"class ": "form-control", "placeholder": "Username"}
        ),
    )


WORKER_SORT_CHOICES = [
    ("id", "ID"),
    ("position", "Position"),
    ("username", "Username"),
    ("first_name", "First Name"),
    ("last_name", "Last Name"),
]


class WorkerSortForm(forms.Form):
    sort_by = forms.ChoiceField(
        choices=WORKER_SORT_CHOICES,
        label="",
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class TaskTypeNameSearchForm(forms.Form):
    search = forms.CharField(
        max_length=255,
        label="",
        required=False,
        widget=forms.TextInput(attrs={"class ": "form-control", "placeholder": "Name"}),
    )


TASKTYPE_SORT_CHOICES = [
    ("id", "ID"),
    ("name", "Name"),
    ("task_count", "Count of tasks"),
]


class TaskTypeSortForm(forms.Form):
    sort_by = forms.ChoiceField(
        choices=TASKTYPE_SORT_CHOICES,
        label="",
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class PositionNameSearchForm(forms.Form):
    search = forms.CharField(
        max_length=255,
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class ": "form-control",
                "placeholder": "Name",
            }
        ),
    )


POSITION_SORT_CHOICES = [
    ("id", "ID"),
    ("name", "Name"),
    ("worker_count", "Count of assignees"),
]


class PositionSortForm(forms.Form):
    sort_by = forms.ChoiceField(
        choices=POSITION_SORT_CHOICES,
        label="",
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class LoginForm(AuthenticationForm):
    username = UsernameField(
        label=_("Your Username"),
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        ),
    )
    password = forms.CharField(
        label=_("Your Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Old Password"}
        ),
        label="Old Password",
    )
    new_password1 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "New Password"}
        ),
        label="New Password",
    )
    new_password2 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm New Password"}
        ),
        label="Confirm New Password",
    )


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position",
        )


class WorkerChangeForm(UserChangeForm):
    date_joined = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}), required=False
    )

    class Meta:
        model = Worker
        fields = "__all__"

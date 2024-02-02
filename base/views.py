from typing import Any

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    DeleteView,
    FormView,
    UpdateView,
)
from django.views.generic.list import ListView

from .forms import TaskCreateForm
from .models import Task


class CustomLoginView(LoginView):
    template_name = "base/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return reverse_lazy("tasks")


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user=self.request.user)
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"
    template_name = "base/task.html"


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ["title", "description", "complete"]
    success_url = reverse_lazy("tasks")


class DeleteTask(DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("tasks")


class RegisterPage(FormView):
    template_name = "base/register.html"
    form_class = UserCreationForm
    # dont work
    redirect_authenticated_user = True
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

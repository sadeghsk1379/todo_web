from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import TaskCreateForm
from .models import Task


class TaskList(ListView):
    model = Task
    context_object_name = "tasks"


class TaskDetail(DetailView):
    model = Task
    context_object_name = "task"
    template_name = "base/task.html"


class TaskCreate(CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("tasks")


class TaskUpdate(UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("tasks")


class DeleteTask(DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("tasks")

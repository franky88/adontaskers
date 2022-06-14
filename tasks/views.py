from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
import datetime
from django.utils import timezone
from django.db.models import Sum
from .models import Task, TaskRemark
from .forms import RemarksForm, TaskForm, AdminTaskForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.


class TaskListView(View):
    form_class = TaskForm
    template_name = 'task_form_template.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        today = timezone.now()
        yesterday = today - timezone.timedelta(days=1)
        if request.user.is_superuser:
            tasks = Task.objects.all().filter(is_done=False)
            priority_tasks_today = Task.objects.filter(updated__date=today.date()).filter(is_priority=True)
            priority_tasks_yesterday = Task.objects.filter(updated__date=yesterday.date()).filter(is_done=False).filter(is_priority=True)
            priority_tasks = Task.objects.filter(is_done=False).filter(is_priority=True)
            wip_tasks_today = Task.objects.filter(created__date=today.date()).filter(is_done=False)
            wip_tasks_yesterday = Task.objects.filter(created__date=yesterday.date()).filter(is_done=False)
            wip_tasks = Task.objects.filter(is_done=False)
            completed_tasks_today = Task.objects.filter(updated__date=today.date()).filter(is_done=True)
            completed_tasks_yesterday = Task.objects.filter(updated__date=yesterday.date()).filter(is_done=True)
            completed_tasks = Task.objects.filter(is_done=True)
            form = AdminTaskForm(request.POST or None)
        else:
            tasks = Task.objects.all().filter(user=request.user).filter(is_done=False)
            priority_tasks_today = Task.objects.filter(user=request.user).filter(updated__date=today.date()).filter(is_done=False).filter(is_priority=True)
            priority_tasks_yesterday = Task.objects.filter(user=request.user).filter(updated__date=yesterday.date()).filter(is_done=False).filter(is_priority=True)
            priority_tasks = Task.objects.filter(user=request.user).filter(is_done=False).filter(is_priority=True)
            wip_tasks_today = Task.objects.filter(user=request.user).filter(created__date=today.date()).filter(is_done=False)
            wip_tasks_yesterday = Task.objects.filter(user=request.user).filter(created__date=yesterday.date()).filter(is_done=False)
            wip_tasks = Task.objects.filter(user=request.user).filter(is_done=False)
            completed_tasks_today = Task.objects.filter(user=request.user).filter(updated__date=today.date()).filter(is_done=True)
            completed_tasks_yesterday = Task.objects.filter(user=request.user).filter(updated__date=yesterday.date()).filter(is_done=True)
            completed_tasks = Task.objects.filter(user=request.user).filter(is_done=True)
            form = self.form_class()
        context = {
                    'form': form,
                    'tasks': tasks,
                    'today': today,
                    'yesterday': yesterday,
                    'priority_tasks_today': priority_tasks_today,
                    'wip_tasks_today': wip_tasks_today,
                    'completed_tasks_today': completed_tasks_today,
                    'priority_tasks_yesterday': priority_tasks_yesterday,
                    'wip_tasks_yesterday': wip_tasks_yesterday,
                    'completed_tasks_yesterday': completed_tasks_yesterday,
                    'priority_tasks': priority_tasks,
                    'completed_tasks': completed_tasks,
                    'wip_tasks': wip_tasks
                }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        if request.user.is_superuser:
            form = AdminTaskForm(request.POST or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                messages.add_message(request, messages.SUCCESS,
                                     'Task successfully created.')
                return redirect("taskers:userview")
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Task successfully created.')
            return redirect("taskers:userview")
        return render(request, self.template_name, {'form': form})


class TaskUpdateView(View):
    form_class = AdminTaskForm
    template_name = 'task_detail_template.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        task_slug = kwargs.get('slug')
        task = get_object_or_404(Task, slug=task_slug)
        remark_form = RemarksForm(request.POST or None)
        if request.user.is_superuser:
            form = AdminTaskForm(request.POST or None, instance=task)
        else:
            form = self.form_class(request.POST or None, instance=task)
        context = {'form': form, 'instance': task, 'remark_form': remark_form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        task_slug = kwargs.get('slug')
        task = get_object_or_404(Task, slug=task_slug)
        remark_form = RemarksForm(request.POST or None)
        if remark_form.is_valid():
            remark = remark_form.save(commit=False)
            remark.user = request.user
            remark.task = task
            remark.save()
            return redirect("taskers:taskdetail", task.slug)
        if request.user.is_superuser:
            admin_form = AdminTaskForm(request.POST or None, instance=task)
            if admin_form.is_valid():
                instance = admin_form.save(commit=False)
                instance.save()
                messages.add_message(request, messages.SUCCESS,
                                     'Task successfully updated.')
                return redirect("taskers:taskdetail", task.slug)
        else:
            form = self.form_class(request.POST or None, instance=task)
            if form.is_valid():
                instance = form.save(commit=False)
                # instance.user = request.user
                instance.save()
                messages.add_message(request, messages.SUCCESS,
                                     'Task successfully updated.')
                return redirect("taskers:taskdetail", task.slug)
        context = {'form': form, 'instance': task}
        return render(request, self.template_name, context)


class DeleteTaskView(View):
    template_name = 'task_delete_template.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        task_slug = kwargs.get('slug')
        task = get_object_or_404(Task, slug=task_slug)
        context = {
            'task': task
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        task_slug = kwargs.get('slug')
        task = get_object_or_404(Task, slug=task_slug)
        context = {
            'task': task
        }
        if request.method == "POST":
            task.delete()
            messages.add_message(request, messages.SUCCESS,
                                 'Task successfully deleted.')
            return redirect("taskers:userview")
        return render(request, self.template_name, context)


@login_required()
def delete_note(request, pk):
    note = get_object_or_404(TaskRemark, pk=pk)
    note.delete()
    messages.add_message(request, messages.SUCCESS,
                         'Note successfully deleted.')
    return redirect("taskers:taskdetail", note.task.slug)


class TaskPriorityView(View):
    template_name = 'priority_task_template.html'

    def get(self, request, *args, **kwargs):
        # tasks_type = kwargs.get('')
        tasks = Task.objects.filter(is_priority=True)
        context = {'tasks': tasks}
        return render(request, self.template_name, context)

class CompletedTasksView(View):
    template_name = 'completed_task_template.html'

    def get(self, request, *args, **kwargs):
        # tasks_type = kwargs.get('')
        if request.user.is_superuser:
            tasks = Task.objects.filter(is_done=True)
        else:
            tasks = Task.objects.filter(user=request.user).filter(is_done=True)
        context = {'tasks': tasks}
        return render(request, self.template_name, context)
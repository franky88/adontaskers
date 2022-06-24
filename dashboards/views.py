from django.shortcuts import render, get_object_or_404, redirect
from tasks.models import Task, TaskCategory, TaskType, TaskRemark
from tasks.forms import RemarksForm, TaskForm, AdminTaskForm
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.utils import timezone
# Create your views here.
class DashboardView(View):
    form_class = TaskForm
    today = timezone.now()
    template_name = 'tasks_summary.html'
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def get(self, request, *args, **kwargs):
        active_users = User.objects.filter(is_active=True)
        designer_points = active_users.filter(task__is_done=True).annotate(total_points=Sum('task__task_category__task_point') + Sum('task__task_type__task_point'))
        tasks_this_month = Task.objects.filter(is_done=True).filter(updated__year=str(self.today.year), updated__month=str(self.today.month))
        on_progress_priority_tasks = Task.objects.filter(user=request.user).filter(is_done=False).filter(is_priority=True)
        on_progress_priority_tasks_total = Task.objects.filter(user=request.user).filter(is_done=False)
        completed = Task.objects.filter(user=request.user).filter(is_done=True)
        task_cats = TaskCategory.objects.all()
        if request.user.is_superuser:
            form = AdminTaskForm(request.POST or None)
        else:
            form = self.form_class()
        context = {
            'prioritytasks': on_progress_priority_tasks,
            "total_tasks": on_progress_priority_tasks_total,
            'users': active_users,
            'completed': completed,
            'done_tasks_this_month': tasks_this_month,
            'month': self.today.month,
            'year': self.today.year,
            'task_cats': task_cats,
            'designer_points': designer_points,
            'form': form
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
                return redirect("dashboards:dashboard")
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Task successfully created.')
            return redirect("dashboards:dashboard")
        return render(request, self.template_name, {'form': form})

class TaskCategoryView(View):
    today = timezone.now()
    template_name = 'tasks_category_view.html'
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def get(self, request, *args, **kwargs):
        task_name = kwargs.get('name')
        task_cat = get_object_or_404(TaskCategory, name=task_name)
        context = {
            'title': 'tasks category',
            'task_cat': task_cat
        }
        return render(request, self.template_name, context)

class UserView(View):
    template_name = 'user_view.html'
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def get(self, request, *args, **kwargs):
        user_name = kwargs.get('username')
        user = get_object_or_404(User, username=user_name)
        context = {
            'title': 'designer details',
            'user': user
        }
        return render(request, self.template_name, context)
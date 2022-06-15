from django.shortcuts import render
from tasks.models import Task, TaskCategory, TaskType, TaskRemark
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
# Create your views here.
class DashboardView(View):
    template_name = 'tasks_summary.html'
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def get(self, request, *args, **kwargs):
        users = User.objects.filter(is_active=True)
        on_progress_priority_tasks = Task.objects.filter(is_done=False).filter(is_priority=True)
        on_progress_priority_tasks_total = Task.objects.filter(is_done=False).filter(is_priority=True).count()
        context = {
            'tasks': on_progress_priority_tasks,
            "total_tasks": on_progress_priority_tasks_total,
            'users': users
            }
        return render(request, self.template_name, context)
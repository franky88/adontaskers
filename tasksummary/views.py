from django.shortcuts import render, get_object_or_404
from django.views import View
from tasks.models import Task, TaskCategory, TaskType, TaskRemark
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

class TasksSummaryView(View):
    template_name = 'tasks_summary.html'
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def get(self, request, *args, **kwargs):
        on_progress_priority_tasks = Task.objects.filter(is_done=False).filter(is_priority=True)
        on_progress_priority_tasks_total = Task.objects.filter(is_done=False).filter(is_priority=True).count()
        context = {'tasks': on_progress_priority_tasks, "total_tasks": on_progress_priority_tasks_total}
        return render(request, self.template_name, context)
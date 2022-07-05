from django.shortcuts import render, get_object_or_404, redirect
from tasks.models import Task, TaskCategory, TaskType, TaskRemark
from tasks.forms import RemarksForm, TaskForm, AdminTaskForm
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Max, Min, F, Count
from django.db.models.functions import TruncMonth
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.utils import timezone
import calendar
# Create your views here.
class DashboardView(View):
    form_class = TaskForm
    today = timezone.now()
    template_name = 'tasks_summary.html'
    year, month = today.year, today.month
    last_day_of_the_month = calendar.monthrange(year, month)[1]
    monthly_range = str(today.year)+"-"+str(today.month)+"-"+"1", str(today.year)+"-"+str(today.month)+"-"+str(last_day_of_the_month)
    print(last_day_of_the_month)
    print(monthly_range)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def get(self, request, *args, **kwargs):
        active_users = User.objects.filter(is_active=True)
        designer_points = User.objects.filter(task__is_done=True).annotate(total_points=Sum('task__task_category__task_point') + Sum('task__task_type__task_point')).order_by('-total_points')
        tasks_this_month = Task.objects.filter(is_done=True).filter(updated__year=self.today.year, updated__month=self.today.month)
        # tasks_this_month = Task.objects.filter(is_done=True).filter(updated__range=[str(self.today.year)+"-"+str(self.today.month)+"-"+"1", str(self.today.year)+"-"+str(self.today.month)+"-"+str(self.last_day_of_the_month)])
        user_total_points = User.objects.filter(username=request.user).filter(task__is_done=True).aggregate(total_sum=Sum('task__task_category__task_point') + Sum('task__task_type__task_point'))
        on_progress_priority_tasks = Task.objects.filter(user=request.user).filter(is_done=False).filter(is_priority=True)
        on_progress_priority_tasks_total = Task.objects.filter(user=request.user).filter(is_done=False)
        completed = Task.objects.filter(user=request.user).filter(is_done=True)
        total_completed = Task.objects.filter(is_done=True)
        task_cats = TaskCategory.objects.all()
        # print(user_total_points.total)
        if request.user.is_superuser:
            form = AdminTaskForm(request.POST or None)
        else:
            form = self.form_class()
        context = {
            'today': self.today,
            'prioritytasks': on_progress_priority_tasks,
            "total_tasks": on_progress_priority_tasks_total,
            'users': active_users,
            'completed': completed,
            'done_tasks_this_month': tasks_this_month,
            'month': self.today.month,
            'year': self.today.year,
            'task_cats': task_cats,
            'designer_points': designer_points,
            'form': form,
            'user_total_points': user_total_points,
            'total_completed': total_completed
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
    today = timezone.now()
    yesterday = today - timezone.timedelta(days=1)
    year, month = today.year, today.month
    last_day_of_the_month = calendar.monthrange(year, month)[1]
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def get(self, request, *args, **kwargs):
        user_name = kwargs.get('username')
        user = get_object_or_404(User, username=user_name)
        designer_points = User.objects.filter(username=user.username).filter(task__is_done=True).annotate(total_points=Sum('task__task_category__task_point') + Sum('task__task_type__task_point'))[0]
        designer_points_month = Task.objects.filter(user__username=user.username).filter(is_done=True).filter(updated__year=str(self.today.year), updated__month=str(self.today.month)).aggregate(total_points=Sum('task_category__task_point') + Sum('task_type__task_point'))
        completed_tasks = Task.objects.filter(is_done=True).filter(user__username=user.username).filter(updated__year=str(self.today.year), updated__month=str(self.today.month))
        task_cat = TaskCategory.objects.filter(TaskCategory__user__username=user.username).filter(TaskCategory__is_done=True).annotate(total=Count('TaskCategory', distinct=True))
        task_type = TaskType.objects.filter(TaskType__user__username=user.username).filter(TaskType__is_done=True).annotate(total=Count('TaskType', distinct=True))
        # task_cat = TaskCategory.objects.filter(TaskCategory__user__username=user.username).filter(TaskCategory__is_done=True).filter(TaskCategory__updated__year=self.today.year, TaskCategory__updated__month=self.today.month).annotate(total=Count('TaskCategory', distinct=True))
        # task_type = TaskType.objects.filter(TaskType__user__username=user.username).filter(TaskType__is_done=True).filter(TaskType__updated__year=self.today.year, TaskType__updated__month=self.today.month).annotate(total=Count('TaskType', distinct=True))
        # task_cat = TaskCategory.objects.values(task__user__username=user_name).annotate(month=TruncMonth('task__updated')).values('month').annotate(total=Count('task', distinct=True))
        # task_type = TaskType.objects.filter(task__user__username=user_name).filter(task__is_done=True).filter(task__updated__range=[str(self.today.year)+"-"+str(self.today.month)+"-"+"1", str(self.today.year)+"-"+str(self.today.month)+"-"+str(self.last_day_of_the_month)]).annotate(total=Count('task', distinct=True))
        # task_cat = User.objects.filter(username=user.username).filter(task__is_done=True).filter(task__updated__year=self.today.year, task__updated__month=self.today.month).annotate(total=Count('task__task_category'))
        tasks = Task.objects.filter(user__username=user_name).filter(is_done=True).annotate(total=Count('task_category', distinct=True))
        total_user_tasks = Task.objects.filter(user__username=user_name).filter(is_done=True).count()
        print('today month',self.today.year ,self.today.month)
        context = {
            'title': 'designer details',
            'user': user,
            'task_cat': task_cat,
            'tasks': tasks,
            'task_type': task_type,
            'completed_tasks': completed_tasks,
            'today': self.today,
            'designer_points': designer_points,
            'designer_points_month': designer_points_month,
            'total_user_tasks': total_user_tasks
        }
        return render(request, self.template_name, context)
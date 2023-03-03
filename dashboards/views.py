from django.shortcuts import render, get_object_or_404, redirect
from tasks.models import Task, TaskCategory, TaskType, TaskRemark
from tasks.forms import RemarksForm, TaskForm, AdminTaskForm
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Max, Min, F, Q, Count, DateTimeField, ExpressionWrapper
from django.db.models.functions import TruncMonth, TruncDay
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.utils import timezone
import calendar
import datetime
# Create your views here.
class DashboardView(View):
    form_class = TaskForm
    today = timezone.now()
    template_name = 'tasks_summary.html'
    year, month = today.year, today.month
    last_day_of_the_month = calendar.monthrange(year, month)[1]
    monthly_range = str(today.year)+"-"+str(today.month)+"-"+"1", str(today.year)+"-"+str(today.month)+"-"+str(last_day_of_the_month)
    expression = F('updated')
    wrapped_expression = ExpressionWrapper(expression, output_field=DateTimeField())
    start_date = datetime.date(today.year, today.month, 1)
    end_date = datetime.date(today.year, today.month, today.day)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def get(self, request, *args, **kwargs):
        tasks_per_day = Task.objects.filter(updated__range=(self.start_date, self.end_date)) \
            .filter(is_done=True) \
            .annotate(day=TruncDay(self.wrapped_expression)) \
            .values('day') \
            .annotate(c=Count(F('id'))) \
            .order_by('day')
        active_users = User.objects.filter(is_active=True)
        designers_task_per_day = User.objects.filter(Q(task__is_done=True) & Q(task__updated__date=self.today.date()))\
            .annotate(total=Count('task'))\
            .annotate(total_points=Sum(F('task__task_category__task_point')) + Sum(F('task__task_type__task_point')))
        designer_points = User.objects.filter(Q(is_active=True) & Q(task__is_done=True) & Q(task__updated__year=self.today.year) & Q(task__updated__month=self.today.month))\
            .annotate(total_points=Sum(F('task__task_category__task_point')) + Sum(F('task__task_type__task_point')))\
            .order_by('-total_points')

        def top_designer():
            if designer_points.count() == 0:
                return 0
            else:
                top_designer_points = designer_points[0]
                return top_designer_points

        print('sample', top_designer())
        tasks_this_month = Task.objects.filter(is_done=True) \
            .filter(updated__year=self.today.year, updated__month=self.today.month)
        # tasks_this_month = Task.objects.filter(is_done=True)\
        # .filter(updated__range=[str(self.today.year)+"-"+str(self.today.month)+"-"+"1", str(self.today.year)+"-"+str(self.today.month)+"-"+str(self.last_day_of_the_month)])
        
        user_total_points = User.objects.filter(username=request.user) \
            .filter(task__is_done=True) \
            .aggregate(total_sum=Sum('task__task_category__task_point') + Sum('task__task_type__task_point'))
        on_progress_priority_tasks = Task.objects.filter(user=request.user) \
            .filter(is_done=False).filter(is_priority=True)
        on_progress_priority_tasks_total = Task.objects.filter(user=request.user) \
            .filter(is_done=False)
        completed = Task.objects.filter(Q(user=request.user) and Q(is_done=True)) \
            .filter(updated__year=self.today.year, updated__month=self.today.month)
        total_completed = Task.objects.filter(is_done=True)\
            .filter(updated__year=self.today.year, updated__month=self.today.month)
        task_cats = TaskCategory.objects.all()
        user_tasks_per_day = Task.objects.filter(updated__range=[self.start_date, self.end_date]) \
            .filter(is_done=True) \
            .filter(user=request.user) \
            .annotate(day=TruncDay(self.wrapped_expression)) \
            .values('day') \
            .annotate(c=Count(F('id'))) \
            .order_by('day')
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
            'total_completed': total_completed,
            'tasks_per_day': tasks_per_day,
            'user_tasks_per_day': user_tasks_per_day,
            'designers_task_per_day': designers_task_per_day,
            'top_designer_points': top_designer()
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
    start_date = datetime.date(today.year, today.month, 1)
    end_date = datetime.date(today.year, today.month, today.day)
    expression = F('updated') - timezone.timedelta(hours=6)
    wrapped_expression = ExpressionWrapper(expression, output_field=DateTimeField())
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def get(self, request, *args, **kwargs):
        user_name = kwargs.get('username')
        user = get_object_or_404(User, username=user_name)
        designer_points = User.objects.filter(username=user.username) \
            .filter(task__is_done=True) \
            .annotate(total_points=Sum('task__task_category__task_point') + Sum('task__task_type__task_point'))[0]
        designer_points_month = Task.objects.filter(user__username=user.username) \
            .filter(is_done=True).filter(updated__year=self.today.year, updated__month=self.today.month) \
            .aggregate(total_points=Sum('task_category__task_point') + Sum('task_type__task_point'))
        completed_tasks = Task.objects.filter(is_done=True) \
            .filter(user__username=user.username) \
            .filter(updated__range=(self.start_date, self.end_date))
        # task_cat = TaskCategory.objects.filter(TaskCategory__is_done=True).filter(TaskCategory__user__username=user.username).annotate(total=Count('TaskCategory', distinct=True))
        # task_type = TaskType.objects.filter(TaskType__is_done=True).filter(TaskType__user__username=user.username).annotate(total=Count('TaskType', distinct=True))
        # task_cat = TaskCategory.objects.filter(TaskCategory__is_done=True).filter(TaskCategory__updated__year=self.today.year, TaskCategory__updated__month=self.today.month).filter(TaskCategory__user__username=user.username).annotate(total=Count('TaskCategory', distinct=True))
        # task_type = TaskType.objects.filter(TaskType__is_done=True).filter(TaskType__updated__year=self.today.year, TaskType__updated__month=self.today.month).filter(TaskType__user__username=user.username).annotate(total=Count('TaskType', distinct=True))
        task_cat = TaskCategory.objects.filter(task__is_done=True) \
            .filter(task__updated__range=(self.start_date, self.end_date)) \
            .filter(task__user=user) \
            .annotate(total=Count('task', distinct=True))
        task_type = TaskType.objects.filter(task__is_done=True) \
            .filter(task__updated__range=(self.start_date, self.end_date)) \
            .filter(task__user=user).annotate(total=Count('task', distinct=True))
        # task_cat = User.objects.filter(username=user.username).filter(task__is_done=True).filter(task__updated__year=self.today.year, task__updated__month=self.today.month).annotate(total=Count('task__task_category'))
        tasks = Task.objects.filter(user__username=user_name) \
            .filter(Q(is_done=False) | Q(updated__date=self.today.date())) \
            .annotate(total=Count('task_category', distinct=True))
        total_user_tasks = Task.objects.filter(user__username=user_name) \
            .filter(is_done=True).count()
        # print('today month',self.start_date, self.end_date)
        # print('user', Task.objects.filter(is_done=True).filter(user__username=user.username).filter(updated__range=(self.start_date, self.end_date)).annotate(total=Count('task_category', distinct=True)))
        tc = Task.objects.filter(updated__range=(self.start_date, self.end_date)) \
            .filter(is_done=True) \
            .filter(user__username=user.username) \
            .annotate(total=Count('pk', distinct=True))
        tasks_per_day = Task.objects.filter(updated__range=(self.start_date, self.end_date)) \
            .filter(is_done=True) \
            .filter(user=user) \
            .annotate(day=TruncDay(self.wrapped_expression)) \
            .values('day') \
            .annotate(c=Count(F('id'))) \
            .order_by('day')
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
            'total_user_tasks': total_user_tasks,
            'tc': tc,
            'tasks_per_day': tasks_per_day
        }
        return render(request, self.template_name, context)
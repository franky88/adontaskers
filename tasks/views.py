from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
import datetime
from django.utils import timezone
from django.db.models import Sum 
from django.db.models import Q
from .models import Task, TaskRemark, TaskCategory, TaskType
from .forms import RemarksForm, TaskForm, AdminTaskForm
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from dashboards.filters import TaskFilter
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
            tasks = Task.objects.filter(Q(is_done=False) | Q(updated__date=today.date()))
            # priority_tasks_today = Task.objects.filter(updated__date=today.date()).filter(is_priority=True).filter(is_done=False)
            # priority_tasks_yesterday = Task.objects.filter(updated__date=yesterday.date()).filter(is_priority=True).filter(is_done=False)
            priority_tasks = Task.objects.filter(is_done=False).filter(is_priority=True)
            # wip_tasks_today = Task.objects.filter(updated__date=today.date()).filter(is_done=False)
            # wip_tasks_yesterday = Task.objects.filter(updated__date=yesterday.date()).filter(is_done=False)
            wip_tasks = Task.objects.filter(is_done=False)
            # completed_tasks_today = Task.objects.filter(updated__date=today.date()).filter(is_done=True)
            # completed_tasks_yesterday = Task.objects.filter(updated__date=yesterday.date()).filter(is_done=True)
            completed_tasks = Task.objects.filter(is_done=True)\
                .filter(updated__year=today.year, updated__month=today.month)
            print('total today', completed_tasks.count())
            tasks_type = TaskType.objects.filter(Q(task__updated__date=today.date()) | Q(task__is_done=False))\
                .annotate(total_type=Count('task', distinct=True))
            tasks_categories = TaskCategory.objects.filter(Q(task__updated__date=today.date()) | Q(task__is_done=False))\
                .annotate(total_categories=Count('task', distinct=True))
            form = AdminTaskForm(request.POST or None)
        else:
            tasks = Task.objects.all().filter(user=request.user).filter(is_done=False)
            # priority_tasks_today = Task.objects.filter(user=request.user).filter(updated__date=today.date()).filter(is_priority=True).filter(is_done=False)
            # priority_tasks_yesterday = Task.objects.filter(user=request.user).filter(updated__date=yesterday.date()).filter(is_done=False).filter(is_priority=True)
            priority_tasks = Task.objects.filter(user=request.user).filter(is_done=False).filter(is_priority=True)
            # wip_tasks_today = Task.objects.filter(user=request.user).filter(updated__date=today.date()).filter(is_done=False)
            # wip_tasks_yesterday = Task.objects.filter(user=request.user).filter(updated__date=yesterday.date()).filter(is_done=False)
            wip_tasks = Task.objects.filter(user=request.user).filter(is_done=False)
            # completed_tasks_today = Task.objects.filter(user=request.user).filter(updated__date=today.date()).filter(is_done=True)
            # completed_tasks_yesterday = Task.objects.filter(user=request.user).filter(updated__date=yesterday.date()).filter(is_done=True)
            completed_tasks = Task.objects.filter(user=request.user).filter(is_done=True)\
                .filter(updated__year=today.year, updated__month=today.month)
            tasks_type = TaskType.objects.filter(Q(task__updated__date=today.date()))\
                .filter(Q(task__user=request.user) & Q(task__is_done=False))\
                .annotate(total_type=Count('task', distinct=True))
            for task in tasks_type:
                print(task.total_type, task)
            tasks_categories = TaskCategory.objects.filter(Q(task__updated__date=today.date()))\
                .filter(Q(task__user=request.user) & Q(task__is_done=False))\
                .annotate(total_categories=Count('task', distinct=True))
            form = self.form_class()
        if request.user.has_perm('auth.view_user'):
            completed_tasks = Task.objects.filter(is_done=True)\
                .filter(updated__year=today.year, updated__month=today.month)
            wip_tasks = Task.objects.filter(is_done=False)
            priority_tasks = Task.objects.filter(is_done=False).filter(is_priority=True)
        query = request.GET.get('q')
        if query:
            tasks = tasks.filter(
                Q(user__username__startswith=query) |
                Q(task_type__name__startswith=query) |
                Q(task_category__name__startswith=query) |
                Q(name__startswith=query) |
                Q(paradise_link__icontains=query) |
                Q(check_list__name__icontains=query)
            ).distinct()
        # for p in request.user.has_perms:
        #     print(p)

        # paginator = Paginator(tasks, tasks.count())
        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)
        # print(request.user.has_perm('auth.view_user'))
        context = {
                    'form': form,
                    'tasks': tasks,
                    'today': today,
                    'yesterday': yesterday,
                    # 'priority_tasks_today': priority_tasks_today,
                    # 'wip_tasks_today': wip_tasks_today,
                    # 'completed_tasks_today': completed_tasks_today,
                    # 'priority_tasks_yesterday': priority_tasks_yesterday,
                    # 'wip_tasks_yesterday': wip_tasks_yesterday,
                    # 'completed_tasks_yesterday': completed_tasks_yesterday,
                    'priority_tasks': priority_tasks,
                    'completed_tasks': completed_tasks,
                    'wip_tasks': wip_tasks,
                    'tasks_type': tasks_type,
                    'tasks_categories': tasks_categories
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
    if request.user.username == note.user.username or request.user.is_superuser:
        note.delete()
        messages.add_message(request, messages.SUCCESS,
                            'Note successfully deleted.')
        return redirect("taskers:taskdetail", note.task.slug)
    else:
        messages.add_message(request, messages.WARNING,
                            'Request denied.')
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

class AllPriorityTaskView(View):
    today = timezone.now()
    yesterday = today - timezone.timedelta(days=1)
    template_name = 'tasks_filter_template.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.has_perm('auth.view_user'):
            tasks = Task.objects.filter(Q(is_priority=True) & Q(is_done=False))
            categories = TaskCategory.objects.filter(Q(task__is_priority=True) & Q(task__is_done=False))\
                .annotate(count=Count('task'))
        else:
            tasks = Task.objects.filter(user=request.user).filter(is_priority=True).filter(is_done=False)
            categories = TaskCategory.objects.all()\
                .filter(Q(task__is_priority=True) & Q(task__is_done=False))
        query = request.GET.get('q')
        if query:
            tasks = tasks.filter(
                Q(user__username__startswith=query) |
                Q(task_type__name__startswith=query) |
                Q(task_category__name__startswith=query) |
                Q(name__startswith=query) |
                Q(paradise_link__icontains=query) |
                Q(check_list_link__icontains=query)
            ).distinct()
        paginator = Paginator(tasks, tasks.count())
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'tasks': tasks, 'title': 'priority tasks', 'page_obj': page_obj, 'categories': categories}
        return render(request, self.template_name, context)

class AllWIPTaskView(View):
    today = timezone.now()
    yesterday = today - timezone.timedelta(days=1)
    template_name = 'tasks_filter_template.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.has_perm('auth.view_user'):
            tasks = Task.objects.filter(is_done=False)
            categories = TaskCategory.objects.filter(Q(task__is_done=False)\
                & Q(task__updated__year=self.today.year)\
                & Q(task__updated__month=self.today.month))\
                .annotate(count=Count('task'))
        else:
            tasks = Task.objects.filter(user=request.user).filter(is_done=False)
            categories = TaskCategory.objects.filter(Q(task__user=request.user)\
                & Q(task__is_done=False)\
                & Q(task__updated__year=self.today.year)\
                & Q(task__updated__month=self.today.month))\
                .annotate(count=Count('task'))
        query = request.GET.get('q')
        if query:
            tasks = tasks.filter(
                Q(user__username__startswith=query) |
                Q(task_type__name__startswith=query) |
                Q(task_category__name__startswith=query) |
                Q(name__startswith=query) |
                Q(paradise_link__icontains=query) |
                Q(check_list__name__icontains=query)
            ).distinct()
        paginator = Paginator(tasks, tasks.count())
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'tasks': tasks, 'title': 'work in progress tasks', 'page_obj': page_obj, 'categories': categories}
        return render(request, self.template_name, context)

class AllCompletedTaskView(View):
    today = timezone.now()
    yesterday = today - timezone.timedelta(days=1)
    template_name = 'tasks_filter_template.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.has_perm('auth.view_user'):
            tasks = Task.objects.filter(is_done=True)\
                .filter(updated__year=self.today.year, updated__month=self.today.month)
            categories = TaskCategory.objects.filter(Q(task__is_done=True)\
                & Q(task__updated__year=self.today.year)\
                & Q(task__updated__month=self.today.month))\
                .annotate(count=Count('task'))
            type = TaskType.objects.filter(Q(task__is_done=True)\
                & Q(task__updated__year=self.today.year)\
                & Q(task__updated__month=self.today.month))\
                .annotate(count=Count('task'))
        else:
            tasks = Task.objects.filter(user=request.user).filter(is_done=True)\
                .filter(updated__year=self.today.year, updated__month=self.today.month)
            categories = TaskCategory.objects.filter(Q(task__user=request.user) \
                & Q(task__is_done=True)\
                & Q(task__updated__year=self.today.year)\
                & Q(task__updated__month=self.today.month))\
                .annotate(count=Count('task'))
            type = TaskType.objects.filter(Q(task__user=request.user)\
                & Q(task__is_done=True)\
                & Q(task__updated__year=self.today.year)\
                & Q(task__updated__month=self.today.month))\
                .annotate(count=Count('task'))
        # f = TaskFilter(request.GET, queryset=tasks)
        query = request.GET.get('q')
        if query:
            tasks = tasks.filter(
                Q(user__username__startswith=query) |
                Q(task_type__name__startswith=query) |
                Q(task_category__name__startswith=query) |
                Q(name__startswith=query) |
                Q(paradise_link__icontains=query) |
                Q(check_list__name__icontains=query) 
            ).distinct()
        paginator = Paginator(tasks, tasks.count())
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'tasks': tasks, 'title': 'completed tasks', 'page_obj': page_obj, 'categories': categories, 'type': type}
        return render(request, self.template_name, context)

class TasksArchiveView(View):
    today = timezone.now()
    yesterday = today - timezone.timedelta(days=1)
    template_name = 'tasks_archive_template.html'

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.filter(is_done=True)
        categories = TaskCategory.objects.filter(Q(task__is_done=True))\
            .annotate(count=Count('task'))
        type = TaskType.objects.filter(Q(task__is_done=True))\
            .annotate(count=Count('task'))
        print(tasks.count())
        query = request.GET.get('q')
        if query:
            tasks = tasks.filter(
                Q(user__username__startswith=query) |
                Q(task_type__name__startswith=query) |
                Q(task_category__name__startswith=query) |
                Q(name__startswith=query) |
                Q(paradise_link__icontains=query) |
                Q(check_list__name__icontains=query)
            ).distinct()
        paginator = Paginator(tasks, tasks.count())
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'tasks': tasks, 'title': 'archived tasks', 'page_obj': page_obj, 'categories': categories, 'type': type,}
        return render(request, self.template_name, context)

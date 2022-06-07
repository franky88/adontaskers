# def task_filter(request):
#     today = timezone.now()
#     yesterday = timezone.now() - timezone.timedelta(days=1)
#     year_today = timezone.now().year
#     if request.user.is_anonymous:
#         redirect('/admin')
#     elif request.user.is_superuser:
#         done_tasks_today = Task.objects.filter(
#             is_done=True).filter(updated__date=today.date()).count()
#         task_by_year = Task.objects.filter(
#             is_done=True).filter(updated__year__lte=str(year_today))
#         task_yesterday = Task.objects.filter(
#             is_done=True).filter(updated__date=yesterday.date()).count()
#         user_tasks_count = Task.objects.all().filter(is_done=False).count()
#         done_tasks = Task.objects.all().filter(is_done=True).count()
#         tasks_priority = Task.objects.all().filter(
#             is_priority=True).filter(is_done=False).count()
#     else:
#         # user_tasks = Task.objects.filter(
#         #     user=request.user).filter(is_done=False)
#         user_tasks_count = Task.objects.filter(
#             user=request.user).filter(is_done=False).count()
#         done_tasks = Task.objects.filter(
#             user=request.user).filter(is_done=True).count()
#         tasks_priority = Task.objects.filter(
#             user=request.user).filter(is_priority=True).filter(is_done=False).count()
#     context = {
#         "title": "task filter",
#         # "tasks": user_tasks,
#         "done": done_tasks,
#         "tasks_priority": tasks_priority,
#         "user_tasks_count": user_tasks_count,
#         "task_by_year": task_by_year,
#         "task_yesterday": task_yesterday,
#         "done_tasks_today": done_tasks_today
#     }
#     return render(request, 'includes/task_filter.html', context)


# def home(request):
#     today = timezone.now()
#     yesterday = timezone.now() - timezone.timedelta(days=1)
#     year_today = timezone.now().year

#     if request.user.is_anonymous:
#         redirect('/admin')
#     elif request.user.is_superuser:
#         user_tasks = Task.objects.all().filter(is_done=False)
#         # done_tasks_today = Task.objects.filter(
#         #     is_done=True).filter(updated__date=today.date()).count()
#         # task_by_year = Task.objects.filter(
#         #     is_done=True).filter(updated__year__lte=str(year_today))
#         # task_yesterday = Task.objects.filter(
#         #     is_done=True).filter(updated__date=yesterday.date()).count()
#         # user_tasks_count = Task.objects.all().filter(is_done=False).count()
#         # done_tasks = Task.objects.all().filter(is_done=True).count()
#         # tasks_priority = Task.objects.all().filter(
#         #     is_priority=True).filter(is_done=False).count()
#         # total_points = done_tasks.aggregate(
#         #     total=Sum('task_category__task_point'))
#         # print("Updated ", user_tasks.updated.date())
#     else:
#         user_tasks = Task.objects.filter(
#             user=request.user).filter(is_done=False)
#         # user_tasks_count = Task.objects.filter(
#         #     user=request.user).filter(is_done=False).count()
#         # done_tasks = Task.objects.filter(
#         #     user=request.user).filter(is_done=True).count()
#         # tasks_priority = Task.objects.filter(
#         #     user=request.user).filter(is_priority=True).filter(is_done=False).count()
#     # for data in request.user.task_set.all():
#     #     print(data.updated.year)
#     context = {
#         "title": "task list",
#         "tasks": user_tasks,
#         # "done": done_tasks,
#         # "tasks_priority": tasks_priority,
#         # "user_tasks_count": user_tasks_count,
#         # "task_by_year": task_by_year,
#         # "task_yesterday": task_yesterday,
#         # "done_tasks_today": done_tasks_today
#     }
#     return render(request, 'home.html', context)


# def priority_task(request):
#     if request.user.is_anonymous:
#         return redirect('/admin')
#     elif request.user.is_superuser:
#         tasks_priority = Task.objects.all().filter(
#             is_priority=True).filter(is_done=False)
#     else:
#         tasks_priority = Task.objects.filter(
#             user=request.user).filter(is_priority=True).filter(is_done=False)
#     context = {
#         "title": "task list",
#         # "tasks": user_tasks,
#         # "done": done_tasks,
#         "tasks_priority": tasks_priority,
#     }
#     return render(request, 'priority_tasks.html', context)


# def completed_task(request):
#     if request.user.is_anonymous:
#         return redirect('/admin')
#     elif request.user.is_superuser:
#         done_tasks = Task.objects.all().filter(is_done=True)
#     else:
#         done_tasks = Task.objects.filter(
#             user=request.user).filter(is_done=True)
#     context = {
#         "title": "task list",
#         # "tasks": user_tasks,
#         "done": done_tasks,
#         # "tasks_priority": tasks_priority,
#     }
#     return render(request, 'completed_tasks.html', context)


# def completed_task_today(request):
#     today = timezone.now()
#     if request.user.is_anonymous:
#         return redirect('/admin')
#     elif request.user.is_superuser:
#         done_tasks = Task.objects.filter(
#             is_done=True).filter(updated__date=today.date())
#     else:
#         done_tasks = Task.objects.filter(
#             user=request.user).filter(is_done=True).filter(updated__date=today.date())
#     context = {
#         "title": "task list",
#         # "tasks": user_tasks,
#         "done": done_tasks,
#         # "tasks_priority": tasks_priority,
#     }
#     return render(request, 'completed_task_today.html', context)


# def create_task(request):
#     if request.user.is_superuser:
#         form = AdminTaskForm(request.POST or None,
#                              request.FILES or None)
#         if request.method == "POST":
#             if form.is_valid():
#                 instance = form.save(commit=False)
#                 instance.save()
#                 return redirect('taskers:home')
#             else:
#                 form = TaskForm(request.POST or None,
#                                 request.FILES or None)
#     else:
#         form = TaskForm(request.POST or None,
#                         request.FILES or None)
#         if request.method == "POST":
#             if form.is_valid():
#                 instance = form.save(commit=False)
#                 instance.user = request.user
#                 instance.save()
#                 return redirect('taskers:home')
#             else:
#                 form = TaskForm(request.POST or None,
#                                 request.FILES or None)
#     context = {
#         "title": "create tast",
#         "form": form
#     }
#     return render(request, 'create_task.html', context)


# def update_task(request, slug):
#     task = get_object_or_404(Task, slug=slug)
#     remarks = TaskRemark.objects.filter(pk=task.pk)
#     remark_form = RemarksForm(request.POST or None)
#     if task.is_done:
#         return redirect('taskers:home')
#     if remark_form.is_valid():
#         instance = remark_form.save(commit=False)
#         instance.user = request.user
#         instance.task = task
#         instance.save()
#         return redirect("taskers:update", task.slug)

#     if request.user.is_superuser:
#         form = AdminTaskForm(request.POST or None,
#                              request.FILES or None, instance=task)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             # instance.user = request.user
#             instance.save()
#             return redirect('taskers:home')
#     else:
#         form = TaskForm(request.POST or None,
#                         request.FILES or None, instance=task)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.user = request.user
#             instance.save()
#             return redirect('taskers:home')
#     context = {
#         "title": "update tast",
#         "task": task,
#         "form": form,
#         "remarks": remarks,
#         "remark_form": remark_form
#     }
#     return render(request, 'update_task.html', context)


# def task_details(request, slug):
#     task = get_object_or_404(Task, slug=slug)
#     if not task.is_done:
#         return redirect("taskers:update", task.pk)
#     context = {
#         "title": "task details",
#         "instance": task
#     }
#     return render(request, "task_details.html", context)


# def delete_task(request, slug):
#     task = get_object_or_404(Task, slug=slug)
#     if request.method == "POST":
#         task.delete()
#         messages.add_message(request, messages.SUCCESS,
#                              'Task successfully deleted.')
#         return redirect('taskers:home')
#     context = {
#         "title": "delete tast",
#         "task": task
#     }
#     return render(request, 'delete_task.html', context)


# def delete_note(request, pk):
#     note = get_object_or_404(TaskRemark, pk=pk)
#     # if request.method == "POST":
#     note.delete()
#     messages.add_message(request, messages.SUCCESS,
#                          'Note successfully deleted.')
#     return redirect("taskers:update", note.task.slug)

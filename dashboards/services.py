from django.db.models import Sum

# request user points
def designer_points(self, username, model):
    points = model.objects.filter(user=username)\
        .filter(task__is_done=True)\
        .annotate(total_points=Sum('task__task_category__task_point') + Sum('task__task_type__task_point'))
    return points
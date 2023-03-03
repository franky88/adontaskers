from dataclasses import fields
import django_filters
from tasks.models import Task, TaskCategory, TaskType, TaskRemark

class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = {
            'user',
            'task_type',
            'task_category',
            'name',
            'paradise_link',
            # 'check_list_link',
            'is_priority',
            'is_done',
            # 'created': ['exact', 'year__gt'],
            # 'updated': ['exact', 'year__gt'],
        }
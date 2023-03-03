from pyexpat import model
from django import forms
from .models import Task, TaskCategory, TaskType, TaskRemark


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'name',
            'task_type',
            'task_category',
            'paradise_link',
            'check_list',
            # 'task_note',
            'is_priority',
            'is_done',
        ]


class AdminTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'user',
            'name',
            'task_type',
            'task_category',
            'paradise_link',
            'check_list',
            # 'task_note',
            'is_priority',
            'is_done',
        ]


# class OnDutyForm(forms.ModelForm):
#     class Meta:
#         model = OnDuty
#         fields = [
#             'on_duty'
#         ]


class RemarksForm(forms.ModelForm):
    class Meta:
        model = TaskRemark
        fields = [
            'remarks',
        ]

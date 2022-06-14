from django.contrib import admin
from .models import Task, TaskCategory, TaskType, TaskRemark
# Register your models here.

admin.site.site_header = "AD ON GROUP"

admin.site.register(Task)
admin.site.register(TaskCategory)
admin.site.register(TaskType)
admin.site.register(TaskRemark)

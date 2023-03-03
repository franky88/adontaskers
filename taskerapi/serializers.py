from django.contrib.auth.models import User
from tasks.models import Task, TaskType
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['url', 'name', 'user', 'is_done', 'is_priority', 'created', 'updated', 'paradise_link', 'task_type']

class TaskTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskType
        fields = ['url', 'name', 'task_point']
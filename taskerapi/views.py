from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer, TaskSerializer, TaskTypeSerializer
from tasks.models import Task, TaskType
# Create your views here.
# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskTypeViewSet(viewsets.ModelViewSet):
    queryset = TaskType.objects.all()
    serializer_class = TaskTypeSerializer
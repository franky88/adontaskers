from django.urls import path
from . import views

app_name = "tasksummary"
urlpatterns = [
    path('', views.TasksSummaryView.as_view(), name="tasksummary"),
]
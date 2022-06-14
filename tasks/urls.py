from django.urls import path
from . import views

app_name = "taskers"
urlpatterns = [
    # path('', views.home, name="home"),
    path('tasks/', views.TaskListView.as_view(), name="userview"),
    path('tasks/completed', views.CompletedTasksView.as_view(), name="completedtasks"),
    path('tasks/<slug>', views.TaskUpdateView.as_view(), name="taskdetail"),
    path('tasks/delete/<slug>', views.DeleteTaskView.as_view(), name="taskdelete"),
    # path('priority/', views.priority_task, name="priority"),
    # path('completed/', views.completed_task, name="completed"),
    # path('completed-today/', views.completed_task_today, name="completedToday"),
    # path('create/', views.create_task, name="create"),
    # path('update/<slug>', views.update_task, name="update"),
    # path('details/<slug>', views.task_details, name="task_detail"),
    # path('delete/<slug>', views.delete_task, name="delete"),
    path('delete-note/<pk>', views.delete_note, name="delete_note"),
    # path('on-duty/', views.on_duty, name="on_duty"),
]

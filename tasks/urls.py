from django.urls import path
from . import views

app_name = "taskers"
urlpatterns = [
    # path('', views.home, name="home"),
    path('tasks/', views.TaskListView.as_view(), name="userview"),
    path('tasks/completed', views.CompletedTasksView.as_view(), name="completedtasks"),
    path('tasks/priority-today', views.TaskTodayView.as_view(), name="tasksprioritytoday"),
    path('tasks/work-in-progress-today', views.WIPTodayView.as_view(), name="workinprogresstoday"),
    path('tasks/completed-today', views.CompletedTodayView.as_view(), name="completedtoday"),
    path('tasks/priority-yesterday', views.PriorityTaskYesterdayView.as_view(), name="taskspriorityyesterday"),
    path('tasks/work-in-progress-yesterday', views.WIPTaskYesterdayView.as_view(), name="wiptaskyesterday"),
    path('tasks/completed-yesterday', views.CompletedTaskYesterdayView.as_view(), name="completedtaskyesterday"),
    path('tasks/all-priority', views.AllPriorityTaskView.as_view(), name="allprioritytasks"),
    path('tasks/all-work-in-progress', views.AllWIPTaskView.as_view(), name="allwiptasks"),
    path('tasks/all-completed', views.AllCompletedTaskView.as_view(), name="allcompletedtasks"),
    path('tasks/<slug>', views.TaskUpdateView.as_view(), name="taskdetail"),
    path('tasks/delete/<slug>', views.DeleteTaskView.as_view(), name="taskdelete"),
    path('delete-note/<pk>', views.delete_note, name="delete_note"),
]

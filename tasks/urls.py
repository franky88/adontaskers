from django.urls import path
from . import views

app_name = "taskers"
urlpatterns = [
    # path('', views.home, name="home"),
    path('', views.TaskListView.as_view(), name="userview"),
    path('completed', views.CompletedTasksView.as_view(), name="completedtasks"),
    path('priority-today', views.TaskTodayView.as_view(), name="tasksprioritytoday"),
    path('work-in-progress-today', views.WIPTodayView.as_view(), name="workinprogresstoday"),
    path('completed-today', views.CompletedTodayView.as_view(), name="completedtoday"),
    path('priority-yesterday', views.PriorityTaskYesterdayView.as_view(), name="taskspriorityyesterday"),
    path('work-in-progress-yesterday', views.WIPTaskYesterdayView.as_view(), name="wiptaskyesterday"),
    path('completed-yesterday', views.CompletedTaskYesterdayView.as_view(), name="completedtaskyesterday"),
    path('all-priority', views.AllPriorityTaskView.as_view(), name="allprioritytasks"),
    path('all-work-in-progress', views.AllWIPTaskView.as_view(), name="allwiptasks"),
    path('all-completed', views.AllCompletedTaskView.as_view(), name="allcompletedtasks"),
    path('task-archived', views.TasksArchiveView.as_view(), name="taskarchived"),
    path('<slug>', views.TaskUpdateView.as_view(), name="taskdetail"),
    path('delete/<slug>', views.DeleteTaskView.as_view(), name="taskdelete"),
    path('delete-note/<pk>', views.delete_note, name="delete_note"),
]

from django.urls import path
from . import views

app_name = "dashboards"
urlpatterns = [
    path('', views.DashboardView.as_view(), name="dashboard"),
    path('<name>', views.TaskCategoryView.as_view(), name="taskcategory"),
    path('users/<username>', views.UserView.as_view(), name="userdetails"),
]
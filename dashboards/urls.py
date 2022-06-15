from django.urls import path
from . import views

app_name = "dashboards"
urlpatterns = [
    path('', views.DashboardView.as_view(), name="dashboard"),
]
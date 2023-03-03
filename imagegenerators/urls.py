from django.urls import path
from . import views

app_name = "imagegenerator"
urlpatterns = [
    path('', views.generate_image, name="generator"),
]
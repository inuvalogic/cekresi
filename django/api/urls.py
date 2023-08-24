from django.urls import path

from . import views

urlpatterns = [
    path('check', views.checkResi, name='cekresi'),
]
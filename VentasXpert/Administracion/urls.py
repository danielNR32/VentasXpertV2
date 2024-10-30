# Administracion/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.administrador_home, name='administrador_home'),
]

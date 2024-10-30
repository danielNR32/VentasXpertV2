# Usuarios_permisos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.usuarios_permisos_home, name='superusuario_home'),
]

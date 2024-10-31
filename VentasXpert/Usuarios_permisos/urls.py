# Usuarios_permisos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='superusuario_home'),  # Ruta para la vista home
    path('logout/', views.logout_view, name='logout'),
    path('usuarios/', views.usuarios, name='usuarios'), 
    path('permisos/', views.permisos, name='permisos'),
    path('roles/', views.roles, name='roles'),
]

# Usuarios_permisos/urls.py
from django.urls import path
from . import views
from utils.decorators import role_required

urlpatterns = [
    path('', views.base, name='superusuario_home'),  # Ruta general
    path('usuarios/', role_required(['SU'])(views.usuarios), name='usuarios'),
    path('permisos/', role_required(['SU'])(views.permisos), name='permisos'),
    path('roles/', role_required(['SU'])(views.roles), name='roles'),
    path('error_permiso/', views.error_permiso, name='error_permiso'),

]

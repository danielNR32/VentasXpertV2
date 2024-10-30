# Administracion/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.administrador_home, name='administrador_home'),
    path('reportes/', views.reportes_home, name='reportes_home'),
    path('inventario/', views.inventario_home, name='inventario_home'),
     path('proovedores/', views.proovedores_home, name='proovedores_home'),
]

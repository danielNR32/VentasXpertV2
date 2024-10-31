# Ventas_caja/urls.py
from django.urls import path
from . import views

urlpatterns = [
  path('homeCajero', views.home, name='cajero_home'),  # Ruta para la vista home
  path('cajero/', views.caja, name='caja'),
  path('cajero2/', views.caja2, name='caja2'),
]

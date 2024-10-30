# Ventas_caja/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.cajero_home, name='cajero_home'),
]

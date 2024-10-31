# Catalogo_productos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo_home, name='catalogo_home'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('infoTienda/', views.infoTienda, name='infoTienda'),
]

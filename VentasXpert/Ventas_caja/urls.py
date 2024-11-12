# Ventas_caja/urls.py
from django.urls import path
from . import views

urlpatterns = [
  path('homeCajero', views.home, name='cajero_home'),  # Ruta para la vista home
  path('cajero/', views.caja, name='caja'),
  path('cajero2/', views.caja2, name='caja2'),
  path('agregar_producto/<int:id>/', views.agregar_producto, name='agregar_producto'),
  path('restar_producto/<int:id>/', views.restar_producto, name='restar_producto'),
  path('sumar_producto/<int:id>/', views.sumar_producto, name='sumar_producto'),
  path('quitar_producto/<int:id>/', views.quitar_producto, name='quitar_producto'),
  path('eliminar_carrito_actual/', views.eliminar_carrito_actual, name='eliminar_carrito_actual'),
  path('generar_ticket_pdf/', views.generar_ticket_pdf, name='generar_ticket_pdf'),
]

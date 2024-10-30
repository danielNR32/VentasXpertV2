# Administracion/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='administrador_home'),  # Ruta para la vista home
    path('dashboard/', views.dashboard, name='dashboard'),
    path('inventario_informacion/', views.informacionInventario, name='informacionInventario'),
    path('inventario_inventario/', views.inventarioInventario, name='inventarioInventario'),
    path('modal-agregar-producto/', views.inventarioAgregra_producto, name='inventarioAgregra_producto'),
    path('inventario-administrar/', views. inventario_administrar, name=' inventario_administrar'),
    path('inventario-administrarAgregar/', views. inventario_admiministrarAgregarProducto, name='inventario_admiministrarAgregarProducto'),
    path('inventario-actualizarProducto/', views. inventario_actualizarProducto, name='inventario_actualizarProducto'), 
    path('reportes/', views.reportes_home, name='reportes_home'),
    path('inventario/', views.inventario_home, name='inventario_home'),
    path('proovedores/', views.proovedores_home, name='proovedores_home'),
]

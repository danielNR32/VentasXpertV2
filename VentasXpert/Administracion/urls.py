# Administracion/urls.py
from django.urls import path
from . import views
from .views import editar_producto_temporal

urlpatterns = [
    path('', views.home, name='administrador_home'),  # Ruta para la vista home
    path('dashboard/', views.dashboard, name='dashboard'),
    path('inventario_informacion/', views.informacionInventario, name='informacionInventario'),
    path('inventario_inventario/', views.inventarioInventario, name='inventarioInventario'),
    path('modal-agregar-producto/', views.inventarioAgregra_producto, name='inventarioAgregra_producto'),
    path('inventario-administrar/', views. inventario_administrar, name=' inventario_administrar'),
    path('inventario-actualizarProducto/', views. inventario_actualizarProducto, name='inventario_actualizarProducto'), 
    path('reportes/', views.reportes_home, name='reportes_home'),
    path('inventario/', views.inventario_home, name='inventario_home'),
    path('proovedores/', views.proovedores_home, name='proovedores_home'),

    ## funcionalidad para guardar en la base de datos
   ## path('agregar_producto/', views.agregar_producto_temporal, name='agregar_producto'),
  

  ##Funcionalidad para agregar nuevo producto
    path('inventario-administrarAgregar/', views.agregar_nuevo_producto, name='inventario_admiministrarAgregarProducto'),
    path('confirmar_inventario/', views.confirmar_inventario, name='confirmar_inventario'),
    path('vista_inventario/', views.vista_inventario, name='vista_inventario'),
    path('vista_inventario2/', views.vista_inventario2, name='vista_inventario2'),
    path('eliminar_producto_temporal/<int:index>/', views.eliminar_producto_temporal, name='eliminar_producto_temporal'),
    ## editar en tabla
    path('editar_producto_temporal/<int:index>/', views.editar_producto_temporal, name='editar_producto_temporal'),

    ##Funcionalidad para agregar stock


    path('surtir_inventario/', views.surtir_inventario, name='surtir_inventario'),
    path('buscar_producto/', views.buscar_producto, name='buscar_producto'),
    path('confirmar_surtido/', views.confirmar_surtido, name='confirmar_surtido'),



    

]

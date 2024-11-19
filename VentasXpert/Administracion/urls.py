# Administracion/urls.py
from django.urls import path
from . import views
from .views import editar_producto_temporal
from utils.decorators import role_required

urlpatterns = [
    path('', views.home, name='administrador_home'),  # Ruta para la vista home
    path('dashboard/', views.dashboard, name='dashboard'),
    path('inventario_informacion/',role_required(['Gerente', 'Administrador', 'SU'])( views.informacion_inventario), name='informacionInventario'),
    path('inventario_inventario/',role_required(['Gerente', 'Administrador', 'SU'])( views.inventarioInventario), name='inventarioInventario'),
    path('modal-agregar-producto/',role_required(['Gerente', 'Administrador', 'SU'])(views.inventarioAgregra_producto), name='inventarioAgregra_producto'),
    path('inventario-administrar/',role_required(['Gerente', 'Administrador', 'SU']) (views. inventario_administrar), name=' inventario_administrar'),
    path('inventario-actualizarProducto/',role_required(['Gerente', 'Administrador', 'SU'])(views. inventario_actualizarProducto), name='inventario_actualizarProducto'), 
    path('reportes/',role_required(['Gerente', 'Administrador', 'SU']) (views.reportes_home), name='reportes_home'),
    path('inventario/', views.inventario_home, name='inventario_home'),
    path('proovedores/', role_required(['Gerente', 'Administrador', 'SU'])(views.proovedores_home), name='proovedores_home'),

    ## funcionalidad para guardar en la base de datos
   ## path('agregar_producto/', views.agregar_producto_temporal, name='agregar_producto'),
  

  ##Funcionalidad para agregar nuevo producto
    path('inventario-administrarAgregar/',role_required(['Gerente', 'Administrador', 'SU']) (views.agregar_nuevo_producto), name='inventario_admiministrarAgregarProducto'),
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

  ## Funcionalidad para inventario inventario
   path('productos-api/', views.productos_api, name='productos_api'),
    path('categorias-api/', views.categorias_api, name='categorias_api'),
     path('actualizar-stock/', views.actualizar_stock, name='actualizar_stock'),

    path('error_permiso/', views.error_permiso, name='error_permiso'),


    

]

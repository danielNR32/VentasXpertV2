from django.urls import path
from . import views
from utils.decorators import role_required

urlpatterns = [
    path(
        'homeCajero/', 
        role_required(['Cajero', 'Administrador', 'SU'])(views.home), 
        name='cajero_home'
    ),
    path(
        'cajero/', 
        role_required(['Cajero', 'Administrador', 'SU'])(views.caja), 
        name='caja'
    ),
    path(
        'cajero2/', 
        role_required(['Cajero', 'Administrador', 'SU'])(views.caja2), 
        name='caja2'
    ),
    path(
        'error_permiso/', 
        views.error_permiso, 
        name='error_permiso'
    ),
]

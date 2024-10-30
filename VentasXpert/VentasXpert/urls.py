from django.contrib import admin
from django.urls import path, include
from . import views  # Importa las vistas donde está login_view y logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),  # Ruta para el login global
    path('logout/', views.logout_view, name='logout'),  # Ruta de logout personalizada
    path('usuarios_permisos/', include('Usuarios_permisos.urls')),
    path('administracion/', include('Administracion.urls')),
    path('ventas_caja/', include('Ventas_caja.urls')),
    path('catalogo_productos/', include('Catalogo_productos.urls')),
]

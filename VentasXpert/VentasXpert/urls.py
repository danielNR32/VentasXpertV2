from django.contrib import admin
from django.urls import path, include
from . import views  # Importa las vistas donde está login_view y logout_view
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),  # Ruta para el login global
    path('logout/', views.logout_view, name='logout'),  # Ruta de logout personalizada
    path('usuarios_permisos/', include('Usuarios_permisos.urls')),
    path('administracion/', include('Administracion.urls')),
    path('ventas_caja/', include('Ventas_caja.urls')),
    path('catalogo_productos/', include('Catalogo_productos.urls')),
]

# Habilitar archivos estáticos en modo desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, "Ventas_caja", "static"))

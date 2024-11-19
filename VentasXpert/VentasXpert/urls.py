from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from . import views  # Importa las vistas globales
from django.conf import settings
from django.conf.urls.static import static
import os
from Ventas_caja.views import serve_pdf_ticket

def redirect_to_historial(request, *args, **kwargs):
    return redirect('vistaHistorial')

urlpatterns = [
    # Rutas del administrador de Django
    path('admin/', admin.site.urls),

    # Rutas globales
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Autenticación multifactor
    path('configure-mfa/', views.configure_mfa, name='configure_mfa'),
    path('verify-totp/', views.verify_totp, name='verify_totp'),

    # Aplicaciones específicas
    path('usuarios_permisos/', include('Usuarios_permisos.urls')),
    path('administracion/', include('Administracion.urls')),
    path('ventas_caja/', include('Ventas_caja.urls')),
    path('catalogo_productos/', include('Catalogo_productos.urls')),

    # Redirección para acceso restringido a archivos PDF
    path('pdf_ticket/', redirect_to_historial),
    path('pdf_ticket/<str:file_name>/', serve_pdf_ticket, name='serve_pdf_ticket'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, "Ventas_caja", "static"))
    urlpatterns += static(settings.MEDIA_URL, document_root=os.path.join(settings.BASE_DIR, "Ventas_caja", "media"))

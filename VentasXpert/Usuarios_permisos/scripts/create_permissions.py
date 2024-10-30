from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from Usuarios_permisos.models import UsuarioPermiso  # Ajusta al modelo adecuado
import django

# Cargar el entorno de Django si estás ejecutando el script fuera del entorno de administración
django.setup()

def crear_permisos():
    permisos = [
        {"codename": "puede_ver_boton_inventario", "name": "Puede ver botón de inventario"},
        {"codename": "puede_ver_boton_caja", "name": "Puede ver botón de caja"},
    ]

    content_type = ContentType.objects.get_for_model(UsuarioPermiso)

    for permiso in permisos:
        Permission.objects.get_or_create(
            codename=permiso["codename"],
            name=permiso["name"],
            content_type=content_type,
        )

    print("Permisos creados correctamente.")

if __name__ == "__main__":
    crear_permisos()

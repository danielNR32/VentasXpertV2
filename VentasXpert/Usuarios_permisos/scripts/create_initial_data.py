from django.contrib.auth.models import Permission
from Usuarios_permisos.models import UsuarioPermiso
from django.contrib.auth import get_user_model
"""def asignar_permiso_adicional():
    User = get_user_model()
    user = User.objects.get(username="nombre_usuario")  # Cambia "nombre_usuario" por el usuario deseado

    # Crear una instancia de UsuarioPermiso si no existe
    usuario_permiso, created = UsuarioPermiso.objects.get_or_create(user=user)

    # Obtener y agregar el permiso específico
    #permiso_adicional = Permission.objects.get(codename='can_access_reports')
    #usuario_permiso.permisos.add(permiso_adicional)
"""
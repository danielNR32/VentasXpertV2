from Usuarios_permisos.models import UsuarioRol,UsuarioPermiso

def user_role(request):
    if request.user.is_authenticated:
        try:
            usuario_rol = UsuarioRol.objects.get(user=request.user)
            return {'user_role': usuario_rol.rol.nombre}
        except UsuarioRol.DoesNotExist:
            return {'user_role': None}
    return {'user_role': None}


def user_permissions(request):
    if request.user.is_authenticated:
        try:
            usuario_permiso = UsuarioPermiso.objects.get(user=request.user)
            permisos_adicionales = [perm.codename for perm in usuario_permiso.permisos.all()]
            return {'user_permissions': permisos_adicionales}
        except UsuarioPermiso.DoesNotExist:
            return {'user_permissions': []}
    return {'user_permissions': []}
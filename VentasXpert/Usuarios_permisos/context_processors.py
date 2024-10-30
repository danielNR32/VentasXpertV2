from Usuarios_permisos.models import UsuarioRol

def user_role(request):
    if request.user.is_authenticated:
        try:
            usuario_rol = UsuarioRol.objects.get(user=request.user)
            return {'user_role': usuario_rol.rol.nombre}
        except UsuarioRol.DoesNotExist:
            return {'user_role': None}
    return {'user_role': None}
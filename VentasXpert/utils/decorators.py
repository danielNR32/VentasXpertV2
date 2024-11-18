from django.shortcuts import redirect
from Usuarios_permisos.models import UsuarioRol  # Importa el modelo adecuado

def role_required(allowed_roles):
    """
    Decorador para restringir acceso a usuarios con roles específicos.
    :param allowed_roles: Lista de roles permitidos.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            # Verifica si el usuario es superusuario
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Verifica si el usuario tiene un rol en la tabla Usuarios_Roles
            try:
                usuario_rol = UsuarioRol.objects.get(user=request.user)
                if usuario_rol.rol.nombre in allowed_roles:
                    return view_func(request, *args, **kwargs)
            except UsuarioRol.DoesNotExist:
                pass  # Si no tiene rol, no puede acceder
            
            # Redirige a la página de error de permisos
            return redirect('error_permiso')
        return _wrapped_view
    return decorator

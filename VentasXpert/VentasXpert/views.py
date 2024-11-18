# vistas_globales.py (o donde tengas la vista de login)
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout  
from Usuarios_permisos.models import UsuarioRol
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Obtener el rol del usuario autenticado
            try:
                usuario_rol = UsuarioRol.objects.get(user=user)
                rol_nombre = usuario_rol.rol.nombre  # Obtiene el nombre del rol
            except UsuarioRol.DoesNotExist:
                rol_nombre = None

            # Redirigir al usuario según su rol
            if rol_nombre == 'SU':
                return redirect('usuarios_permisos_home')
            elif rol_nombre == 'Administrador':
                return redirect('administrador_home')
            elif rol_nombre == 'Cajero':
                return redirect('cajero_home')
            else:
                return redirect('catalogo_home')
        else:
            return render(request, 'login.html', {'error': 'Nombre de usuario o contraseña incorrectos'})

    return render(request, 'login.html')

@login_required
def administrador_home(request):
    user_role = request.user.usuario_rol.rol.nombre if hasattr(request.user, 'usuario_rol') else None
    return render(request, 'Administracion/home.html', {'user_role': user_role})


def logout_view(request):
    logout(request)
   
    return redirect('login')  
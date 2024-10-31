# Usuarios_permisos/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout

@login_required
def usuarios_permisos_home(request):
    return render(request, 'Usuarios_permisos/home.html')
# Create your views here.
def base(request):
    return render(request, 'Usuarios_permisos/home.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page or another page

def usuarios(request):
    return render(request, 'app/usuarios.html')

def permisos(request):
    return render(request, 'app/permisos.html')

def roles(request):
    return render(request, 'app/roles.html')
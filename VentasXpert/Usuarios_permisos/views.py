# Usuarios_permisos/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def usuarios_permisos_home(request):
    return render(request, 'Usuarios_permisos/home.html')

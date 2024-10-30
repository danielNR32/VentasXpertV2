from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def administrador_home(request):
    return render(request, 'Administracion/home.html')


@login_required
def reportes_home(request):
    return render(request, 'Administracion/reportes_home.html')
@login_required
def inventario_home(request):
    return render(request, 'Administracion/inventario_home.html')

@login_required
def proovedores_home(request):
    return render(request, 'Administracion/proovedores_home.html')
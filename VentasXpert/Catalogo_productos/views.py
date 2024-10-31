# Catalogo_productos/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required



@login_required
def catalogo_home(request):
    return render(request, 'Catalogo_productos/home.html')

@login_required
def catalogo(request):
    return render(request, 'app/catalogoClientes.html')

def infoTienda(request):
    return render(request, 'app/infoTienda.html')

def home(request):
    return render(request, 'Catalogo_productos/home.html')


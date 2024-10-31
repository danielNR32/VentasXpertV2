# Catalogo_productos/views.py
from django.shortcuts import render



def catalogo_home(request):
    return render(request, 'Catalogo_productos/home.html')

def catalogo(request):
    return render(request, 'app/catalogoClientes.html')

def infoTienda(request):
    return render(request, 'app/infoTienda.html')

def home(request):
    return render(request, 'Catalogo_productos/home.html')


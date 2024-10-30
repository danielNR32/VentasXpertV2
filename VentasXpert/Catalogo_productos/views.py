# Catalogo_productos/views.py
from django.shortcuts import render



def catalogo_home(request):
    return render(request, 'Catalogo_productos/home.html')

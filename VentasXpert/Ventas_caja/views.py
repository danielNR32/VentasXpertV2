# Ventas_caja/views.py
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Usuarios_permisos.models import Producto

@login_required
def caja(request):
    return render(request, 'app/caja.html')

@login_required
def home(request):
    productos = Producto.objects.all()
    context = {'productos': productos}
    return render(request, 'Ventas_caja/home.html', context)

@login_required
def caja2(request):
    return render(request, 'Ventas_caja/caja.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page or another page
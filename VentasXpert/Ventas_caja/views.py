# Ventas_caja/views.py
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def caja(request):
    return render(request, 'app/caja.html')

@login_required
def home(request):
    return render(request, 'Ventas_caja/home.html')

@login_required
def caja2(request):
    return render(request, 'Ventas_caja/caja.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page or another page
# Ventas_caja/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def cajero_home(request):
    return render(request, 'Ventas_caja/home.html')

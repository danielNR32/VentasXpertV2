from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.
def dashboard(request):
    return render(request, 'app/dashboard.html')

def informacionInventario(request):
    return render(request, 'app/Inventario/informacion.html')

def inventarioInventario(request):
    return render(request, 'app/Inventario/inventario.html')

def inventarioAgregra_producto(request):
    return render(request, 'app/Inventario/modales/agregar_producto.html')
def inventario_administrar(request):
    return render(request, 'app/Inventario/administrar.html')
def inventario_admiministrarAgregarProducto(request):
    return render(request, 'app/Inventario/modales/agregarNuevoProducto.html')

def inventario_actualizarProducto(request):
    return render(request, 'app/Inventario/modales/actualizarProducto.html')

def home(request):
    return render(request, 'Administracion/home.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page or another page

def proovedores_home(request):
    return render(request, 'Administracion/proovedores_home.html')

def reportes_home(request):
    return render(request, 'Administracion/reportes_home.html')

def inventario_home(request):
    return render(request, 'Administracion/inventario_home.html')

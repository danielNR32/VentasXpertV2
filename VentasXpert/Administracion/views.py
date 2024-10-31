from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'app/dashboard.html')
@login_required
def informacionInventario(request):
    return render(request, 'app/Inventario/informacion.html')
@login_required
def inventarioInventario(request):
    return render(request, 'app/Inventario/inventario.html')
@login_required
def inventarioAgregra_producto(request):
    return render(request, 'app/Inventario/modales/agregar_producto.html')
@login_required
def inventario_administrar(request):
    return render(request, 'app/Inventario/administrar.html')
@login_required
def inventario_admiministrarAgregarProducto(request):
    return render(request, 'app/Inventario/modales/agregarNuevoProducto.html')
@login_required
def inventario_actualizarProducto(request):
    return render(request, 'app/Inventario/modales/actualizarProducto.html')
@login_required
def home(request):
    return render(request, 'Administracion/home.html')
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page or another page
@login_required
def proovedores_home(request):
    return render(request, 'Administracion/proovedores_home.html')
@login_required
def reportes_home(request):
    return render(request, 'Administracion/reportes_home.html')
@login_required
def inventario_home(request):
    return render(request, 'Administracion/inventario_home.html')

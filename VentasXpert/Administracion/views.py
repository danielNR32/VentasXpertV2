from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout

from django.shortcuts import render, redirect
from django.contrib import messages
from Usuarios_permisos.models import Categoria, Proveedor, Producto  # Cambia la ubicación de los modelos
from .forms import ProductoForm

from django.shortcuts import render, redirect
from django.contrib import messages
from Usuarios_permisos.models import Categoria, Proveedor, Producto
from .forms import ProductoForm

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


@login_required
def vista_inventario(request):
    # Recupera los productos temporales de la sesión
    productos_temp = request.session.get('productos_temp', [])
    return render(request, 'app/Inventario/inventario.html', {'productos_temp': productos_temp})

@login_required
def vista_inventario2(request):
    # Recupera los productos temporales de la sesión
    productos_temp = request.session.get('productos_temp', [])
    return render(request, 'app/Inventario/modales/agregarNuevoProducto.html', {'productos_temp': productos_temp})




# guardar en la base de datos
from django.core.exceptions import ObjectDoesNotExist

def confirmar_inventario(request):
    productos_temp = request.session.get('productos_temp', [])
    
    for producto_data in productos_temp:
        # Buscar el proveedor, si está vacío o no existe, el valor será None
        proveedor = None
        if producto_data.get('proveedor') and producto_data['proveedor'] != "No asignado":
            proveedor = Proveedor.objects.filter(nombre=producto_data['proveedor']).first()

        # Obtener la categoría siempre
        categoria = Categoria.objects.get(nombre=producto_data['categoria'])

        # Crear y guardar el producto
        producto = Producto(
            codigo=producto_data['codigo'],
            nombre=producto_data['nombre'],
            categoria=categoria,
            proveedor=proveedor,  # Si no hay proveedor, se guarda como None automáticamente
            stock_Inventario=producto_data['stock_Inventario'],
            stock_Minimo=producto_data['stock_Minimo'],
            precio_proveedor=producto_data['precio_proveedor'],
            precio_tienda=producto_data['precio_tienda'],
            ganancia_pesos=producto_data['ganancia_pesos'],
            ganancia_porcentaje=producto_data['ganancia_porcentaje'],
        )
        producto.save()

    # Limpiar la sesión después de guardar los productos
    request.session['productos_temp'] = []
    messages.success(request, "Inventario actualizado correctamente.")
    return redirect('vista_inventario')


## funcionalidad de AgregarNuevoProducto.html

from decimal import Decimal
def agregar_nuevo_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            # Check if the product already exists in the database
            if Producto.objects.filter(codigo=form.cleaned_data['codigo']).exists():
                messages.error(request, "El producto con este código ya existe.")
                return redirect('vista_inventario2')
            
            producto = form.save(commit=False)
            producto.ganancia_pesos = producto.precio_tienda - producto.precio_proveedor
            producto.ganancia_porcentaje = (producto.ganancia_pesos / producto.precio_proveedor) * 100 if producto.precio_proveedor > 0 else 0

            productos_temp = request.session.get('productos_temp', [])
            productos_temp.append({
                'codigo': producto.codigo,
                'nombre': producto.nombre,
                'categoria': producto.categoria.nombre,
                'proveedor': producto.proveedor.nombre if producto.proveedor else "No asignado",
                'stock_Inventario': int(producto.stock_Inventario),
                'stock_Minimo': int(producto.stock_Minimo),
                'precio_proveedor': float(producto.precio_proveedor),
                'precio_tienda': float(producto.precio_tienda),
                'ganancia_porcentaje': round(float(producto.ganancia_porcentaje), 2),
                'ganancia_pesos': round(float(producto.ganancia_pesos), 2),
            })
            request.session['productos_temp'] = productos_temp
            messages.success(request, "Producto agregado temporalmente.")
            return redirect('vista_inventario2')

    else:
        form = ProductoForm()

    categorias = Categoria.objects.all()
    productos_temp = request.session.get('productos_temp', [])
    
    return render(request, 'app/Inventario/modales/agregarNuevoProducto.html', {
        'form': form,
        'categorias': categorias,
        'productos_temp': productos_temp
    })



def eliminar_producto_temporal(request, index):
    productos_temp = request.session.get('productos_temp', [])
    if 0 <= index < len(productos_temp):
        del productos_temp[index]
        request.session['productos_temp'] = productos_temp
        messages.success(request, "Producto eliminado temporalmente.")
    else:
        messages.error(request, "No se pudo eliminar el producto.")

    return redirect('vista_inventario2')
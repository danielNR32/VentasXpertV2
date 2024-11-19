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

from decimal import Decimal

def confirmar_inventario(request):
    productos_temp = request.session.get('productos_temp', [])
    
    for producto_data in productos_temp:
        # Buscar el proveedor, si está vacío o no existe, el valor será None
        proveedor = None
        if producto_data.get('proveedor') and producto_data['proveedor'] != "No asignado":
            proveedor = Proveedor.objects.filter(nombre=producto_data['proveedor']).first()

        # Obtener la categoría siempre
        categoria = Categoria.objects.get(nombre=producto_data['categoria'])

        # Convertir precios a números antes de realizar operaciones matemáticas
        precio_proveedor = Decimal(producto_data['precio_proveedor'])
        precio_tienda = Decimal(producto_data['precio_tienda'])

        # Calcular ganancia
        ganancia_pesos = precio_tienda - precio_proveedor
        ganancia_porcentaje = (ganancia_pesos / precio_proveedor) * 100 if precio_proveedor > 0 else 0

        # Crear y guardar el producto
        producto = Producto(
            codigo=producto_data['codigo'],
            nombre=producto_data['nombre'],
            categoria=categoria,
            proveedor=proveedor,  # Si no hay proveedor, se guarda como None automáticamente
            stock_Inventario=producto_data['stock_Inventario'],
            stock_Minimo=producto_data['stock_Minimo'],
            precio_proveedor=precio_proveedor,
            precio_tienda=precio_tienda,
            ganancia_pesos=ganancia_pesos,
            ganancia_porcentaje=ganancia_porcentaje,
        )
        producto.save()

    # Limpiar la sesión después de guardar los productos
    request.session['productos_temp'] = []
    messages.success(request, "Inventario actualizado correctamente.")
    return redirect('vista_inventario')

## funcionalidad de AgregarNuevoProducto.html

from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from Usuarios_permisos.models import Producto, Categoria  # Asegúrate de importar tus modelos correctamente
from .forms import ProductoForm  # Asegúrate de tener el formulario correcto

from decimal import Decimal, InvalidOperation

def agregar_nuevo_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        
        if form.is_valid():
            try:
                # Convertir a Decimal para precios
                precio_proveedor = Decimal(form.cleaned_data['precio_proveedor'])
                precio_tienda = Decimal(form.cleaned_data['precio_tienda'])

                # Asegurarse que sean números válidos y positivos
                if precio_proveedor < 0 or precio_tienda < 0:
                    messages.error(request, "Los precios no pueden ser negativos.")
                    return redirect('inventario_admiministrarAgregarProducto')

                # Validar que el stock sea un número entero positivo
                stock_Inventario = int(form.cleaned_data['stock_Inventario'])
                stock_Minimo = int(form.cleaned_data['stock_Minimo'])

                if stock_Inventario < 0 or stock_Minimo < 0:
                    messages.error(request, "El stock no puede ser negativo.")
                    return redirect('inventario_admiministrarAgregarProducto')

                # Continuar con el procesamiento del producto
                producto = form.save(commit=False)
                producto.ganancia_pesos = precio_tienda - precio_proveedor
                producto.ganancia_porcentaje = (producto.ganancia_pesos / precio_proveedor) * 100 if precio_proveedor > 0 else 0

                # Guardar el producto temporalmente en la sesión
                productos_temp = request.session.get('productos_temp', [])
                productos_temp.append({
                    'codigo': producto.codigo,
                    'nombre': producto.nombre,
                    'categoria': producto.categoria.nombre,
                    'proveedor': producto.proveedor.nombre if producto.proveedor else "No asignado",
                    'stock_Inventario': stock_Inventario,
                    'stock_Minimo': stock_Minimo,
                    'precio_proveedor': float(precio_proveedor),
                    'precio_tienda': float(precio_tienda),
                    'ganancia_porcentaje': round(float(producto.ganancia_porcentaje), 2),
                    'ganancia_pesos': round(float(producto.ganancia_pesos), 2),
                })
                request.session['productos_temp'] = productos_temp
                messages.success(request, "Producto agregado con exito!!.")
                return redirect('inventario_admiministrarAgregarProducto')

            except InvalidOperation:
                messages.error(request, "Por favor, ingrese un valor válido para los precios.")
                return redirect('inventario_admiministrarAgregarProducto')
        else:
            messages.error(request, "Formulario no válido codigo del producto ya existente.")
            return redirect('inventario_admiministrarAgregarProducto')

    form = ProductoForm()
    return render(request, 'app/Inventario/modales/agregarNuevoProducto.html', {
        'form': form,
        'categorias': Categoria.objects.all(),
        'productos_temp': request.session.get('productos_temp', [])
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


## recargar js
from datetime import datetime

def tu_vista(request):
    # Otras lógicas de la vista
    context = {
        'timestamp': datetime.now().timestamp(),  # Marca de tiempo actual
        # Otros contextos
    }
    return render(request, 'tu_template.html', context)



from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

def editar_producto_temporal(request, index):
    if request.method == 'POST':
        productos_temp = request.session.get('productos_temp', [])
        
        if 0 <= index < len(productos_temp):
            # Obtener los valores enviados desde el formulario
            field = request.POST.get('field')
            value = request.POST.get('value')

            # Actualizar el producto temporal
            productos_temp[index][field] = value
            request.session['productos_temp'] = productos_temp

            messages.success(request, "Producto actualizado correctamente.")
            return redirect('vista_inventario2')  # Redirigir a la página del inventario
        else:
            messages.error(request, "Índice fuera de rango.")
            return redirect('vista_inventario2')

    messages.error(request, "Método no permitido.")
    return redirect('vista_inventario2')

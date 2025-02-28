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
from Usuarios_permisos.models import Producto, CarritoProducto, Carrito, Bitacora, UsuarioRol
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
    if request.user.is_authenticated:
        Bitacora.objects.create(
            usuario=request.user,
            accion='Cerrar Sesión',
            detalle=f'Cierre de sesión para el usuario {request.user.username}.'
        )
    logout(request)
    return redirect('login')

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

      # Obtener el rol del usuario
    usuario = request.user
    try:
        usuario_rol = UsuarioRol.objects.get(user=usuario)
        rol = usuario_rol.rol.nombre
    except UsuarioRol.DoesNotExist:
        rol = "Sin rol asignado"

    # Registrar la acción en la bitácora
    Bitacora.objects.create(
        usuario=usuario,
        persona=usuario.persona if hasattr(usuario, 'persona') else None,
        rol=usuario_rol.rol if hasattr(usuario, 'usuariorol') else None,
        accion='Inventario actualizado',
        detalle=f"Se han agregado nuevos productos al inventario. Usuario: {usuario.username}, Rol: {rol}",
    )
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
from Administracion.factories import ProductoInventarioFactory  # Importamos la fábrica
from decimal import Decimal, InvalidOperation
def agregar_nuevo_producto(request):
    """
    Vista para agregar productos al inventario usando el patrón Factory Method.
    """
    if request.method == "POST":
        form = ProductoForm(request.POST)
        
        if form.is_valid():
            try:
                # Extraer datos del formulario
                datos_producto = form.cleaned_data
                factory = ProductoInventarioFactory()  # Instanciamos la fábrica
                factory.crear_producto(**datos_producto)  # Creamos el producto

                messages.success(request, "Producto agregado con éxito.")
                return redirect("inventario_admiministrarAgregarProducto")

            except ValueError as e:
                messages.error(request, f"Error al agregar el producto: {e}")
                return redirect("inventario_admiministrarAgregarProducto")

        else:
            messages.error(request, "Formulario no válido, código de producto ya existente.")
            return redirect("inventario_admiministrarAgregarProducto")

    form = ProductoForm()
    return render(request, "app/Inventario/modales/agregarNuevoProducto.html", {
        "form": form,
        "categorias": Categoria.objects.all(),
        "productos_temp": request.session.get("productos_temp", [])
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
#


#Funcionalidad de agregar funcionalidad agregar nuevo producto
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from Usuarios_permisos.models import Producto, Categoria
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

def surtir_inventario(request):
    categorias = Categoria.objects.all()
    return render(request, 'app/Inventario/informacion.html', {'categorias': categorias})

def buscar_producto(request):
    codigo = request.GET.get('codigo', '').strip()
    nombre = request.GET.get('nombre', '').strip()
    categoria_id = request.GET.get('categoria', '').strip()

    productos = Producto.objects.all()
    if codigo:
        productos = productos.filter(codigo__icontains=codigo)
    if nombre:
        productos = productos.filter(nombre__icontains=nombre)
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    productos_data = [
        {
            "id": producto.id,
            "codigo": producto.codigo,
            "nombre": producto.nombre,
            "categoria": producto.categoria.nombre,
            "stock_Inventario": producto.stock_Inventario,
            "precio_tienda": str(producto.precio_tienda),
            "precio_proveedor": str(producto.precio_proveedor),
        }
        for producto in productos
    ]
    
    return JsonResponse({"productos": productos_data})

@csrf_exempt
def confirmar_surtido(request):
    # Confirmar los productos en surtido
    productos_temp = request.session.get('productos_temp', [])
    for item in productos_temp:
        producto = Producto.objects.get(id=item['id'])
        producto.stock_Inventario += item['cantidad']
        producto.save()
    

    # Obtener el rol del usuario
    usuario = request.user
    try:
        usuario_rol = UsuarioRol.objects.get(user=usuario)
        rol = usuario_rol.rol.nombre
    except UsuarioRol.DoesNotExist:
        rol = "Sin rol asignado"

    # Registrar la acción en la bitácora
    Bitacora.objects.create(
        usuario=usuario,
        persona=usuario.persona if hasattr(usuario, 'persona') else None,
        rol=usuario_rol.rol if hasattr(usuario, 'usuariorol') else None,
        accion='Inventario actualizado',
        detalle=f"Se han agregado stock a los productos del inventario. Usuario: {usuario.username}, Rol: {rol}",
    )
    
     

    # Limpiar la sesión temporal
    request.session['productos_temp'] = []
    messages.success(request, "Surtido confirmado exitosamente.")
    return JsonResponse({"success": True})

#restriccion de url
def error_permiso(request):
    return render(request, 'usuarios_permisos/error_permiso.html', {
        'mensaje': "No tienes permiso para acceder a esta página."
    })



## VITSA PARA INVENTARIO INVENTARIO
from django.http import JsonResponse
from django.db.models import F

from django.http import JsonResponse
from django.db.models import F

def productos_api(request):
    """
    Devuelve los datos de productos en formato JSON para DataTables.
    """
    productos = Producto.objects.all()
    
    # Filtrar por categoría
    categoria = request.GET.get('categoria')
    if categoria:
        productos = productos.filter(categoria__nombre=categoria)
    
    # Filtrar por estado
    estado = request.GET.get('estado')
    if estado:
        if estado == "Suficiente":
            productos = productos.filter(stock_Inventario__gte=F('stock_Minimo')).exclude(stock_Inventario=0)
            print(productos.count())
        elif estado == "Poca existencia":
            productos = productos.filter(stock_Inventario__lt=F('stock_Minimo'), stock_Inventario__gt=0)
        elif estado == "Sin existencia":
            productos = productos.filter(stock_Inventario=0)
    
    # Serializar los datos
    data = [
        {
            "codigo": producto.codigo,
            "nombre": producto.nombre,
            "categoria": producto.categoria.nombre if producto.categoria else "",
            "estado_stock": (
                "Sin existencia" if producto.stock_Inventario == 0
                else "Poca existencia" if producto.stock_Inventario < producto.stock_Minimo
                else "Suficiente"
            ),
            "cantidad_minima": producto.stock_Minimo,
            "cantidad_total": producto.stock_Inventario,
            "precio_tienda": producto.precio_tienda,
            "ganancia": producto.ganancia_pesos,
            "precio_provedor": producto.precio_proveedor,
        }
        for producto in productos
    ]

    # Debugging para comprobar los filtros aplicados
    print(f"Filtrado: {categoria=}, {estado=}, Productos encontrados: {len(data)}")
    
    return JsonResponse({"data": data})

from Usuarios_permisos.models import Categoria

@login_required
def inventarioInventario(request):
    # Obtener todas las categorías de la base de datos
    categorias = Categoria.objects.all()
    return render(request, 'app/Inventario/inventario.html', {'categorias': categorias})


from django.http import JsonResponse
from Usuarios_permisos.models import Categoria

def categorias_api(request):
    categorias = Categoria.objects.values('id', 'nombre')  # Obtén las categorías
    return JsonResponse({"categorias": list(categorias)})

##Actualizar el stock
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Usuarios_permisos.models import Producto

@csrf_exempt
def actualizar_stock(request):
    if request.method == "POST":
        codigo = request.POST.get("codigo")
        cantidad = int(request.POST.get("cantidad", 0))
        
        try:
            # Buscar el producto por su código
            producto = Producto.objects.get(codigo=codigo)
            producto.stock_Inventario += cantidad  # Actualizar el stock
            producto.save()

             # Obtener el rol del usuario
            usuario = request.user
            try:
                usuario_rol = UsuarioRol.objects.get(user=usuario)
                rol = usuario_rol.rol.nombre
            except UsuarioRol.DoesNotExist:
                rol = "Sin rol asignado"

            # Registrar la acción en la bitácora
            Bitacora.objects.create(
                usuario=usuario,
                persona=usuario.persona if hasattr(usuario, 'persona') else None,
                rol=usuario_rol.rol if hasattr(usuario, 'usuariorol') else None,
                accion='Inventario actualizado',
                detalle=f"Se han agregado stock a los productos del inventario. Usuario: {usuario.username}, Rol: {rol}",
            )

            return JsonResponse({"success": True})
        except Producto.DoesNotExist:
            return JsonResponse({"success": False, "error": "Producto no encontrado."})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Método no permitido."})

## Informacion inventario
from django.shortcuts import render
from django.db.models import F, Sum, Max
from Usuarios_permisos.models import Producto

def informacion_inventario(request):
    productos = Producto.objects.all()

    # Total de productos (cantidad de todos los productos)
    total_productos = productos.count()
    #total cantidad productos
    total_cantidad_productos = productos.aggregate(total=Sum('stock_Inventario'))['total'] or 0
    # Productos con poca cantidad (stock menor que el mínimo)
    poca_cantidad = productos.filter(stock_Inventario__lt=F('stock_Minimo')).count()

    # Productos sin existencia (stock igual a 0)
    sin_existencia = productos.filter(stock_Inventario=0).count()

    # Valor en tienda (precio_proveedor * stock_Inventario para cada producto)
    valor_tienda = sum(p.precio_proveedor * p.stock_Inventario for p in productos)

    # Reinversión en stock (cantidad necesaria para llegar al stock mínimo)
    reinversion = sum(
        max(0, p.stock_Minimo - p.stock_Inventario) * p.precio_proveedor for p in productos
    )



    context = {
        'total_productos': total_productos,
        'total_cantidad_productos': total_cantidad_productos,
        'poca_cantidad': poca_cantidad,
        'sin_existencia': sin_existencia,
        'valor_tienda': valor_tienda,
        'reinversion': reinversion,
        
    }

  
    return render(request, 'app/Inventario/informacion.html', context)

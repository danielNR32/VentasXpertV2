# Ventas_caja/views.py
import datetime
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Usuarios_permisos.models import Producto, CarritoProducto, Carrito

@login_required
def caja(request):
    return render(request, 'app/caja.html')

@login_required
def home(request):
    productos = Producto.objects.all()
    #carritoProductos = CarritoProducto.objects.all()
    carritoProductos = CarritoProducto.objects.select_related('producto').all()
    
    #Elimina los productos automaticamente en caso de que la cantidad sea 0
    for carritoProducto in carritoProductos:
        if carritoProducto.cantidad == 0:
            carritoProducto.delete()
            
    #suma todas las cantidades de productos para mostralo en detalles de productos y suma el total de costo de productos
    total_productos = 0
    total_costo_productos = 0
    for carritoProducto in carritoProductos:
        total_productos += carritoProducto.cantidad
        total_costo_productos += carritoProducto.subtotal
        
    #calcular fecha actual en formato dd/mm/aaaa
    fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y")
    
    #calcular hora actual en formato hh:mm:ss
    hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        
    context = {
        'productos': productos, 
        'carritoProductos': carritoProductos, 
        'total_productos': total_productos,
        'total_costo_productos': total_costo_productos,
        'fecha_actual': fecha_actual,
        'hora_actual': hora_actual
    }
    return render(request, 'Ventas_caja/home.html', context)

def agregar_producto(request, id):
    producto = Producto.objects.get(id=id)
    try:
        carrito_producto = CarritoProducto.objects.get(producto=producto)
        carrito_producto.cantidad += 1
        carrito_producto.subtotal += producto.precio_tienda
        carrito_producto.save()
    except CarritoProducto.DoesNotExist:
        CarritoProducto.objects.create(
            producto=producto,
            cantidad=1,
            subtotal=producto.precio_tienda,
            producto_id=producto.id
        )
    
    return redirect('cajero_home')

def restar_producto(request, id):
    producto = Producto.objects.get(id=id)
    try:
        carrito_producto = CarritoProducto.objects.get(producto=producto)
        carrito_producto.cantidad -= 1
        carrito_producto.subtotal -= producto.precio_tienda
        carrito_producto.save()
    except CarritoProducto.DoesNotExist:
        pass
    
    return redirect('cajero_home')

def sumar_producto(request, id):
    producto = Producto.objects.get(id=id)
    try:
        carrito_producto = CarritoProducto.objects.get(producto=producto)
        carrito_producto.cantidad += 1
        carrito_producto.subtotal += producto.precio_tienda
        carrito_producto.save()
    except CarritoProducto.DoesNotExist:
        pass
    
    return redirect('cajero_home')

def quitar_producto(request, id):
    producto = Producto.objects.get(id=id)
    try:
        carrito_producto = CarritoProducto.objects.get(producto=producto)
        carrito_producto.delete()
    except CarritoProducto.DoesNotExist:
        pass
    
    return redirect('cajero_home')

def eliminar_carrito_actual(request):
    carritoProductos = CarritoProducto.objects.all()
    for carritoProducto in carritoProductos:
        carritoProducto.delete()
    return redirect('cajero_home')

@login_required
def caja2(request):
    return render(request, 'Ventas_caja/caja.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page or another page
# Ventas_caja/views.py
import datetime
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Usuarios_permisos.models import Producto, CarritoProducto, Carrito, Bitacora, UsuarioRol
from django.http import HttpResponse, HttpResponseForbidden, FileResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io, os
from django.conf import settings

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
    
    # Restaurar stock de productos
    for carritoProducto1 in carritoProductos:
        producto_actual = Producto.objects.get(id=carritoProducto1.producto_id)
        producto_actual.stock_Inventario -= carritoProducto1.cantidad
        producto_actual.save()
        
    # llama a la funcion para generar el ticket
    generar_ticket_pdf(request)
    
    # Eliminar productos del carrito
    for carritoProducto in carritoProductos:
        carritoProducto.delete()
    return redirect('cajero_home')

# Interfaz Command (Refactorizacion al metodo command para la generacion de tickets)
class Command:
    def execute(self):
        raise NotImplementedError("Debe implementarse en una subclase")

# Comando para obtener productos del carrito
class ObtenerProductosCommand(Command):
    def __init__(self, request):
        self.request = request
    
    def execute(self):
        productos = Producto.objects.all()
        carritoProductos = CarritoProducto.objects.select_related('producto').all()
        total_productos = sum([carrito.cantidad for carrito in carritoProductos])
        total_costo_productos = sum([carrito.subtotal for carrito in carritoProductos])
        
        fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y")
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        
        context = {
            'productos': productos,
            'carritoProductos': carritoProductos,
            'total_productos': total_productos,
            'total_costo_productos': total_costo_productos,
            'fecha_actual': fecha_actual,
            'hora_actual': hora_actual,
            'usuarios': self.request.user
        }
        
        return context

# Comando para registrar en la bitácora
class RegistrarBitacoraCommand(Command):
    def __init__(self, request, total_productos, total_costo_productos):
        self.request = request
        self.total_productos = total_productos
        self.total_costo_productos = total_costo_productos
    
    def execute(self):
        Bitacora.objects.create(
            accion='purchase',
            detalle=f'Compra de {self.total_productos} productos por un total de ${self.total_costo_productos}',
            usuario=self.request.user,
            rol=self.request.user.usuariorol.rol if hasattr(self.request.user, 'usuariorol') else None,
            persona=self.request.user.persona if hasattr(self.request.user, 'persona') else None,
        )

# Comando para generar PDF
class GenerarPDFCommand(Command):
    def __init__(self, context):
        self.context = context
    
    def execute(self):
        html = render_to_string('Ventas_caja/ticket_pdf.html', self.context)
        pdf_dir = os.path.join(settings.BASE_DIR, 'Ventas_caja', 'media', 'pdf_ticket')
        os.makedirs(pdf_dir, exist_ok=True)
        pdf_path = os.path.join(pdf_dir, f'ticket_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.pdf')
        
        with open(pdf_path, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(io.BytesIO(html.encode("UTF-8")), dest=pdf_file, encoding='UTF-8')
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="ticket.pdf"'
        
        pisa_status = pisa.CreatePDF(io.BytesIO(html.encode("UTF-8")), dest=response, encoding='UTF-8')
        
        if pisa_status.err:
            return HttpResponse("Hubo un error al generar el PDF", status=500)
        
        return response

# Invoker que gestiona la ejecución de los comandos
class TicketInvoker:
    def __init__(self):
        self.comandos = []
    
    def agregar_comando(self, comando):
        self.comandos.append(comando)
    
    def ejecutar_comandos(self):
        resultados = []
        for comando in self.comandos:
            resultados.append(comando.execute())
        return resultados

# Vista Django refactorizada
def generar_ticket_pdf(request):
    invoker = TicketInvoker()
    
    obtener_productos_command = ObtenerProductosCommand(request)
    context = obtener_productos_command.execute()
    
    registrar_bitacora_command = RegistrarBitacoraCommand(request, context['total_productos'], context['total_costo_productos'])
    generar_pdf_command = GenerarPDFCommand(context)
    
    invoker.agregar_comando(registrar_bitacora_command)
    invoker.agregar_comando(generar_pdf_command)
    
    resultados = invoker.ejecutar_comandos()
    return resultados[-1]  # Retorna la respuesta del PDF

# Fin vista refactorizada

@login_required
def caja2(request):
    return render(request, 'Ventas_caja/caja.html')

@login_required
def vistaHistorial(request):
    import os
    from django.conf import settings

    # Ruta de la carpeta donde se guardan los PDFs
    pdf_folder = os.path.join(settings.BASE_DIR, 'Ventas_caja', 'media', 'pdf_ticket')

    # Lista los archivos en la carpeta
    pdf_files = []
    for file_name in os.listdir(pdf_folder):
        file_path = os.path.join(pdf_folder, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.pdf'):
            # Obtener la fecha de creación
            creation_time = os.path.getctime(file_path)
            pdf_files.append({
                'name': file_name,
                'creation_time': datetime.datetime.fromtimestamp(creation_time),
                'path': f'{settings.MEDIA_URL}pdf_ticket/{file_name}'
            })

    # Ordenar por fecha de creación descendente
    pdf_files.sort(key=lambda x: x['creation_time'], reverse=True)

    return render(request, 'Ventas_caja/vistaHistorial.html', {'pdf_files': pdf_files})

@login_required
def serve_pdf_ticket(request, file_name):
    # Ruta completa del archivo
    file_path = os.path.join(settings.BASE_DIR, 'Ventas_caja', 'media', 'pdf_ticket', file_name)

    # Verifica si el archivo existe
    if not os.path.exists(file_path):
        return HttpResponse("Archivo no encontrado", status=404)

    # Devuelve el archivo como respuesta
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')


def logout_view(request):
    return redirect('login')  # Redirect to the login page or another page

#restriccion de url
def error_permiso(request):
    return render(request, 'usuarios_permisos/error_permiso.html', {
        'mensaje': "No tienes permiso para acceder a esta página."
    })


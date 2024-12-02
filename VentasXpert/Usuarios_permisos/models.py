from django.db import models
from django.contrib.auth.models import User, Permission

class Persona(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('N', 'Prefiero no decirlo'),
        ('D', 'Desconocido'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="persona")
    nombre = models.CharField(max_length=100)
    segNombre = models.CharField(max_length=100, blank=True, null=True)
    apPaterno = models.CharField(max_length=100)
    apMaterno = models.CharField(max_length=100)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, default='D')
    correo = models.EmailField(max_length=200)
    telefono = models.CharField(max_length=15)
    rfc=models.CharField(max_length=100)
    curp=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Persona'
        verbose_name_plural = 'Personas'
       
    def __str__(self):
        return f"{self.nombre} {self.apPaterno} {self.apMaterno}"

class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    permisos = models.ManyToManyField(Permission, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Roles'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.nombre        

class UsuarioRol(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Usuarios_Roles'
        verbose_name_plural = 'Usuarios Roles'
    
    def __str__(self):
        return f"{self.user.username} - {self.rol.nombre}"

class UsuarioPermiso(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    permisos = models.ManyToManyField(Permission, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Usuario_Permisos'
        verbose_name_plural = 'Usuarios Permisos'

    def __str__(self):
        permisos_nombres = ", ".join([perm.name for perm in self.permisos.all()])
        return f"{self.user.username} - Permisos: {permisos_nombres}"

class Categoria(models.Model):
    nombre = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Categoria'
        verbose_name_plural = 'Categorias'


class Proveedor(models.Model):
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Proveedor'
        verbose_name_plural = 'Proveedores'


class Producto(models.Model):
    codigo = models.CharField(max_length=100, unique=True)  # Código de barras o SKU
    nombre = models.CharField(max_length=255)               # Nombre del producto
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)  # Relación con Categoria
    proveedor = models.ForeignKey(Proveedor, null=True, blank=True, on_delete=models.SET_NULL)  # Opcional # Relación con Proveedor
    stock_Inventario = models.IntegerField()                # Cantidad en el inventario
    stock_Minimo = models.IntegerField()                    # Cantidad mínima para alertas de stock bajo
    precio_proveedor = models.DecimalField(max_digits=10, decimal_places=2)  # Precio de compra al proveedor
    precio_tienda = models.DecimalField(max_digits=10, decimal_places=2)     # Precio de venta en tienda
    ganancia_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # % de ganancia (calculado)
    ganancia_pesos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)      # Ganancia en pesos (calculado)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Calcula la ganancia antes de guardar
        self.ganancia_pesos = self.precio_tienda - self.precio_proveedor
        if self.precio_proveedor > 0:
            self.ganancia_porcentaje = (self.ganancia_pesos / self.precio_proveedor) * 100
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'Producto'
        verbose_name_plural = 'Productos'




class Caja(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saldo_actual = models.DecimalField(max_digits=10, decimal_places=2)
    corte_caja = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Caja'
        verbose_name_plural = 'Cajas'


class Carrito(models.Model):
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Carrito'
        verbose_name_plural = 'Carritos'


class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'Carrito_x_Producto'
        verbose_name_plural = 'Carritos por Productos'


class Venta(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)  # Relación con Carrito
    caja = models.ForeignKey('Caja', on_delete=models.CASCADE)  # Relación con Caja
    finanzas = models.ForeignKey('Finanzas', on_delete=models.CASCADE)  # Relación con Finanzas
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'Venta'
        verbose_name_plural = 'Ventas'

class Finanzas(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'Finanza'
        verbose_name_plural = 'Finanzas'



class UsuarioMFA(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mfa_secret = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'UsuarioMFA'
        verbose_name_plural = 'UsuariosMFA'

class Bitacora(models.Model):
    ACCION_CHOICES = [
    ('create', 'Crear'),
    ('update', 'Actualizar'),
    ('delete', 'Eliminar'),
    ('purchase', 'Compra'),
    ('login', 'Inicio de Session'),
    ('logout', 'Cierre de Session'),
]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Relación con el usuario
    persona = models.ForeignKey(Persona, on_delete=models.SET_NULL, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True) # Rol del usuario
    accion = models.CharField(max_length=50, choices=ACCION_CHOICES)  # Acción realizada
    detalle = models.TextField(blank=True, null=True)  # Información adicional de la acción
    created_at = models.DateTimeField(auto_now_add=True) # Fecha y hora de creación
    update_at = models.DateTimeField(auto_now=True)# Fecha y hora de actualización

    class Meta:
        db_table = 'Bitacora'
        verbose_name_plural = 'Bitacoras'
        indexes = [
        models.Index(fields=['usuario']),  # Índice para usuario
        models.Index(fields=['rol']),     # Índice para rol
        models.Index(fields=['created_at']),  # Índice para la fecha de creación
    ]

    def __str__(self):
        if self.persona:
            return f"{self.persona.nombre} ({self.usuario.username}) - {self.accion}"
        
        if self.rol:
            return f"{self.rol.nombre} ({self.usuario.username}) - {self.accion}"
        return f"{self.usuario.username} - {self.accion}"    
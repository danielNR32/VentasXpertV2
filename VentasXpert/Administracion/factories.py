"""
factories.py

Implementación del patrón Factory Method para la creación de productos en Django.

Clases:
- ProductoFactory: Clase abstracta que define el método para crear productos.
- ProductoInventarioFactory: Implementación concreta que crea productos en el inventario.
"""

from abc import ABC, abstractmethod
from decimal import Decimal, InvalidOperation
from Usuarios_permisos.models import Producto

class ProductoFactory(ABC):
    """
    Clase abstracta que define la estructura de las fábricas de productos.
    """

    @abstractmethod
    def crear_producto(self, **datos):
        """
        Método abstracto para crear un producto.

        Parámetros:
        - datos (dict): Diccionario con la información del producto.

        Retorno:
        - Producto: Objeto Producto creado.
        """
        pass

class ProductoInventarioFactory(ProductoFactory):
    """
    Fábrica concreta para la creación de productos en el inventario.
    """

    def crear_producto(self, **datos):
        """
        Crea un producto y lo almacena en la base de datos.

        Parámetros:
        - datos (dict): Información del producto.

        Retorno:
        - Producto: Objeto Producto creado.
        """
        try:
            # Convertir valores a Decimal para evitar errores de tipo
            datos["precio_proveedor"] = Decimal(datos["precio_proveedor"])
            datos["precio_tienda"] = Decimal(datos["precio_tienda"])

            # Validaciones de valores
            if datos["precio_proveedor"] < 0 or datos["precio_tienda"] < 0:
                raise ValueError("Los precios no pueden ser negativos.")

            # Validaciones de stock
            datos["stock_Inventario"] = int(datos["stock_Inventario"])
            datos["stock_Minimo"] = int(datos["stock_Minimo"])

            if datos["stock_Inventario"] < 0 or datos["stock_Minimo"] < 0:
                raise ValueError("El stock no puede ser negativo.")

            # Calcular ganancia
            datos["ganancia_pesos"] = datos["precio_tienda"] - datos["precio_proveedor"]
            datos["ganancia_porcentaje"] = (
                (datos["ganancia_pesos"] / datos["precio_proveedor"]) * 100
                if datos["precio_proveedor"] > 0
                else 0
            )

            # Crear y guardar el producto en la base de datos
            return Producto.objects.create(**datos)

        except (InvalidOperation, ValueError) as e:
            raise ValueError(f"Error en la creación del producto: {e}")

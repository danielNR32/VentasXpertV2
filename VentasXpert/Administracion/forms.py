from django import forms
from Usuarios_permisos.models import Categoria, Producto

class ProductoForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        empty_label="Seleccione una categoría",
        required=True
    )

    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'categoria', 'proveedor', 'stock_Inventario', 'stock_Minimo', 'precio_proveedor', 'precio_tienda']

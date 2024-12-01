from django.contrib import admin
from .models import Persona, Rol, UsuarioRol,UsuarioPermiso, Bitacora

# Registrar los modelos en el admin
admin.site.register(Persona)
admin.site.register(Rol)
admin.site.register(UsuarioRol)
admin.site.register(UsuarioPermiso)
admin.site.register(Bitacora)

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Permission
from Usuarios_permisos.models import UsuarioPermiso

@receiver(post_save, sender=User)
def asignar_permiso_al_crear_usuario(sender, instance, created, **kwargs):
    if created:
        # Agregar lógica para verificar el rol del usuario si es necesario
        usuario_permiso, created = UsuarioPermiso.objects.get_or_create(user=instance)
        permiso_adicional = Permission.objects.get(codename='can_access_reports')
        usuario_permiso.permisos.add(permiso_adicional)

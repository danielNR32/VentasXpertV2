from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from Usuarios_permisos.models import Persona  # Asegúrate de que el modelo Persona esté en la app correcta

class Command(BaseCommand):
    help = 'Crea roles y permisos predeterminados'

    def handle(self, *args, **kwargs):
        # Crear los grupos (roles)
        grupo_administrador, created = Group.objects.get_or_create(name='Administrador')
        grupo_cajero, created = Group.objects.get_or_create(name='Cajero')
        grupo_SU, created = Group.objects.get_or_create(name='SuperUsuario')  # Cambié a SuperUsuario para mayor claridad

        # Obtener el ContentType para el modelo Persona
        content_type_persona = ContentType.objects.get_for_model(Persona)

        # Crear permisos personalizados para Persona
        permiso_editar_persona = Permission.objects.create(
            codename='puede_editar_persona',
            name='Puede editar personas',
            content_type=content_type_persona,
        )

        permiso_ver_persona = Permission.objects.create(
            codename='puede_ver_persona',
            name='Puede ver personas',
            content_type=content_type_persona,
        )

        permiso_crear_persona = Permission.objects.create(
            codename='puede_crear_persona',
            name='Puede crear personas',
            content_type=content_type_persona,
        )

        permiso_eliminar_persona = Permission.objects.create(
            codename='puede_eliminar_persona',
            name='Puede eliminar personas',
            content_type=content_type_persona,
        )

        # Obtener el ContentType para el modelo User (usuarios)
        content_type_user = ContentType.objects.get_for_model(User)

        # Obtener permisos predeterminados del modelo User
        permiso_ver_usuario = Permission.objects.get(codename='view_user', content_type=content_type_user)
        permiso_crear_usuario = Permission.objects.get(codename='add_user', content_type=content_type_user)
        permiso_editar_usuario = Permission.objects.get(codename='change_user', content_type=content_type_user)
        permiso_eliminar_usuario = Permission.objects.get(codename='delete_user', content_type=content_type_user)

        # Asignar permisos a los grupos
        grupo_administrador.permissions.add(permiso_editar_persona, permiso_ver_persona, permiso_crear_persona, permiso_eliminar_persona)
        
        # Si quieres que SU tenga todos los permisos (para personas y usuarios):
        grupo_SU.permissions.add(
            permiso_editar_persona, permiso_ver_persona, permiso_crear_persona, permiso_eliminar_persona,  # Permisos de Persona
            permiso_ver_usuario, permiso_crear_usuario, permiso_editar_usuario, permiso_eliminar_usuario    # Permisos de User
        )

        # Si quieres que el grupo Cajero tenga un permiso (por ejemplo, solo puede ver personas):
        grupo_cajero.permissions.add(permiso_ver_persona)

        self.stdout.write(self.style.SUCCESS('Grupos y permisos creados exitosamente.'))

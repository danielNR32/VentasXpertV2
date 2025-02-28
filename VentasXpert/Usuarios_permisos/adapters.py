# adapters.py
from django.contrib.auth.models import User
from .models import Persona, Bitacora
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import Rol, UsuarioRol, Bitacora




class UserAdapter:
    @staticmethod
    def create_user(formUser, formPerson, created_by):
        """
        Crea un usuario con su persona asociada y lo registra en la bitácora.
        """
        user = formUser.save(commit=False)
        user.set_password(formUser.cleaned_data['password'])
        user.save()

        persona = formPerson.save(commit=False)
        persona.user = user
        persona.save()

        Bitacora.objects.create(
            usuario=created_by,
            persona=created_by.persona if hasattr(created_by, 'persona') else None,
            rol=created_by.usuariorol.rol if hasattr(created_by, 'usuariorol') else None,
            accion='create',
            detalle=f"Usuario {user.username} añadido."
        )

        return user

    def __init__(self, user):
        """Inicializa el adaptador con un usuario específico."""
        self.user = user

    def update_user(self, formUser, formPerson, password_actual, password_nueva, updated_by):
        """
        Actualiza la información de un usuario y su persona asociada.
        """
        if password_nueva and password_actual:
            if self.user.check_password(password_actual):
                self.user.password = make_password(password_nueva)
            else:
                return {'password_actual': ['Contraseña actual incorrecta']}

        formUser.save()
        formPerson.save()

        # Registrar en bitácora
        Bitacora.objects.create(
            usuario=updated_by,
            persona=updated_by.persona if hasattr(updated_by, 'persona') else None,
            rol=updated_by.usuariorol.rol if hasattr(updated_by, 'usuariorol') else None,
            accion='update',
            detalle=f"Usuario {self.user.username} actualizado."
        )

        return None  # No hay errores


    def delete_user(self, deleted_by):
            """Elimina al usuario y registra la acción en la bitácora."""
            if hasattr(self.user, 'persona'):
                self.user.persona.delete()

            Bitacora.objects.create(
                usuario=deleted_by,
                persona=deleted_by.persona if hasattr(deleted_by, 'persona') else None,
                rol=deleted_by.usuariorol.rol if hasattr(deleted_by, 'usuariorol') else None,
                accion='delete',
                detalle=f"Usuario {self.user.username} eliminado."
            )

            self.user.delete()



    def assign_role(self, rol_id, assigned_by):
        """Asigna un rol a un usuario y registra la acción en la bitácora."""
        try:
            rol = Rol.objects.get(id=rol_id)
            UsuarioRol.objects.update_or_create(user=self.user, defaults={'rol': rol})

            # Registrar en la bitácora
            Bitacora.objects.create(
                usuario=assigned_by,
                persona=assigned_by.persona if hasattr(assigned_by, 'persona') else None,
                rol=assigned_by.usuariorol.rol if hasattr(assigned_by, 'usuariorol') else None,
                accion='update',
                detalle=f"Rol {rol.nombre} asignado al usuario {self.user.username}."
            )

            return {'success': True}
        except Rol.DoesNotExist:
            return {'success': False, 'error': 'El rol seleccionado no existe.'}


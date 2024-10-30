from django.db import models
from django.contrib.auth.models import User,Permission

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
    correo = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ('ver_persona', 'Puede ver el perfil de persona'),
            ('editar_persona', 'Puede editar el perfil de persona'),
            ('actualizar_persona', 'Puede actualizar el perfil de persona'),
            ('borrar_persona', 'Puede borrar el perfil de persona'),
              
        ]
        db_table = 'Persona'
        verbose_name_plural = 'Personas'
       
    def __str__(self):
        return f"{self.nombre} {self.apPaterno} {self.apMaterno}"


class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    permisos = models.ManyToManyField(Permission, blank=True)  # Un rol tiene varios permisos

    class Meta:
        db_table = 'Roles'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.nombre        

class UsuarioRol(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Usuarios_Roles'
        verbose_name_plural = 'Usuarios Roles'
    
    def __str__(self):
        return f"{self.user.username} - {self.rol.nombre}"        
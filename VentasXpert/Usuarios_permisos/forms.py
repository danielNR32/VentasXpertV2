from django import forms
from django.contrib.auth.models import User,Permission,ContentType
from .models import Persona, Rol, UsuarioRol

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={
                'class': 'form-control', 'placeholder': 'Contraseña', 'id': 'user_password'}),
            'username': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nombre de usuario', 'id': 'user_username'}),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 'placeholder': 'Correo electrónico', 'id': 'user_email'}),
        }

class PersonForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = [
            'nombre', 'segNombre', 'apPaterno', 'apMaterno', 'genero',
            'correo', 'telefono', 'rfc', 'curp'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre', 'id': 'person_nombre'}),
            'segNombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Segundo Nombre', 'id': 'person_segNombre'}),
            'apPaterno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Paterno', 'id': 'person_apPaterno'}),
            'apMaterno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Materno', 'id': 'person_apMaterno'}),
            'genero': forms.Select(attrs={'class': 'form-control', 'id': 'person_genero'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo', 'id': 'person_correo'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono', 'id': 'person_telefono'}),
            'rfc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RFC', 'id': 'person_rfc'}),
            'curp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CURP', 'id': 'person_curp'}),
        }

class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ['nombre', 'permisos']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'permisos': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': 10  # Adjust the size as needed for better UX
            }),
        }

class PermForm(forms.ModelForm):
    content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Tipo de Contenido"
    )

    class Meta:
        model = Permission
        fields = ['name', 'codename', 'content_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Permiso'}),
            'codename': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Codename'}),
        }
class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # Excluir 'password' aquí
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nombre de usuario', 
                'id': 'user_username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Correo electrónico', 
                'id': 'user_email'
            }),
        }

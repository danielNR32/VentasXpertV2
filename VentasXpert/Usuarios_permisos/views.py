from django.forms import model_to_dict
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import    EditUserForm, PermForm, PersonForm, RolForm, UserForm
from .models import Bitacora, Rol, UsuarioRol, Persona
from django.contrib.auth.models import User,Permission,ContentType
from django.template.loader import render_to_string

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.views.decorators.http import require_POST

@login_required
def usuarios_permisos_home(request):
    bitacoras = Bitacora.objects.all().order_by('-created_at')  # Ordenar por fecha más reciente
    return render(request, 'Usuarios_permisos/home.html', {'bitacoras': bitacoras})

@login_required
def logout_view(request):
    # Registrar el cierre de sesión antes de hacer logout
    if request.user.is_authenticated:
        Bitacora.objects.create(
            usuario=request.user,
            persona=request.user.persona if hasattr(request.user, 'persona') else None,
            rol=request.user.usuariorol.rol if hasattr(request.user, 'usuariorol') else None,
            accion='logout',
            detalle=f"Cierre de sesión para el usuario {request.user.username}."
        )

    logout(request)
    return redirect('login')

"""
!Apartado para las vistas, modales, formularios 
    como: añadir, editar, elimnar y asignar en Usuarios.!

"""

@login_required
def users(request):
    formUser = UserForm()
    formPerson = PersonForm()
    user = User.objects.prefetch_related('usuariorol', 'persona').all()  # Incluye las relaciones
    roles = Rol.objects.all()  # Obtener todos los roles
    return render(
        request,
        'Usuarios_permisos/users.html',
        {
            'formUser': formUser,
            'formPerson': formPerson,
            'Usuarios': user,  # Asegúrate de enviar los usuarios aquí
            'roles': roles,  # Enviar los roles al template
        }
    )


@login_required
def add_user(request):
    if request.method == 'POST':
        formUser = UserForm(request.POST)
        formPerson = PersonForm(request.POST)

        if formUser.is_valid() and formPerson.is_valid():
            user = formUser.save(commit=False)
            user.set_password(formUser.cleaned_data['password'])
            user.save()

            persona = formPerson.save(commit=False)
            persona.user = user
            persona.save()

            # Registrar en la bitácora
            Bitacora.objects.create(
                usuario=request.user,
                persona=request.user.persona if hasattr(request.user, 'persona') else None,
                rol=request.user.usuariorol.rol if hasattr(request.user, 'usuariorol') else None,
                accion='create',
                detalle=f"Usuario {user.username} añadido."
            )

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Usuario añadido correctamente'})
            
            return redirect('usuarios')
        
        errors = {**formUser.errors, **formPerson.errors}
        return JsonResponse({'success': False, 'errors': errors})

    return JsonResponse({'success': False, 'message': 'Método no permitido'})


#? Editar de usuarios
@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    try:
        persona = Persona.objects.get(user=user)
    except Persona.DoesNotExist:
        raise Http404("No se encontró una Persona asociada con este usuario.")

    if request.method == 'POST':
        formUser = EditUserForm(request.POST, instance=user)
        formPerson = PersonForm(request.POST, instance=persona)

        if formUser.is_valid() and formPerson.is_valid():
            password_actual = request.POST.get('password_actual')
            password_nueva = request.POST.get('new_password')

            if password_nueva and password_actual:
                if authenticate(username=user.username, password=password_actual):
                    user.password = make_password(password_nueva)
                else:
                    return JsonResponse({'success': False, 'errors': {'password_actual': ['Contraseña actual incorrecta']}})
            
            formUser.save()
            formPerson.save()

            # Registrar en la bitácora
            Bitacora.objects.create(
                usuario=request.user,
                persona=request.user.persona if hasattr(request.user, 'persona') else None,
                rol=request.user.usuariorol.rol if hasattr(request.user, 'usuariorol') else None,
                accion='update',
                detalle=f"Usuario {user.username} actualizado."
            )

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Usuario actualizado correctamente'})
            
            return redirect('usuarios')

        errors = {**formUser.errors, **formPerson.errors}
        return JsonResponse({'success': False, 'errors': errors})

    elif request.method == 'GET':
        formUser = EditUserForm(instance=user)
        formPerson = PersonForm(instance=persona)

        return JsonResponse({
            'formUser': {
                'username': formUser['username'].value(),
                'email': formUser['email'].value(),
            },
            'formPerson': {
                'nombre': formPerson['nombre'].value(),
                'segNombre': formPerson['segNombre'].value(),
                'apPaterno': formPerson['apPaterno'].value(),
                'apMaterno': formPerson['apMaterno'].value(),
                'genero': formPerson['genero'].value(),
                'telefono': formPerson['telefono'].value(),
                'rfc': formPerson['rfc'].value(),
                'curp': formPerson['curp'].value(),
                'correo': formPerson['correo'].value(),
            }
        })

    return redirect('usuarios')







@login_required
def eliminar_usuario(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)

        # Elimina el objeto Persona asociado si existe
        if hasattr(user, 'persona'):
            user.persona.delete()

        # Registrar en la bitácora
        Bitacora.objects.create(
            usuario=request.user,
            persona=request.user.persona if hasattr(request.user, 'persona') else None,
            rol=request.user.usuariorol.rol if hasattr(request.user, 'usuariorol') else None,
            accion='delete',
            detalle=f"Usuario {user.username} eliminado."
        )

        # Elimina el usuario
        user.delete()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)




@login_required
def assign_role_to_user(request, id_user):
    # Obtenemos el usuario por ID
    user = get_object_or_404(User, id=id_user)

    if request.method == 'POST':
        # Obtenemos el ID del rol desde la solicitud POST
        rol_id = request.POST.get('rol', None)
        if rol_id:
            try:
                # Obtenemos el objeto Rol correspondiente al ID proporcionado
                rol = Rol.objects.get(id=rol_id)
                # Actualizamos o creamos la relación Usuario-Rol
                UsuarioRol.objects.update_or_create(user=user, defaults={'rol': rol})

                # Registrar en la bitácora
                Bitacora.objects.create(
                    usuario=request.user,
                    persona=request.user.persona if hasattr(request.user, 'persona') else None,
                    rol=request.user.usuariorol.rol if hasattr(request.user, 'usuariorol') else None,
                    accion='update',
                    detalle=f"Rol {rol.nombre} asignado al usuario {user.username}."
                )

                return JsonResponse({'success': True})
            except Rol.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'El rol seleccionado no existe.'})
        return JsonResponse({'success': False, 'error': 'No se proporcionó un rol válido.'})
    else:
        # Para solicitudes GET, obtenemos todos los roles disponibles
        roles = Rol.objects.all()
        return render(
            request,
            'Usuarios_permisos/modals/assign_role_to_user.html',
            {
                'usuario': user,
                'roles': roles,
            }
        )










"""
    !Apartado para las vistas, modales, formularios 
    !como: añadir, editar, elimnar y asignar en Roles.!
"""
#? Vista de roles
@login_required
def roles(request):
    form = RolForm()
    roles = Rol.objects.all()
    permisos = Permission.objects.all()
    return render(request, 'Usuarios_permisos/roles.html', {'form': form, 'Roles': roles, 'permisos': permisos})

#? Añadir de roles
@login_required
def add_role(request):
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            rol = form.save()

            # Registrar en la bitácora
            Bitacora.objects.create(
                usuario=request.user,
                persona=request.user.persona if hasattr(request.user, 'persona') else None,
                rol=request.user.usuariorol.rol if hasattr(request.user, 'usuariorol') else None,
                accion='create',
                detalle=f"Rol {rol.nombre} creado."
            )

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Rol añadido correctamente'})
            return redirect('roles')  # Redirige si no es una solicitud AJAX
    else:
        form = RolForm()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'Usuarios_permisos/modals/add_role.html', {'form': form})
    
    return render(request, 'Usuarios_permisos/roles.html', {'form': form})


#? Editar de roles
@login_required
def edit_role(request, role_id):
    rol = get_object_or_404(Rol, id=role_id)

    if request.method == 'POST':
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            rol = form.save()

            # Registrar en la bitácora
            Bitacora.objects.create(
                usuario=request.user,
                persona=request.user.persona if hasattr(request.user, 'persona') else None,
                rol=request.user.usuariorol.rol if hasattr(request.user, 'usuariorol') else None,
                accion='update',
                detalle=f"Rol {rol.nombre} actualizado."
            )

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Rol actualizado correctamente'})
            return redirect('roles')
    else:
        form = RolForm(instance=rol)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'Usuarios_permisos/modals/edit_role.html', {'form': form, 'rol': rol})

    return redirect('roles')



@login_required
def get_role_data(request, role_id):
    rol = get_object_or_404(Rol, id=role_id)
    permisos_ids = list(rol.permisos.values_list('id', flat=True))
    data = {
        'nombre': rol.nombre,
        'permisos_ids': permisos_ids,
    }
    return JsonResponse(data)


@login_required
def delete_role(request, role_id):
    rol = get_object_or_404(Rol, id=role_id)

    # Registrar en la bitácora antes de eliminar
    Bitacora.objects.create(
        usuario=request.user,
        persona=request.user.persona if hasattr(request.user, 'persona') else None,
        rol=request.user.usuariorol.rol if hasattr(request.user, 'usuariorol') else None,
        accion='delete',
        detalle=f"Rol {rol.nombre} eliminado."
    )

    rol.delete()
    return redirect('roles')



"""
    !Apartado para las vistas, modales, formularios 
    como: añadir, editar, elimnar y asignar en Permisos.!

"""

@login_required
def permissions(request):
    permisos = Permission.objects.all()  # Obtener todos los permisos
    form = PermForm()
    return render(request, 'Usuarios_permisos/permissions.html', {'permisos': permisos,'form':form})

@login_required
def add_permission(request):
    if request.method == 'POST':
        form = PermForm(request.POST)
        if form.is_valid():
            permiso = form.save()

            # Registrar en la bitácora
            Bitacora.objects.create(
                usuario=request.user,
                persona=request.user.persona if hasattr(request.user, 'persona') else None,
                rol=request.user.usuariorol.rol if hasattr(request.user, 'usuariorol') else None,
                accion='create',
                detalle=f"Permiso {permiso.name} creado."
            )

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = PermForm()
    
    return render(request, 'Usuarios_permisos/modals/add_permission.html', {'form': form})


@login_required
def edit_permission(request, permission_id):
    permission = get_object_or_404(Permission, id=permission_id)

    if request.method == 'POST':
        form = PermForm(request.POST, instance=permission)
        if form.is_valid():
            permiso_editado = form.save()

            # Registrar en la bitácora
            Bitacora.objects.create(
                usuario=request.user,
                persona=request.user.persona if hasattr(request.user, 'persona') else None,
                rol=request.user.usuariorol.rol if hasattr(request.user, 'usuariorol') else None,
                accion='update',
                detalle=f"Permiso {permiso_editado.name} actualizado."
            )

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = PermForm(instance=permission)
    
    return render(request, 'Usuarios_permisos/modals/edit_permission.html', {'form': form, 'permission_id': permission_id})

@require_POST
@login_required
def delete_permission(request, permission_id):
    permiso = get_object_or_404(Permission, id=permission_id)

    # Registrar en la bitácora antes de eliminar
    Bitacora.objects.create(
        usuario=request.user,
        persona=request.user.persona if hasattr(request.user, 'persona') else None,
        rol=request.user.usuariorol.rol if hasattr(request.user, 'usuariorol') else None,
        accion='delete',
        detalle=f"Permiso {permiso.name} eliminado."
    )

    permiso.delete()
    return JsonResponse({'success': True})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from Usuarios_permisos.models import UsuarioMFA, UsuarioRol
from django.contrib.auth.models import User
import pyotp
import qrcode
from io import BytesIO
import base64


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Guarda temporalmente al usuario en la sesión para MFA
            request.session['pre_auth_user_id'] = user.id
            
            # Verifica si el usuario tiene configurado el MFA
            try:
                mfa = UsuarioMFA.objects.get(user=user)
                if mfa.mfa_secret:  # Si ya tiene MFA configurado
                    return redirect('verify_totp')  # Redirige a la verificación del OTP
            except UsuarioMFA.DoesNotExist:
                # Si no existe el registro, redirige a la configuración de MFA
                return redirect('configure_mfa')
        else:
            # Error de autenticación
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})

    return render(request, 'login.html')


def configure_mfa(request):
    # Verifica si el usuario está en sesión pre-autenticado
    pre_auth_user_id = request.session.get('pre_auth_user_id')
    if not pre_auth_user_id:
        return redirect('login')

    # Recupera al usuario
    user = User.objects.get(id=pre_auth_user_id)

    # Obtiene o crea el registro MFA
    mfa, created = UsuarioMFA.objects.get_or_create(user=user)

    # Generar un secreto MFA si no existe
    if not mfa.mfa_secret:
        secret = pyotp.random_base32()
        mfa.mfa_secret = secret
        mfa.save()

    # Generar la URI para el código QR
    totp = pyotp.TOTP(mfa.mfa_secret)
    qr_uri = totp.provisioning_uri(name=user.email, issuer_name="VentasXpert")

    # Crear la imagen QR
    qr = qrcode.make(qr_uri)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    # Codificar la imagen QR en base64
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    # Renderizar la plantilla con el QR en base64
    context = {'qr_code': qr_base64}
    return render(request, 'configure_mfa.html', context)


def verify_totp(request):
    if request.method == 'POST':
        otp_token = request.POST.get('otp_code')  # Código OTP introducido por el usuario
        pre_auth_user_id = request.session.get('pre_auth_user_id')

        # Si no hay usuario preautenticado, redirige al login
        if not pre_auth_user_id:
            return redirect('login')

        try:
            # Recupera al usuario preautenticado
            user = User.objects.get(id=pre_auth_user_id)

            # Verifica si el usuario tiene MFA configurado
            mfa = UsuarioMFA.objects.get(user=user)

            # Genera el TOTP con el secreto almacenado
            totp = pyotp.TOTP(mfa.mfa_secret)

            # Verifica si el código OTP introducido es válido
            if totp.verify(otp_token):
                login(request, user)  # Autentica al usuario
                del request.session['pre_auth_user_id']  # Limpia la sesión temporal

                # Redirige al usuario según su rol
                usuario_rol = UsuarioRol.objects.filter(user=user).first()
                rol_nombre = usuario_rol.rol.nombre if usuario_rol else None

                if rol_nombre == 'SU':
                    return redirect('usuarios_permisos_home')
                elif rol_nombre == 'Administrador':
                    return redirect('administrador_home')
                elif rol_nombre == 'Cajero':
                    return redirect('cajero_home')
                else:
                    return redirect('catalogo_home')
            else:
                # Código OTP incorrecto
                return render(request, 'verify_totp.html', {'error': 'Código OTP incorrecto'})

        except User.DoesNotExist:
            # Usuario no encontrado, redirige al login
            return redirect('login')

    return render(request, 'verify_totp.html')


def logout_view(request):
    logout(request)
    return redirect('login')
